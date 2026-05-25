"""OCR + ducat lookup + recommendation pipeline."""

from __future__ import annotations

import io
import re
from typing import TYPE_CHECKING

from PIL import Image
from pydantic import BaseModel

if TYPE_CHECKING:
    from rapidocr_onnxruntime import RapidOCR as _RapidOCRType

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ItemResult(BaseModel):
    """A matched Prime component with its ducat value and recommendation."""

    name: str
    ducats: int
    recommendation: str


class Totals(BaseModel):
    """Summary statistics for the OCR analysis."""

    items_detected: int
    items_matched: int
    ducats_sum: int


class AnalyzeResult(BaseModel):
    """Complete result of OCR analysis including matched items and summary totals."""

    items: list[ItemResult]
    totals: Totals


# ---------------------------------------------------------------------------
# Lazy engine cache
# ---------------------------------------------------------------------------

_engine: "_RapidOCRType | None" = None


def _get_engine() -> "_RapidOCRType":
    """Return the module-level RapidOCR engine, loading it on first call."""
    global _engine
    if _engine is None:
        from rapidocr_onnxruntime import RapidOCR  # noqa: PLC0415

        _engine = RapidOCR()
    return _engine


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------

_PUNCT_RE = re.compile(r"[^\w\s]")


def normalize(text: str) -> str:
    """Return a lowercase, punctuation-stripped, whitespace-collapsed version of text.

    Punctuation characters are replaced with a space (not deleted) so that
    token boundaries adjacent to punctuation are preserved. Whitespace is
    then collapsed to a single space and leading/trailing space is stripped.

    Examples:
        "Wisp Prime Blueprint!" -> "wisp prime blueprint"
        "  Braton  Prime  Barrel  " -> "braton prime barrel"
        "Volt--Prime Blueprint" -> "volt prime blueprint"
        "" -> ""
    """
    text = text.lower()
    text = _PUNCT_RE.sub(" ", text)
    text = " ".join(text.split())
    return text


def recommend(ducats: int) -> str:
    """Return a sell recommendation string based on the ducat value.

    Thresholds (per _architecture.md API contract):
        >= 65            -> "high-value sell"
        45 or 25         -> "mid-value consider"
        <= 15            -> "low-value keep"

    Values that fall between thresholds but are not explicitly listed
    (e.g. 26, 30, 50) default to "mid-value consider" so that any
    unknown ducat value gets a safe, non-alarming label.
    """
    if ducats >= 65:
        return "high-value sell"
    if ducats in (25, 45):
        return "mid-value consider"
    if ducats <= 15:
        return "low-value keep"
    # Catch-all for any ducat value not explicitly in the threshold table
    return "mid-value consider"


# ---------------------------------------------------------------------------
# Bbox spatial helpers
# ---------------------------------------------------------------------------


def _bbox_center(bbox: list) -> tuple[float, float, float]:
    """Compute (center_x, center_y, height) from a RapidOCR bbox polygon.

    RapidOCR returns bbox as 4 corner points in order:
        [top-left, top-right, bottom-right, bottom-left]
    Each point is [x, y].

    center_x  = mean of all 4 x-coords
    center_y  = mean of all 4 y-coords
    height    = abs(mean of bottom y-coords - mean of top y-coords)
    """
    xs = [pt[0] for pt in bbox]
    ys = [pt[1] for pt in bbox]
    center_x = sum(xs) / 4.0
    center_y = sum(ys) / 4.0
    # Top two points are index 0 and 1; bottom two are index 2 and 3
    top_y = (bbox[0][1] + bbox[1][1]) / 2.0
    bottom_y = (bbox[2][1] + bbox[3][1]) / 2.0
    height = abs(bottom_y - top_y)
    return (center_x, center_y, height)


