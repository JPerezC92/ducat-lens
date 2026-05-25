# ducat-lens

Warframe Ducat Kiosk inventory analyzer. Upload a Ducat Kiosk screenshot → app detects Prime parts → returns ducat values + sell recommendations.

## Stack

- **Frontend:** Astro 5 + React islands + TypeScript — SEO-first, static-rendered crawlable HTML
- **Backend:** FastAPI (Python)
- **Vision:** RapidOCR (ONNX, always-free, no API key)
- **Data:** WFCD/warframe-items (MIT JSON, build-time bundled), warframe.market v1 fallback

## Status

Bootstrap phase. See `plans/ducat-lens-bootstrap-20260524/plan.md` for active work.

## Project layout

```
frontend/        Astro + React islands + TS app  (TBD — phase 07)
backend/         FastAPI Python app
data/            Ducat values JSON bundle
plans/           Plan artifacts (subfolder pattern)
knowledge/       Audits + design briefs + research outputs
.claude/         Agent specs + skills
agents/          Persona CV files
image.png        Test fixture (Ducat Kiosk screenshot)
```

See `CLAUDE.md` for orchestration model + agent roster.

## Setup

**Frontend** (Astro dev server on port 4321):
```
cd frontend && pnpm install && pnpm dev
```

**Frontend static build** (SEO crawlable HTML output to `frontend/dist/`):
```
cd frontend && pnpm build
```

**Backend** (FastAPI on port 8000):
```
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -e .
```

**Ducat data bundle** (one-time fetch, re-run after Warframe updates):
```
python -m backend.scripts.fetch_ducats
```

**Run the backend server:**
```
uvicorn backend.main:app --reload
```
