# Architecture lock — ducat-lens

> Status: locked (revised 2026-05-25 for SEO + Astro swap)
> Locked on: 2026-05-25
> Revised: 2026-05-25 — frontend swap Vite+React → Astro+React-islands per user SEO HIGH priority
> Locked by: Cipher 🔓 (Dev-Team Orchestrator)
> Source plan: `plans/ducat-lens-bootstrap-20260524/plan.md` phase 03
> Source research: `_research-vision.md` + `_research-ducat-api.md`
> User decisions: vision=RapidOCR (always-free, no key); ducat source=WFCD/warframe-items; bundling=build-time; **SEO=HIGH (Google ranking target)**; **frontend=Astro with React islands**

---

## Stack picks (locked)

| Layer | Pick | Version target | Why |
|---|---|---|---|
| Backend language | Python | 3.11+ | RapidOCR + FastAPI both support; widely available |
| Backend framework | FastAPI | latest stable | Plan-locked; async support; OpenAPI auto-gen |
| Backend server | uvicorn | latest stable | Standard FastAPI server |
| Vision lib | **RapidOCR (ONNX)** | `rapidocr-onnxruntime` latest | Always free, no key, no signup; 0.21s/image CPU; ~30-80MB; same PP-OCR weights as PaddleOCR |
| Image handling | Pillow | latest | Decode upload + preprocess (HSV crop, contrast) |
| HTTP client (build-time fetch) | httpx (sync mode in script) | latest | Async-friendly, used by build script and any future runtime calls |
| Frontend framework | **Astro** | 5.x | SEO HIGH — static-first, React islands for interactivity |
| Frontend interactive runtime | React | 18 | Via `@astrojs/react` integration — islands only (upload form + results table) |
| Frontend language | TypeScript | 5.x | Astro supports TS natively |
| Frontend file upload UI | react-dropzone | latest | Used inside React island component |
| Frontend HTTP | fetch (native) | n/a | No axios — keep deps small |
| SEO meta | Astro `<head>` + reusable `SEO.astro` component | n/a | Per-page meta + Open Graph + Twitter cards |
| Sitemap | `@astrojs/sitemap` | latest | Auto-generated at build time |
| Structured data | JSON-LD in landing page `<head>` | n/a | `WebApplication` schema for Google rich results |
| Package manager (FE) | pnpm | latest | Plan-locked |
| Package manager (BE) | pip | bundled | Standard Python |

---

## Vision pipeline

**Pick: RapidOCR.** Per Augur's `_research-vision.md` § "PaddleOCR re-evaluation (2026-05-25)":
- PP-OCRv5 model weights via ONNX runtime — same accuracy as PaddleOCR (CER ~0.10)
- 0.21s/image CPU (vs PaddleOCR 4.85s, EasyOCR 0.66s)
- ~30MB wheel + ~80MB total env
- Apache 2.0, no auth, no external service per request

**Preprocessing (planned for phase 08):**
- HSV color-threshold crop to isolate white text on dark background (prior art: WFinfo)
- Crop per Prime-part card grid cell, run OCR per cell rather than full screenshot
- Normalize OCR output (lowercase, strip punctuation, collapse whitespace) before lookup

**Out of scope for MVP:** GPU mode, batch processing, OCR fallback to EasyOCR.

OCR confidence threshold = 0.5 (locked phase 08)

---

## Ducat data source

**Pick: WFCD/warframe-items static JSON, build-time bundle.** Per `_research-ducat-api.md`:
- Source: `https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/<Category>.json`
- Categories needed: `Warframes`, `Primary`, `Secondary`, `Melee`, `Companions`
- License: MIT — no ToS concerns
- Fields used per item component: `name`, `ducats` (or `primeSellingPrice` as backup field within same record)
- Auto-updated upstream per Warframe release

**Bundling pattern: build-time** (per user lock):
- Build script at `scripts/fetch_ducats.py` (or equivalent path under `backend/scripts/`) downloads all 5 category JSONs, filters Prime-only items, builds merged lookup dict, writes `data/ducats.json`
- Script is part of repo setup (documented in `README.md` install steps)
- App runtime reads `data/ducats.json` only — zero outbound HTTPS at request time
- Refresh strategy: re-run build script on Warframe release (manual or via README instructions); stale data is acceptable for MVP

**Lookup dict shape:**
```json
{
  "wisp prime blueprint": 100,
  "braton prime barrel": 15,
  "ash prime systems blueprint": 65
}
```
Key = normalized (lowercase, single-space) item name. Value = integer ducat amount.

---

## Repo layout (locked)

```
ducat-lens/
├── frontend/                    # Astro + React islands + TS app
│   ├── package.json
│   ├── astro.config.mjs         # Astro config: react + sitemap integrations, site URL
│   ├── tsconfig.json
│   ├── public/
│   │   └── robots.txt           # allow all crawlers, point to sitemap
│   └── src/
│       ├── pages/
│       │   └── index.astro      # Landing page (crawlable HTML + SEO meta + JSON-LD)
│       ├── layouts/
│       │   └── BaseLayout.astro # Shared shell
│       ├── components/
│       │   ├── SEO.astro        # Reusable head meta + OG + Twitter + JSON-LD
│       │   └── DucatAnalyzer.tsx # React island: upload + results (client:load)
│       └── env.d.ts             # Astro type defs
├── backend/                     # FastAPI Python app
│   ├── pyproject.toml           # or requirements.txt
│   ├── main.py                  # FastAPI app entry
│   ├── analyze.py               # OCR + lookup + recommend pipeline
│   ├── ducats.py                # data/ducats.json loader + lookup
│   └── scripts/
│       └── fetch_ducats.py      # build-time WFCD JSON fetch
├── data/
│   └── ducats.json              # generated by fetch_ducats.py
├── image.png                    # test fixture (Ducat Kiosk screenshot)
├── README.md
├── CLAUDE.md
├── .gitignore
├── .claude/                     # agent specs + skills
├── agents/                      # persona profiles
├── knowledge/                   # design/audits/research outputs
└── plans/                       # plan artifacts
```

