# Phase 01 — Source images + write CSS filter + edit landing page

## Owner

Forge 🔨 (Implementation Agent) → Atrium 🏛️ (Frontend Architect) auto-gate

## Pre

- Working branch synced with `origin/main` per CLAUDE.md § Pre-coding sync gate
- `frontend/public/` exists (verified — contains `logo.svg` + `robots.txt`)
- Repo root `image.png` exists (verified — 756×607, 692 KB)
- `backend/` `uv sync` env populated (Pillow available)
- Hero source verified live: `https://cdn.warframestat.us/img/LokiPrime.png` (512×512, 97 KB)

## Reads

- `frontend/src/pages/index.astro` — landing page to edit
- `frontend/src/styles/global.css` — add `.crt-duotone`
- `image.png` — repo-root Ducat Kiosk source
- `plans/add-website-images-20260527/plan.md` — scope + decisions
- `plans/add-website-images-20260527/_crt-snippets.md` — verbatim CSS + Astro + Pillow blocks

## Writes

- `frontend/public/images/hero-prime.png` — copy of WFCD hero PNG (alpha preserved)
- `frontend/public/images/example-kiosk.jpg` — re-encoded from `image.png` (JPEG quality 82, ≤ 500 KB)
- `frontend/src/styles/global.css` — `.crt-duotone` utility appended inside `@layer utilities`
- `frontend/src/pages/index.astro` — two `<figure class="crt-duotone">` blocks inserted

## Steps

1. Pick hero `imageName`. Default `LokiPrime.png` per plan Resolved decisions. User override goes in plan Pending.
2. Download hero to repo root temp: `curl -sL -o _tmp-hero.png -w "HTTP:%{http_code} BYTES:%{size_download}\n" "https://cdn.warframestat.us/img/LokiPrime.png"`. Expect `HTTP:200` and `BYTES:97000`±5000.
3. Run Snippet D (`_crt-snippets.md`) from repo root. Produces `frontend/public/images/hero-prime.png` + `frontend/public/images/example-kiosk.jpg`. Captures dimensions to stdout — record both.
4. Delete `_tmp-hero.png` from repo root: `rm _tmp-hero.png`.
5. Append Snippet A from `_crt-snippets.md` to `frontend/src/styles/global.css` inside the existing `@layer utilities` block (after `.animate-scan-sweep`).
6. Edit `frontend/src/pages/index.astro`:
   - Insert Snippet B (`<figure>` hero) above existing `<div class="flex items-center gap-4">` H1 row. Substitute `W`/`H` with step 3 hero dimensions.
   - Insert Snippet C (`<figure>` example) at end of the `<li>Upload a screenshot of your Warframe Ducat Kiosk inventory.</li>`. Substitute `W2`/`H2` with step 3 example dimensions. Set `src="/images/example-kiosk.jpg"` per Snippet D format note.
7. Build: `cd frontend && pnpm build`. Exit 0 required. No missing-asset warnings. (Browser smoke happens in phase 02 under Lumen ✨ (Visual Director) via Atrium-launched server — Forge does NOT run `pnpm dev` per CLAUDE.md Bash registry which scopes that grant to Atrium 🏛️ (Frontend Architect).)

## Output

- `frontend/public/images/hero-prime.png` — PNG with alpha, ≤ 300 KB (97 KB expected)
- `frontend/public/images/example-kiosk.jpg` — JPEG q82, ≤ 500 KB
- `frontend/src/styles/global.css` — Snippet A appended verbatim
- `frontend/src/pages/index.astro` — Snippets B + C inserted

## Gate

- `cd frontend && pnpm build` exits 0
- Atrium 🏛️ (Frontend Architect) auto-gate PASS on edited `.astro` + `global.css`
- Both `<img>` tags carry non-empty `alt`, `width`, `height`
- Hero has `loading="eager"` + `fetchpriority="high"`; example has `loading="lazy"` + `decoding="async"`
- No new entries in `frontend/package.json` `dependencies` or `devDependencies`
- No backend file touched
- No file left at repo root (no `_tmp-hero.png`)

## Abort conditions

- WFCD CDN HTTP non-200 → halt, return to Cipher 🔓 (Dev-Team Orchestrator); pick alternate
- Pillow re-encode of example > 500 KB at q82 → halt, return to Cipher 🔓; consider q70 or scale to 640px wide
- `pnpm build` fails → halt with log
- Atrium 🏛️ (Frontend Architect) FAIL → halt, route fix to Forge 🔨 (Implementation Agent); do not advance to phase 02

## MCP whitelist/blacklist

- Allowed: none required (Forge uses Bash + Edit + Write only)
- Forbidden: `chrome-devtools` (reserved for Lumen ✨ (Visual Director) in phase 02)
