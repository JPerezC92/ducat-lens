"""FastAPI endpoint integration tests for POST /analyze."""

from __future__ import annotations

import io
import struct
import zlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.main import app

# ---------------------------------------------------------------------------
# Test client (sync, no event loop management needed)
# ---------------------------------------------------------------------------

client = TestClient(app)

_REPO_ROOT = Path(__file__).parent.parent.parent
_IMAGE_PNG = _REPO_ROOT / "image.png"


def _make_blank_png(width: int = 4, height: int = 4) -> bytes:
    """Return a minimal valid PNG with no recognizable text (solid dark pixels)."""
    # PNG signature
    sig = b"\x89PNG\r\n\x1a\n"

    def _chunk(tag: bytes, data: bytes) -> bytes:
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return length + tag + data + crc

    # IHDR: width, height, bit depth=8, colour type=2 (RGB), compression=0, filter=0, interlace=0
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr = _chunk(b"IHDR", ihdr_data)

    # IDAT: rows of filter byte (0) + RGB pixels (all dark: 20, 20, 20)
    raw_rows = b""
    for _ in range(height):
        raw_rows += b"\x00" + b"\x14\x14\x14" * width
    compressed = zlib.compress(raw_rows)
    idat = _chunk(b"IDAT", compressed)

    iend = _chunk(b"IEND", b"")
    return sig + ihdr + idat + iend


# ---------------------------------------------------------------------------
# TestAnalyzeEndpoint
# ---------------------------------------------------------------------------


class TestAnalyzeEndpoint:
    def test_valid_png_returns_200_with_valid_shape(self) -> None:
        """POST /analyze with a real PNG fixture must return 200 + valid JSON shape."""
        assert _IMAGE_PNG.exists(), f"Test fixture missing: {_IMAGE_PNG}"
        with _IMAGE_PNG.open("rb") as fh:
            response = client.post(
                "/analyze",
                files={"image": ("image.png", fh, "image/png")},
            )
        assert response.status_code == 200
        body = response.json()
        assert "items" in body
        assert "totals" in body
        assert isinstance(body["items"], list)
        assert len(body["items"]) > 0
        totals = body["totals"]
        assert "items_detected" in totals
        assert "items_matched" in totals
        assert "ducats_sum" in totals
        # Each item must have the three required fields
        for item in body["items"]:
            assert "name" in item
            assert "ducats" in item
            assert "recommendation" in item

    def test_wrong_content_type_returns_400(self) -> None:
        """POST /analyze with text/plain content-type must return 400."""
        response = client.post(
            "/analyze",
            files={"image": ("file.txt", b"not an image", "text/plain")},
        )
        assert response.status_code == 400

    def test_empty_file_returns_400(self) -> None:
        """POST /analyze with an empty file body must return 400."""
        response = client.post(
            "/analyze",
            files={"image": ("empty.png", b"", "image/png")},
        )
        assert response.status_code == 400

    def test_blank_image_returns_422(self) -> None:
        """POST /analyze with a blank PNG (no Prime parts) must return 422."""
        blank_png = _make_blank_png()
        response = client.post(
            "/analyze",
            files={"image": ("blank.png", io.BytesIO(blank_png), "image/png")},
        )
        assert response.status_code == 422

    def test_wrong_method_returns_405(self) -> None:
        """GET /analyze must return 405 Method Not Allowed."""
        response = client.get("/analyze")
        assert response.status_code == 405