---

## Backend dependency list (locked)

```
fastapi
uvicorn[standard]
python-multipart        # file upload support for FastAPI
pillow                  # image decode + preprocess
rapidocr-onnxruntime    # vision
httpx                   # build script only (and any future API fallback)
pydantic                # FastAPI default; explicit pin for response model
```

Dev deps (not runtime):
```
pytest
pytest-asyncio          # async FastAPI test support
httpx                   # also reused by TestClient
ruff                    # lint
mypy                    # type check (optional MVP)
```

---

## Frontend dependency list (locked)

```json
{
  "dependencies": {
    "astro": "^5",
    "@astrojs/react": "latest",
    "@astrojs/sitemap": "latest",
    "react": "^18",
    "react-dom": "^18",
    "react-dropzone": "latest"
  },
  "devDependencies": {
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "typescript": "^5"
  }
}
```

No CSS framework picked yet — defer to Lumen ✨ (Visual Director) brief in phase 09 (Lumen may recommend Tailwind, shadcn-style components, scoped Astro `<style>`, or CSS modules based on design intent).

---

## SEO requirements (locked — user priority HIGH, 2026-05-25)

- Landing page `/` MUST render crawlable HTML at build time. Astro static output target.
- Per-page `<title>` + `<meta name="description">` + Open Graph (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) + Twitter cards (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`).
- JSON-LD `WebApplication` schema in landing page `<head>` for Google rich results.
- `@astrojs/sitemap` integration auto-generates `sitemap-index.xml` at build.
- `public/robots.txt` — allow all crawlers, point to sitemap.
- `<link rel="canonical">` per page.
- Semantic HTML: single `<h1>` per page, structured headings, alt text on every `<img>`.
- Lighthouse SEO score target ≥ 95 (verified phase 10 by Lumen ✨ via `impeccable` skill).
- React islands (`DucatAnalyzer.tsx`) are interactive only — crawlable substance (title, description, how-to-use copy, screenshot preview) lives in `index.astro` body so crawlers see content without executing JS.
- Site URL placeholder for sitemap + canonical: `https://ducat-lens.example` — Cipher 🔓 updates to real domain when deployment locked (deferred — out of scope for MVP).

---

## API contract (locked)

**Endpoint:** `POST /analyze`

**Request:** `multipart/form-data` with field `image` (PNG/JPEG bytes)

**Response (200):**
```json
{
  "items": [
    {
      "name": "Wisp Prime Blueprint",
      "ducats": 100,
      "recommendation": "high-value sell"
    },
    {
      "name": "Braton Prime Barrel",
      "ducats": 15,
      "recommendation": "low-value keep"
    }
  ],
  "totals": {
    "items_detected": 12,
    "items_matched": 10,
    "ducats_sum": 540
  }
}
```

**Response (4xx):**
- `400` if no image attached or unreadable format
- `422` if OCR returns zero recognizable items
- `500` on OCR engine failure

Recommendation thresholds (initial — tunable in phase 08):
- `ducats >= 65` → `"high-value sell"`
- `ducats in {25, 45}` → `"mid-value consider"`
- `ducats <= 15` → `"low-value keep"`

Single endpoint for MVP. Future endpoints (out of scope): `/refresh-ducats`, `/health`, batch upload.

---

## Out of scope (re-confirmed)

- Auth, user accounts, history
- Platinum trade pricing
- Mobile / PWA
- CI/CD, deploy infra
- OCR fallback (Gemini, EasyOCR, PaddleOCR) — RapidOCR-only for MVP
- Real-time WFCD refresh — manual via `fetch_ducats.py`
- Image storage / caching
- Multi-image batch processing
- Localization (English only)
- Deploy domain lock (sitemap site URL placeholder until deployment phase)

---

## Phase progression unlocked

With architecture locked, the next dispatches (per `plans/ducat-lens-bootstrap-20260524/plan.md`):

- **Phase 07 — Forge 🔨 (Implementation Agent)**: scaffold `frontend/`, `backend/`, write `scripts/fetch_ducats.py`, populate `data/ducats.json`
- **Phase 08 — Forge 🔨 (Implementation Agent)**: implement `backend/analyze.py` + `POST /analyze` endpoint working on `image.png`
- **Phase 09 — Forge 🔨 (Implementation Agent)**: frontend upload UI + results table
- **Phase 10 — parallel audits**: Atrium 🏛️ (FE) + Bastion 🧱 (BE) + Crucible 🔥 (tests) + **Inquisitor 🔎 (PR Reviewer)** cross-file pre-PR

Inquisitor 🔎 (PR Reviewer) hired 2026-05-25 in parallel with this lock (Marshal 🎖️ wrote spec + persona; Sentinel 🛡️ audit PASS).
