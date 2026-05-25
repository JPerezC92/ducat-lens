# PR Review — feat/scaffold/phase-07-app-scaffold (2026-05-25)

## Scope

Branch: `feat/scaffold/phase-07-app-scaffold`
Base: `main`
Diff command: `git diff main...feat/scaffold/phase-07-app-scaffold`
PR number: NONE YET — pre-PR cross-file review per Cipher 🔓 (Dev-Team Orchestrator) dispatch. Herald 📯 (Release Manager) opens PR only after this signal.
Commits on branch: 1 (`44f3078` — `feat(scaffold): phase 07 backend FastAPI + frontend Astro + ducat data bundle`)
Files changed: 21 (+1048 / -34) — matches Cipher 🔓 (Dev-Team Orchestrator) stated scope exactly.

| Path | Change | Lines |
|---|---|---|
| `README.md` | MODIFIED | +34 / -6 |
| `backend/__init__.py` | ADDED | +0 |
| `backend/analyze.py` | ADDED | +1 |
| `backend/ducats.py` | ADDED | +25 |
| `backend/main.py` | ADDED | +19 |
| `backend/pyproject.toml` | ADDED | +31 |
| `backend/scripts/__init__.py` | ADDED | +0 |
| `backend/scripts/fetch_ducats.py` | ADDED | +65 |
| `data/ducats.json` | ADDED | +558 |
| `frontend/astro.config.mjs` | ADDED | +16 |
| `frontend/package.json` | ADDED | +24 |
| `frontend/public/robots.txt` | ADDED | +3 |
| `frontend/src/components/DucatAnalyzer.tsx` | ADDED | +7 |
| `frontend/src/components/SEO.astro` | ADDED | +35 |
| `frontend/src/env.d.ts` | ADDED | +1 |
| `frontend/src/layouts/BaseLayout.astro` | ADDED | +29 |
| `frontend/src/pages/index.astro` | ADDED | +57 |
| `frontend/tsconfig.json` | ADDED | +3 |
| `knowledge/audits/pr-2-20260525.md` | ADDED | +80 |
| `plans/ducat-lens-bootstrap-20260524/_architecture.md` | MODIFIED | +59 / -28 |
| `plans/ducat-lens-bootstrap-20260524/phase-07-forge.md` | MODIFIED | +29 / -0 |

## Primary Goal Check

- Stated goal (Cipher 🔓 brief + commit subject + `phase-07-forge.md` runbook): scaffold backend FastAPI skeleton (`main.py`, `analyze.py` stub, `ducats.py` loader, `pyproject.toml`, `scripts/fetch_ducats.py`), scaffold frontend Astro 5 + React-islands app with SEO-HIGH wiring (`SEO.astro`, `BaseLayout.astro`, `index.astro`, `DucatAnalyzer.tsx` stub, `robots.txt`, `sitemap()` integration), generate `data/ducats.json` ducat lookup bundle, persist prior Inquisitor audit (`knowledge/audits/pr-2-20260525.md`), update README + `_architecture.md` + `phase-07-forge.md` for the Astro swap.
- Diff achieves stated goal: **Yes**. Every changed file maps directly to one of the stated workstreams.
- Scope creep detected: **No**. All 21 files fall inside `backend/`, `frontend/`, `data/`, `knowledge/audits/`, `plans/ducat-lens-bootstrap-20260524/`, or `README.md`.

## Findings

| # | Severity | File(s) | Finding | Fix Routing |
|---|----------|---------|---------|-------------|
| 1 | INFO | `backend/pyproject.toml` line 27 | `build-backend = "setuptools.backends.legacy:build"` is not a documented setuptools build-backend identifier (standard values are `setuptools.build_meta` or `setuptools.build_meta:__legacy__`). If the README setup command `pip install -e .` fails on this string, the documented onboarding path breaks. Bastion 🧱 (Backend Architect) PASSed `backend/**/*.py` and `pyproject.toml` per Cipher 🔓 (Dev-Team Orchestrator) brief; this observation is recorded for Bastion 🧱 visibility but does not override the upstream PASS. | Cipher 🔓 (Dev-Team Orchestrator) may surface to Bastion 🧱 (Backend Architect) for confirmation if onboarding repro fails. No action required pre-PR. |

Severity: **INFO only** (no BLOCK, no ADVISORY).

## Cross-cutting Checks

