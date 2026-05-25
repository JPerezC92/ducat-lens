"""FastAPI application entry point for ducat-lens backend."""

import logging

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .analyze import AnalyzeResult, analyze_image
from .ducats import load_ducats

logger = logging.getLogger(__name__)

# Load the ducat lookup table once at app boot.
# If the data file is missing, refuse to start rather than serve broken responses.
try:
    _DUCATS: dict[str, int] = load_ducats()
except FileNotFoundError as exc:
    logger.error("Failed to load data/ducats.json at boot: %s", exc)
    raise

app = FastAPI(title="ducat-lens")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResult)
async def analyze(image: UploadFile = File(...)) -> AnalyzeResult:
    """Accept a PNG or JPEG screenshot, run OCR, and return matched Prime parts."""
    if image.content_type not in {"image/png", "image/jpeg"}:
        raise HTTPException(status_code=400, detail="Image must be PNG or JPEG")

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image upload")

    result = await analyze_image(image_bytes, _DUCATS)

    if result.totals.items_matched == 0:
        raise HTTPException(
            status_code=422, detail="No recognizable Prime parts detected"
        )

    return result