def _group_detections(
    detections: list[tuple[list, str, float]],
    ducat_lookup: dict[str, int],
) -> tuple[list[ItemResult], int]:
    """Group OCR detections spatially to build compound item names.

    Each Kiosk card prints the weapon name (containing "prime") on one line
    and the component (e.g. "Receiver", "Blueprint") on the line directly
    below it. RapidOCR returns these as separate detections, so they must be
    spatially paired before lookup.

    Algorithm:
        For each detection whose normalised text contains "prime" (anchor):
            1. Find the nearest detection BELOW it within 2 * anchor.height
               vertical distance AND within 3 * anchor.height horizontal
               distance (same card column, not the next card over).
            2. Try compound lookup: normalize("<anchor> <component>").
            3. If compound misses, fall back to anchor-only lookup.
        Deduplicate: each detection index may only be used as a component once.

    Args:
        detections: list of (bbox, raw_text, confidence) tuples, already
                    filtered by confidence and minimum text length.
        ducat_lookup: mapping of normalised item name -> ducat value.

    Returns:
        Tuple of (list[ItemResult], items_detected) where items_detected is
        the count of distinct anchor detections found.
    """
    # Pre-compute geometry for every detection
    geo: list[tuple[float, float, float]] = []
    for bbox, _text, _conf in detections:
        geo.append(_bbox_center(bbox))

    items_detected = 0
    matched: list[ItemResult] = []
    seen_normalized: set[str] = set()
    used_component_indices: set[int] = set()

    for anchor_idx, (bbox, raw_text, _conf) in enumerate(detections):
        norm_anchor = normalize(raw_text)
        if "prime" not in norm_anchor:
            continue

        items_detected += 1
        anchor_cx, anchor_cy, anchor_h = geo[anchor_idx]
        v_threshold = 2.0 * anchor_h
        h_threshold = 3.0 * anchor_h

        # Find the closest detection directly below the anchor
        best_candidate_idx: int | None = None
        best_distance: float = float("inf")

        for cand_idx, (_cbbox, cand_text, _cconf) in enumerate(detections):
            if cand_idx == anchor_idx:
                continue
            if cand_idx in used_component_indices:
                continue

            cand_norm = normalize(cand_text)
            # Skip detections that are also anchors — they pair with their own components
            if "prime" in cand_norm:
                continue

            cand_cx, cand_cy, _cand_h = geo[cand_idx]

            dy = cand_cy - anchor_cy
            dx = abs(cand_cx - anchor_cx)

            # Must be BELOW the anchor (positive dy) within vertical threshold
            if dy <= 0 or dy > v_threshold:
                continue

            # Must be within horizontal threshold (same card column)
            if dx > h_threshold:
                continue

            if dy < best_distance:
                best_distance = dy
                best_candidate_idx = cand_idx

        # Build lookup key — compound first, anchor-only fallback
        lookup_key: str
        display_name: str
        component_text: str | None = None

        if best_candidate_idx is not None:
            component_text = detections[best_candidate_idx][1]
            compound_norm = normalize(f"{raw_text} {component_text}")
            if compound_norm in ducat_lookup:
                lookup_key = compound_norm
                display_name = f"{raw_text.strip()} {component_text.strip()}"
            else:
                # Compound miss — try anchor alone
                if norm_anchor in ducat_lookup:
                    lookup_key = norm_anchor
                    display_name = raw_text.strip()
                else:
                    # Neither matched — still counted as detected, not matched
                    continue
        else:
            # No component candidate found — try anchor alone
            if norm_anchor in ducat_lookup:
                lookup_key = norm_anchor
                display_name = raw_text.strip()
            else:
                continue

        if lookup_key in seen_normalized:
            continue

        seen_normalized.add(lookup_key)
        if best_candidate_idx is not None and component_text is not None:
            # Mark component as used so it isn't paired with another anchor
            used_component_indices.add(best_candidate_idx)

        ducat_value = ducat_lookup[lookup_key]
        matched.append(
            ItemResult(
                name=display_name,
                ducats=ducat_value,
                recommendation=recommend(ducat_value),
            )
        )

    return matched, items_detected


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

_OCR_CONFIDENCE_THRESHOLD = 0.5
_OCR_MIN_TEXT_LENGTH = 3


async def analyze_image(
    image_bytes: bytes,
    ducat_lookup: dict[str, int],
) -> AnalyzeResult:
    """Run the full OCR → spatial grouping → lookup → recommend pipeline on image bytes.

    Steps:
    1. Decode bytes to PIL Image; convert to RGB.
    2. Re-encode as PNG bytes for RapidOCR consumption.
    3. Run RapidOCR; filter by confidence > threshold and text length >= minimum.
    4. Call _group_detections to spatially pair anchor ("prime") detections with
       their nearest component text and perform ducat lookup.
    5. Build AnalyzeResult from grouped matches and aggregate Totals.
    """
    # Decode and normalise colour space
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Re-encode to bytes for RapidOCR (accepts file path or bytes)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    engine = _get_engine()
    ocr_result, _ = engine(png_bytes)

    # OCR may return None when no text is found
    if not ocr_result:
        return AnalyzeResult(
            items=[],
            totals=Totals(items_detected=0, items_matched=0, ducats_sum=0),
        )

    # Filter by confidence and minimum text length
    filtered: list[tuple[list, str, float]] = []
    for detection in ocr_result:
        if len(detection) < 3:
            continue
        bbox, raw_text, confidence = detection[0], detection[1], detection[2]
        if confidence is None or float(confidence) <= _OCR_CONFIDENCE_THRESHOLD:
            continue
        if len(raw_text) < _OCR_MIN_TEXT_LENGTH:
            continue
        filtered.append((bbox, raw_text, float(confidence)))

    matched, items_detected = _group_detections(filtered, ducat_lookup)
    ducats_sum = sum(item.ducats for item in matched)

    return AnalyzeResult(
        items=matched,
        totals=Totals(
            items_detected=items_detected,
            items_matched=len(matched),
            ducats_sum=ducats_sum,
        ),
    )