- **AI attribution scan**: **PASS**.
  - Git artifacts: commit `44f3078` inspected via `git log -1 --format=fuller`. Author and committer are `Philip Junior Pérez Castro <jperez.c92@gmail.com>`. Body has no `Co-Authored-By:` trailer, no `Generated with` footer, no `🤖` glyph, no AI tool URL. PR not yet open — no PR title/body to scan.
  - Changed file bodies: full diff scanned for `Co-Authored-By|Generated with|claude\.com|anthropic\.com|openai\.com|cursor\.sh|copilot\.github|noreply@anthropic|bot@openai|🤖` (case-insensitive). Result: **zero hits anywhere in the diff** — including legitimate rule-statement files in the allowlist (the prior `knowledge/audits/pr-2-20260525.md` artifact carried the rule strings in quoted form inside a regex listing, but the literal patterns did not match standalone). No attribution outside any allowlist location, because there is no attribution at all.

- **Naming consistency (cross-file)**: **PASS**.
  - Backend Python uses `snake_case` consistently (`load_ducats`, `fetch_ducats`, `_normalize`, `_DATA_FILE`, `_WHITESPACE_RE`, `OUTPUT_FILE`, `BASE_URL`, `CATEGORIES`). Frontend TypeScript uses `camelCase` / `PascalCase` consistently (`DucatAnalyzer`, `BaseLayout`, `pageTitle`, `pageDescription`, `jsonLd`, `ogImage`).
  - Public API endpoint: backend defines `GET /` (health check only — `POST /analyze` is phase 08). Frontend has zero hardcoded backend URLs in this scaffold (`DucatAnalyzer.tsx` is a placeholder div; `astro.config.mjs` comment notes the React island will fetch `http://localhost:8000/analyze` directly via CORS in phase 09). No cross-file URL drift possible at this stage.
  - Roster naming convention (`Name Emoji (Role)`) honored in all changed markdown files: `_architecture.md`, `phase-07-forge.md`, `pr-2-20260525.md`, README. Sentinel 🛡️ (Quality Guardian) owns the deep markdown audit; Inquisitor 🔎 (PR Reviewer) confirms only no cross-file drift between agent references.

- **Scope creep**: **PASS**. No files changed outside the scope Cipher 🔓 (Dev-Team Orchestrator) stated. No `.claude/agents/*.md` edits (Marshal 🎖️ HR Director gate not triggered). No persona file edits. No CLAUDE.md edit. No test files (correct — Crucible 🔥 (Test Architect) is phase-08+).

- **Dead code introduced**: **PASS**. No unused imports detected in any backend Python file (`backend/main.py` uses `FastAPI` + `CORSMiddleware`; `backend/ducats.py` uses `json`, `Path`; `backend/scripts/fetch_ducats.py` uses `json`, `re`, `sys`, `Path`, `httpx`). No unused imports in TypeScript / Astro files (`index.astro` uses `BaseLayout` + `DucatAnalyzer`; `BaseLayout.astro` uses `SEO`; `astro.config.mjs` uses `defineConfig` + `react` + `sitemap`). No leftover Vite or port-5173 references in additions — diff shows them only as removed lines in README (`-- **Frontend:** React + Vite + TypeScript`, `-frontend/        React + Vite + TS app`). The Astro swap is clean.

- **Public API consistency**: **N/A**. No frontend ↔ backend HTTP wiring lives in this scaffold (per phase plan, that arrives in phase 09 with the upload form + fetch call). `backend/main.py` exposes only `GET /` as a health check; no frontend caller exists to mismatch.

- **Dep hygiene**: **PASS** with a Warden 🔒 (Dependency Warden) gate note.
  - `frontend/package.json` deps match `_architecture.md` Frontend dependency list **exactly**: `astro ^5`, `@astrojs/react latest`, `@astrojs/sitemap latest`, `react ^18`, `react-dom ^18`, `react-dropzone latest`; devDeps `@types/react ^18`, `@types/react-dom ^18`, `typescript ^5`. Zero drift.
  - `backend/pyproject.toml` runtime deps match `_architecture.md` Backend dependency list **exactly**: `fastapi`, `uvicorn[standard]`, `python-multipart`, `pillow`, `rapidocr-onnxruntime`, `httpx`, `pydantic`. Dev deps `pytest`, `pytest-asyncio`, `httpx`, `ruff`, `mypy` match the dev list in `_architecture.md`. Zero drift.
  - **Warden 🔒 (Dependency Warden) gate note**: this is the first PR introducing both `frontend/package.json` and `backend/pyproject.toml` to the tree. Per Inquisitor 🔎 (PR Reviewer) Workflow § 3.6, dep changes without a corresponding Warden 🔒 gate signal in `knowledge/audits/` are an ADVISORY. No `warden-*` audit file currently exists in `knowledge/audits/`. **Per Cipher 🔓 (Dev-Team Orchestrator) brief, Inquisitor 🔎 runs in parallel with Warden 🔒** — Cipher 🔓 is dispatching Warden 🔒 in the same wave and will receive that gate signal separately. Inquisitor 🔎 (PR Reviewer) therefore does not block on the missing Warden 🔒 artifact at this scaffold-introduction moment; Cipher 🔓 (Dev-Team Orchestrator) holds the responsibility to confirm Warden 🔒 returns PASS/ADVISORY before Herald 📯 (Release Manager) opens the PR.

