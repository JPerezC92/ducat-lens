# ducat-lens

Warframe Ducat Kiosk inventory analyzer. Upload a Ducat Kiosk screenshot → app detects Prime parts → returns ducat values + sell recommendations.

## Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI (Python)
- **Vision:** Google Gemini 1.5 Flash (free tier) primary, EasyOCR fallback
- **Data:** WFCD/warframe-items (MIT JSON) primary, warframe.market v1 fallback

## Status

Bootstrap phase. See `plans/ducat-lens-bootstrap-20260524/plan.md` for active work.

## Project layout

```
frontend/        React + Vite + TS app          (TBD — phase 07)
backend/         FastAPI Python app             (TBD — phase 07)
data/            Ducat values JSON bundle       (TBD — phase 07)
plans/           Plan artifacts (subfolder pattern)
.claude/         Agent specs + skills
agents/          Persona CV files
image.png        Test fixture (Ducat Kiosk screenshot)
```

See `CLAUDE.md` for orchestration model + agent roster.
