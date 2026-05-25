"""Unit and integration tests for backend.analyze pipeline."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from backend.analyze import (
    AnalyzeResult,
    ItemResult,
    Totals,
    _bbox_center,
    _group_detections,
    analyze_image,
    normalize,
    recommend,
)

# ---------------------------------------------------------------------------
# Repo root — used to locate image.png test fixture
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).parent.parent.parent


# ---------------------------------------------------------------------------
# TestNormalize
# ---------------------------------------------------------------------------


class TestNormalize:
    def test_lowercases_input(self) -> None:
        assert normalize("Wisp Prime Blueprint") == "wisp prime blueprint"

    def test_strips_punctuation(self) -> None:
        assert normalize("Braton Prime Barrel!") == "braton prime barrel"

    def test_collapses_whitespace(self) -> None:
        assert normalize("Ash  Prime   Systems  Blueprint") == "ash prime systems blueprint"

    def test_strips_leading_trailing_whitespace(self) -> None:
        assert normalize("  Boltor Prime Blueprint  ") == "boltor prime blueprint"

    def test_punctuation_in_middle(self) -> None:
        # Apostrophe is replaced with a space, then collapsed — "Mag's" -> "mag s"
        assert normalize("Mag's Prime Systems") == "mag s prime systems"

    def test_empty_string(self) -> None:
        assert normalize("") == ""

    def test_whitespace_only(self) -> None:
        assert normalize("   ") == ""

    def test_already_normalized(self) -> None:
        assert normalize("wisp prime blueprint") == "wisp prime blueprint"

    def test_mixed_punctuation_and_spaces(self) -> None:
        assert normalize("  Volt--Prime  Blueprint!! ") == "volt prime blueprint"


# ---------------------------------------------------------------------------
# TestRecommend
# ---------------------------------------------------------------------------


class TestRecommend:
    def test_high_value_sell_above_threshold(self) -> None:
        assert recommend(100) == "high-value sell"

    def test_high_value_sell_at_threshold(self) -> None:
        assert recommend(65) == "high-value sell"

    def test_mid_value_consider_45(self) -> None:
        assert recommend(45) == "mid-value consider"

    def test_mid_value_consider_25(self) -> None:
        assert recommend(25) == "mid-value consider"

    def test_low_value_keep_at_threshold(self) -> None:
        assert recommend(15) == "low-value keep"

    def test_low_value_keep_below_threshold(self) -> None:
        assert recommend(0) == "low-value keep"

    # Boundary checks
    def test_boundary_64_is_not_high_value(self) -> None:
        assert recommend(64) != "high-value sell"

    def test_boundary_16_is_not_low_value(self) -> None:
        assert recommend(16) != "low-value keep"

    def test_boundary_26_is_not_low_value(self) -> None:
        assert recommend(26) != "low-value keep"


# ---------------------------------------------------------------------------
# TestBboxCenter
# ---------------------------------------------------------------------------


class TestBboxCenter:
    """Unit tests for _bbox_center geometry helper."""

    def test_axis_aligned_unit_square(self) -> None:
        # top-left, top-right, bottom-right, bottom-left
        bbox = [[0, 0], [10, 0], [10, 20], [0, 20]]
        cx, cy, h = _bbox_center(bbox)
        assert cx == pytest.approx(5.0)
        assert cy == pytest.approx(10.0)
        assert h == pytest.approx(20.0)

    def test_axis_aligned_typical_text_line(self) -> None:
        # 100x15 text bounding box
        bbox = [[50, 100], [150, 100], [150, 115], [50, 115]]
        cx, cy, h = _bbox_center(bbox)
        assert cx == pytest.approx(100.0)
        assert cy == pytest.approx(107.5)
        assert h == pytest.approx(15.0)

    def test_skewed_bbox_produces_sensible_center(self) -> None:
        # Slightly skewed (as OCR sometimes returns)
        bbox = [[10, 5], [90, 8], [88, 22], [12, 19]]
        cx, cy, h = _bbox_center(bbox)
        # center_x ≈ (10+90+88+12)/4 = 50
        assert cx == pytest.approx(50.0)
        # center_y ≈ (5+8+22+19)/4 = 13.5
        assert cy == pytest.approx(13.5)
        # height = abs(mean(22,19) - mean(5,8)) = abs(20.5 - 6.5) = 14.0
        assert h == pytest.approx(14.0)

    def test_height_is_always_non_negative(self) -> None:
        # Even if top/bottom ordering is swapped (should not happen but defensive)
        bbox = [[0, 20], [10, 20], [10, 0], [0, 0]]
        _cx, _cy, h = _bbox_center(bbox)
        assert h >= 0.0


# ---------------------------------------------------------------------------
# TestGroupDetections
# ---------------------------------------------------------------------------

# Minimal bbox that satisfies _bbox_center: axis-aligned 100x20 boxes
# placed at different vertical positions.
def _make_bbox(x: float, y: float, w: float = 100.0, h: float = 20.0) -> list:
    """Return a 4-point axis-aligned bbox with top-left at (x, y)."""
    return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]


class TestGroupDetections:
    """Unit tests for the _group_detections spatial grouping function."""

    # ducat_lookup used across most test cases
    _lookup: dict[str, int] = {
        "wisp prime systems": 45,
        "wisp prime blueprint": 15,
        "saryn prime neuroptics": 65,
        "akarius prime receiver": 65,
    }

    def test_two_detection_card_matches_compound(self) -> None:
        """Anchor 'Wisp Prime' + component 'Systems' directly below → compound match."""
        detections = [
            (_make_bbox(100, 100), "Wisp Prime", 0.95),
            (_make_bbox(100, 125), "Systems", 0.90),
        ]
        items, items_detected = _group_detections(detections, self._lookup)
        assert items_detected == 1
        assert len(items) == 1
        assert items[0].ducats == 45
        assert "wisp prime" in items[0].name.lower()
        assert "systems" in items[0].name.lower()

    def test_anchor_alone_fallback_when_no_nearby_component(self) -> None:
        """Anchor alone (no candidate within proximity) tries anchor-only lookup."""
        lookup_with_bare = {"wisp prime": 25}
        detections = [
            (_make_bbox(100, 100), "Wisp Prime", 0.95),
        ]
        items, items_detected = _group_detections(detections, lookup_with_bare)
        assert items_detected == 1
        assert len(items) == 1
        assert items[0].ducats == 25

    def test_far_below_detection_does_not_pair(self) -> None:
        """Component detection > 2*height below anchor: vertical threshold rejects it."""
        # anchor height = 20, threshold = 40; place component at dy=50 (> 40)
        detections = [
            (_make_bbox(100, 100), "Wisp Prime", 0.95),
            (_make_bbox(100, 155), "Systems", 0.90),  # dy = 155+10 - (100+10) = 55 > 40
        ]
        # No compound key and no bare "wisp prime" key → not matched
        items, items_detected = _group_detections(detections, self._lookup)
        assert items_detected == 1
        assert len(items) == 0

    def test_horizontal_proximity_rejects_next_card_over(self) -> None:
        """Component on a different card (far horizontal offset) is not paired."""
        # anchor at x=100, component at x=400; h_threshold = 3*20 = 60; dx=300+50=350 > 60
        detections = [
            (_make_bbox(100, 100), "Wisp Prime", 0.95),
            (_make_bbox(400, 125), "Systems", 0.90),
        ]
        items, items_detected = _group_detections(detections, self._lookup)
        assert items_detected == 1
        assert len(items) == 0

    def test_multiple_anchors_pair_with_own_components(self) -> None:
        """Two cards side-by-side: each anchor pairs with its own component."""
        lookup = {
            "wisp prime blueprint": 15,
            "saryn prime neuroptics": 65,
        }
        detections = [
            (_make_bbox(100, 100), "Wisp Prime", 0.95),   # anchor 1
            (_make_bbox(100, 125), "Blueprint", 0.90),    # component 1 (below anchor 1)
            (_make_bbox(400, 100), "Saryn Prime", 0.95),  # anchor 2
            (_make_bbox(400, 125), "Neuroptics", 0.90),   # component 2 (below anchor 2)
        ]
        items, items_detected = _group_detections(detections, lookup)
        assert items_detected == 2
        assert len(items) == 2
        names_lower = {item.name.lower() for item in items}
        assert any("wisp" in n for n in names_lower)
        assert any("saryn" in n for n in names_lower)

    def test_compound_miss_and_anchor_miss_not_counted_in_matched(self) -> None:
        """Compound misses lookup, anchor also misses → detected but not matched."""
        # "unknown prime" and "gadget" do not appear in lookup
        detections = [
            (_make_bbox(100, 100), "Unknown Prime", 0.95),
            (_make_bbox(100, 125), "Gadget", 0.90),
        ]
        items, items_detected = _group_detections(detections, self._lookup)
        assert items_detected == 1
        assert len(items) == 0

    def test_component_not_reused_across_two_anchors(self) -> None:
        """A component directly below two stacked anchors is consumed by the first."""
        lookup = {
            "akarius prime receiver": 65,
            "wisp prime receiver": 100,
        }
        # Two anchors stacked; single component below both.
        # anchor1 at y=100, anchor2 at y=125, component at y=150
        # anchor2 is closer to component (dy=25) than anchor1 (dy=50);
        # depending on iteration order, the first anchor that claims it wins.
        detections = [
            (_make_bbox(100, 100), "Akarius Prime", 0.95),
            (_make_bbox(100, 125), "Wisp Prime", 0.95),
            (_make_bbox(100, 150), "Receiver", 0.90),
        ]
        items, items_detected = _group_detections(detections, lookup)
        assert items_detected == 2
        # At most one should match the compound with "Receiver" (component used once)
        compound_matches = [i for i in items if "receiver" in i.name.lower()]
        assert len(compound_matches) <= 1


# ---------------------------------------------------------------------------
# TestAnalyzeImage — integration (loads real image.png + RapidOCR)
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestAnalyzeImage:
    """Integration tests that run real OCR on image.png.

    First run may take 5-10 seconds while RapidOCR downloads ONNX models.
    """

    _image_path = _REPO_ROOT / "image.png"
    _ducat_sample: dict[str, int] = {}

    @classmethod
    def _get_ducats(cls) -> dict[str, int]:
        if not cls._ducat_sample:
            from backend.ducats import load_ducats  # noqa: PLC0415

            cls._ducat_sample = load_ducats()
        return cls._ducat_sample

    def test_image_fixture_exists(self) -> None:
        assert self._image_path.exists(), f"Test fixture not found: {self._image_path}"

    def test_items_matched_greater_than_zero(self) -> None:
        """Core abort condition: RapidOCR on image.png must match at least one Prime part."""
        ducats = self._get_ducats()
        image_bytes = self._image_path.read_bytes()
        result = asyncio.get_event_loop().run_until_complete(
            analyze_image(image_bytes, ducats)
        )
        assert isinstance(result, AnalyzeResult)
        assert result.totals.items_matched > 0, (
            f"No Prime parts matched. items_detected={result.totals.items_detected}. "
            "Signals normalization mismatch or threshold too strict."
        )

    def test_items_matched_at_least_ten_after_grouping(self) -> None:
        """After bbox grouping, expect >= 10 matched Prime parts from image.png.

        The pre-grouping single-detection approach yielded 1/57.  Spatial
        pairing should recover the compound keys (e.g. 'wisp prime blueprint')
        and raise matches substantially.  If this assertion fails, the grouping
        thresholds need tuning — halt and report bbox samples rather than
        lowering this threshold.
        """
        ducats = self._get_ducats()
        image_bytes = self._image_path.read_bytes()
        result = asyncio.get_event_loop().run_until_complete(
            analyze_image(image_bytes, ducats)
        )
        assert result.totals.items_matched >= 10, (
            f"Grouping fix underperformed: items_matched={result.totals.items_matched}, "
            f"items_detected={result.totals.items_detected}. "
            "Spatial thresholds likely need tuning. Halt and report bbox samples."
        )

    def test_schema_shape(self) -> None:
        """Returned AnalyzeResult must conform to the API contract schema."""
        ducats = self._get_ducats()
        image_bytes = self._image_path.read_bytes()
        result = asyncio.get_event_loop().run_until_complete(
            analyze_image(image_bytes, ducats)
        )

        assert isinstance(result.items, list)
        assert isinstance(result.totals, Totals)
        assert result.totals.items_detected >= result.totals.items_matched
        assert result.totals.ducats_sum == sum(item.ducats for item in result.items)

        for item in result.items:
            assert isinstance(item, ItemResult)
            assert isinstance(item.name, str) and item.name
            assert isinstance(item.ducats, int) and item.ducats > 0
            assert item.recommendation in {
                "high-value sell",
                "mid-value consider",
                "low-value keep",
            }

    def test_ducats_sum_matches_items(self) -> None:
        """Totals.ducats_sum must equal the sum of individual item ducat values."""
        ducats = self._get_ducats()
        image_bytes = self._image_path.read_bytes()
        result = asyncio.get_event_loop().run_until_complete(
            analyze_image(image_bytes, ducats)
        )
        assert result.totals.ducats_sum == sum(item.ducats for item in result.items)