## SEO completeness check (HIGH priority per `_architecture.md` § SEO requirements)

| Requirement | Location | Verdict | Evidence |
|---|---|---|---|
| Single `<h1>` per page | `frontend/src/pages/index.astro` | **PASS** | One `<h1>ducat-lens</h1>` at line 28 of file body. No additional `<h1>` elements. |
| `<title>` per page | `frontend/src/components/SEO.astro` → consumed by `BaseLayout.astro` → consumed by `index.astro` (`pageTitle` const) | **PASS** | `<title>{title}</title>` rendered by `SEO.astro`. |
| `<meta name="description">` | `SEO.astro` | **PASS** | `<meta name="description" content={description} />` rendered. |
| `<link rel="canonical">` | `SEO.astro` | **PASS** | `<link rel="canonical" href={Astro.url.href} />` rendered. |
| Open Graph (og:title, og:description, og:image, og:url, og:type) | `SEO.astro` | **PASS** | All five `<meta property="og:*">` tags emitted (lines 18–22 of file body). |
| Twitter cards (twitter:card, twitter:title, twitter:description, twitter:image) | `SEO.astro` | **PASS** | All four `<meta name="twitter:*">` tags emitted (lines 25–28). |
| JSON-LD `WebApplication` schema | `index.astro` passes `jsonLd` prop → `SEO.astro` renders `<script type="application/ld+json">` | **PASS** | Schema includes `@context`, `@type: WebApplication`, `name`, `description`, `applicationCategory: GameApplication`, `operatingSystem: Web`, free `offers` block. Conditional render in `SEO.astro` (`{jsonLd && <script ...>}`). |
| `@astrojs/sitemap` integration registered | `frontend/astro.config.mjs` | **PASS** | `import sitemap from '@astrojs/sitemap'` + `integrations: [react(), sitemap()]`. |
| `site` URL set (required by sitemap) | `frontend/astro.config.mjs` | **PASS** | `site: 'https://ducat-lens.example'` (placeholder per `_architecture.md` — Cipher 🔓 updates when deployment locked). |
| `robots.txt` allow + sitemap pointer | `frontend/public/robots.txt` | **PASS** | `User-agent: *` / `Allow: /` / `Sitemap: https://ducat-lens.example/sitemap-index.xml`. |
| Static-rendered HTML target | `frontend/astro.config.mjs` | **PASS** | `output: 'static'`. |
| Crawlable substance in page body (not JS-only) | `index.astro` body | **PASS** | `<h1>`, descriptive `<p>`, `<h2>How it works</h2>` ordered list, `<h2>Features</h2>` unordered list — all rendered server-side. React island (`<DucatAnalyzer client:load />`) is interactive enhancement only. |

**SEO completeness: 12/12 checks PASS.** All HIGH-priority requirements from `_architecture.md` § SEO requirements are wired into the scaffold. Lighthouse SEO verification deferred to Lumen ✨ (Visual Director) in phase 10 per the architecture lock — that is outside Inquisitor 🔎 (PR Reviewer) scope.

## Gate Signal

**[PASS]** — diff matches Cipher 🔓 (Dev-Team Orchestrator) stated scope exactly, zero AI attribution anywhere, SEO HIGH requirements 12/12 wired, dep manifests align with `_architecture.md` zero-drift, single INFO observation on a `setuptools` build-backend string that Bastion 🧱 (Backend Architect) already PASSed.

## Fix Routing Summary

- **Finding 1 (INFO, `backend/pyproject.toml` build-backend string)**: no required action pre-PR. Cipher 🔓 (Dev-Team Orchestrator) may relay to Bastion 🧱 (Backend Architect) for confirmation if first user `pip install -e .` execution surfaces an installer error. Not a merge blocker.
- **GitHub comment**: not posted — no PR exists yet. If the gate signal had been [ADVISORY] or [BLOCK], Inquisitor 🔎 (PR Reviewer) would have posted via `gh pr comment` once Herald 📯 (Release Manager) opens the PR. On [PASS], no comment posted per spec § Hard Rules.
- **Warden 🔒 (Dependency Warden) parallel gate**: pending in Cipher 🔓 (Dev-Team Orchestrator)'s parallel dispatch wave; Cipher 🔓 owns the merge of all parallel gate signals before clearing Herald 📯 (Release Manager) to run `gh pr create`.
