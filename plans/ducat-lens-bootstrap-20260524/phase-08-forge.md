# Phase 08 — Backend pipeline: image upload → OCR → ducat lookup → recommend

## Owner

Forge 🔨 (Implementation Agent)

## Pre

- Phase 07 complete: backend scaffold + `data/ducats.json` (556 entries) shipped on main (PR #3 merged 2026-05-25)
- Pre-Forge sync gate passed: `git rev-list HEAD..origin/main --count` = 0
- New feature branch created by Herald 📯 (Release Manager) before Forge starts
- `image.png` test fixture present at repo root
- `rapidocr-onnxruntime` already installed via `backend/pyproject.toml` dep list (phase 07 verified `pip install -e .`)

## Reads

- `plans/ducat-lens-bootstrap-20260524/_architecture.md` — API contract (Endpoint, Request, Response, 4xx, Recommendation thresholds) + Vision pipeline section (preprocessing intent: HSV crop, normalize, per-card OCR)
- `plans/ducat-lens-bootstrap-20260524/_research-vision.md` — RapidOCR sample stub
- `backend/main.py` — current FastAPI app skeleton (GET / placeholder route)
- `backend/analyze.py` — current empty stub (replace with pipeline)
- `backend/ducats.py` — `load_ducats()` loader returning `dict[str, int]`
- `data/ducats.json` — generated lookup table
- `image.png` — test fixture for OCR end-to-end verification

## Writes

### `backend/analyze.py` (replace stub with full pipeline)

Module exports:
- `normalize(text: str) -> str` — lowercase, strip punctuation, collapse whitespace to single space, strip leading/trailing. Pure function. Unit-testable.
- `recommend(ducats: int) -> str` — threshold logic per `_architecture.md`: `>= 65` → `"high-value sell"`, `25 | 45` → `"mid-value consider"`, `<= 15` → `"low-value keep"`. Pure function. Unit-testable.
- `class AnalyzeResult(pydantic.BaseModel)`: `items: list[ItemResult]`, `totals: Totals`
- `class ItemResult(pydantic.BaseModel)`: `name: str`, `ducats: int`, `recommendation: str`
- `class Totals(pydantic.BaseModel)`: `items_detected: int`, `items_matched: int`, `ducats_sum: int`
- `async def analyze_image(image_bytes: bytes, ducat_lookup: dict[str, int]) -> AnalyzeResult` — main pipeline. Steps:
  1. Decode image bytes to PIL Image (`PIL.Image.open(io.BytesIO(image_bytes))`)
  2. Convert to RGB if not already
  3. Pass image bytes (or PIL → bytes via BytesIO) to RapidOCR via `from rapidocr_onnxruntime import RapidOCR; engine = RapidOCR()` (module-level engine cached so model loads once)
  4. RapidOCR returns list of `(bbox, text, confidence)` tuples
  5. Filter: keep only text with confidence > 0.5 AND length >= 3
  6. For each OCR'd text: `normalized = normalize(text)`. If `normalized` contains `"prime"` (case-insensitive match on normalized string), attempt lookup in `ducat_lookup`. Treat lookup miss as "detected but not matched".
  7. Build `ItemResult` per matched item. Aggregate `totals`.
  8. Return `AnalyzeResult`.
- Module-level: `_engine: RapidOCR | None = None` and `def _get_engine() -> RapidOCR` lazy initializer (avoid loading ONNX model at module import — slows app boot).

### `backend/main.py` (add `/analyze` endpoint)

- Import: `from fastapi import FastAPI, File, HTTPException, UploadFile` (extend existing imports)
- Import: `from backend.analyze import analyze_image, AnalyzeResult`
- Import: `from backend.ducats import load_ducats`
- Module-level: `_DUCATS: dict[str, int] = load_ducats()` — load once at app boot. Wrap in try/except FileNotFoundError; if file missing, log and raise (app should refuse to boot rather than serve broken responses).
- Add route:
  ```python
  @app.post("/analyze", response_model=AnalyzeResult)
  async def analyze(image: UploadFile = File(...)) -> AnalyzeResult:
      if image.content_type not in {"image/png", "image/jpeg"}:
          raise HTTPException(status_code=400, detail="Image must be PNG or JPEG")
      image_bytes = await image.read()
      if not image_bytes:
          raise HTTPException(status_code=400, detail="Empty image upload")
      result = await analyze_image(image_bytes, _DUCATS)
      if result.totals.items_matched == 0:
          raise HTTPException(status_code=422, detail="No recognizable Prime parts detected")
      return result
  ```
- Keep existing `GET /` health route untouched.

### `backend/tests/__init__.py` — empty package marker

### `backend/tests/test_analyze.py` — unit + integration tests

Test pyramid per Crucible 🔥 (Test Architect) discipline. Three classes:

```python
class TestNormalize:
    # mixed-case input, punctuation, multiple spaces, leading/trailing — verify output
    # empty string, whitespace-only — verify graceful handling

class TestRecommend:
    # ducats=100 → "high-value sell"
    # ducats=65 → "high-value sell"
    # ducats=45 → "mid-value consider"
    # ducats=25 → "mid-value consider"
    # ducats=15 → "low-value keep"
    # boundary checks: 64, 26, 16

class TestAnalyzeImage:
    # Integration: load image.png, call analyze_image with real ducat dict, assert items_matched > 0
    # Verify schema: returned AnalyzeResult matches API contract
    # Mark slow: pytest.mark.slow (RapidOCR model load + inference takes 1-3s on first run)
```

### `backend/tests/test_api.py` — FastAPI integration

```python
class TestAnalyzeEndpoint:
    # Use httpx AsyncClient or fastapi.testclient.TestClient with image.png
    # POST /analyze with valid PNG → 200 + valid JSON shape
    # POST /analyze with text/plain content-type → 400
    # POST /analyze with empty file → 400
    # POST /analyze with PNG containing no Prime parts (use a tiny blank PNG fixture) → 422
    # GET /analyze (wrong method) → 405 (FastAPI default)
```

### Update `_architecture.md` confidence threshold note

Add a one-liner to the Vision pipeline section: `OCR confidence threshold = 0.5 (locked phase 08)`.

## Steps

1. **Confirm pre-state**: read all listed files. If anything is ambiguous about the API contract or pipeline, halt and ask Cipher 🔓 (Dev-Team Orchestrator).
2. **Write `backend/analyze.py`** — full pipeline per Writes spec. Lazy-load the RapidOCR engine. Pure helper functions (`normalize`, `recommend`) before the pipeline function.
3. **Write `backend/tests/test_analyze.py`** unit tests for `normalize` + `recommend` (Crucible 🔥 expects ≥1 unit per critical fn).
4. **Write `backend/main.py`** updates — add `/analyze` route + module-level ducat dict load.
5. **Write `backend/tests/__init__.py`** + **`backend/tests/test_api.py`** integration tests.
6. **Run tests locally**: `cd backend && pip install -e ".[dev]" && pytest tests/ -v` (this installs pytest + pytest-asyncio). Verify all pass. Note: `TestAnalyzeImage` integration test may take 5-10s on first run (RapidOCR model download + ONNX session init). If model download required, document in README that first run is slow.
7. **Smoke test the endpoint manually**: `uvicorn backend.main:app --port 8000 &; curl -s -X POST -F "image=@image.png" http://localhost:8000/analyze | jq` → expect JSON with detected Prime parts. Capture output + include in dispatch report.
8. **Update `_architecture.md`** with confidence threshold note (1 line).
9. **Report back to Cipher 🔓** with file list, test results (passed count + any skipped), and a sample curl response showing detected items.

## Output

- `backend/analyze.py` ~150-200 LOC with full pipeline + helpers
- `backend/main.py` extended with `/analyze` route + module-level ducat dict
- `backend/tests/__init__.py` + `backend/tests/test_analyze.py` + `backend/tests/test_api.py` with passing tests
- `_architecture.md` updated with confidence threshold lock
- `pytest tests/` exits 0
- Manual curl test returns valid JSON with ≥ 1 matched Prime part from `image.png`
- Zero AI attribution in any file

## Gate

- Bastion 🧱 (Backend Architect) audits all `backend/*.py` — returns `[PASS]`
- Crucible 🔥 (Test Architect) audits `backend/tests/*.py` — returns `[PASS]` on test pyramid (≥1 unit per pure function, ≥1 integration per endpoint, fixture isolation, no shared mutable state)
- Inquisitor 🔎 (PR Reviewer) cross-file pre-PR — returns `[PASS]` or `[ADVISORY]`
- Warden 🔒 (Dependency Warden) — no new deps expected this phase (rapidocr-onnxruntime already shipped phase 07); if any new dep added, Warden gate runs
- Manual `curl -F image=@image.png http://localhost:8000/analyze` returns 200 + items_matched > 0

## Abort conditions

- RapidOCR returns zero text from `image.png` — halt, dump OCR raw output, report to Cipher (signals OCR engine issue OR `image.png` doesn't have crawlable text)
- RapidOCR import fails at runtime despite phase 07 install — halt, report import error
- `_DUCATS` dict load fails at app boot — halt, report error path (likely `data/ducats.json` not in expected location)
- Test integration on `image.png` returns items_matched == 0 — halt, report which Prime-part text RapidOCR DID detect; signals normalization mismatch or threshold too strict
- Any test in `backend/tests/` fails — halt, do NOT proceed to Herald PR until green

## MCP whitelist/blacklist

- Allowed: `context7` for RapidOCR / FastAPI / Pillow API spot-checks
- Forbidden: `chrome-devtools` (no live UI testing this phase — phase 09 wires the frontend)
