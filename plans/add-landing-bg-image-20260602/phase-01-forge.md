# Phase 01 — Download bg image + write CSS + build

## Owner

Forge 🔨 (Implementation Agent) → Atrium 🏛️ (Frontend Architect) auto-gate

## Pre

- On branch `feat/frontend/add-crt-image-figures`, synced with remote: `git fetch origin && git rev-list HEAD..origin/feat/frontend/add-crt-image-figures --count` must return `0`
- `frontend/public/images/` exists (already contains hero-prime.png + example-kiosk.jpg)
- WFCD CDN accessible: `https://cdn.warframestat.us/img/MagPrime.png`

## Reads

- `frontend/src/styles/global.css` — insert `body::before` block in `@layer base`
- `plans/add-landing-bg-image-20260602/plan.md` — image strategy + filter values

## Writes

- `frontend/public/images/bg-warframe.png` — downloaded MagPrime render
- `frontend/src/styles/global.css` — `body::before` block inserted in `@layer base`, after existing `body {}` rule

## Steps

1. Download bg image to output path:
   ```
   curl -sL -o frontend/public/images/bg-warframe.png -w "HTTP:%{http_code} BYTES:%{size_download}\n" "https://cdn.warframestat.us/img/MagPrime.png"
   ```
   Expect `HTTP:200`. File must be ≤ 300 KB.

2. Edit `frontend/src/styles/global.css`: inside `@layer base`, immediately after the closing `}` of the existing `body { }` rule, insert:

   ```css
   body::before {
     content: "";
     position: fixed;
     inset: 0;
     z-index: -1;
     background-image: url("/images/bg-warframe.png");
     background-size: cover;
     background-position: center;
     filter: grayscale(1) sepia(1) hue-rotate(160deg) brightness(0.12) saturate(3) contrast(1.5);
     pointer-events: none;
   }
   @media (max-width: 767px) {
     body::before { display: none; }
   }
   ```

3. Build: `cd frontend && pnpm build`. Exit 0 required. No missing-asset warnings.

## Output

- `frontend/public/images/bg-warframe.png` — PNG ≤ 300 KB
- `frontend/src/styles/global.css` — `body::before` block appended

## Gate

- `frontend/public/images/bg-warframe.png` exists, ≤ 300 KB
- `body::before` block present in `global.css` inside `@layer base`, with all required properties: `position: fixed`, `inset: 0`, `z-index: -1`, `background-size: cover`, full filter chain (no `mix-blend-mode`), `@media (max-width: 767px)` hide rule
- `pnpm build` exits 0
- Atrium 🏛️ (Frontend Architect) auto-gate PASS on `global.css`
- No changes to `frontend/package.json` dependencies

## Abort conditions

- WFCD CDN HTTP non-200 → try `RhinoPrime.png` fallback; if also fails halt and return to Cipher 🔓 (Dev-Team Orchestrator)
- File size > 300 KB → halt; Forge does NOT resize (no Pillow step planned); return to Cipher 🔓 for resolution
- `pnpm build` fails → halt with log
- Atrium 🏛️ (Frontend Architect) FAIL → halt, route fix back to Forge 🔨 (Implementation Agent); do not advance to phase 02

## MCP whitelist/blacklist

- Allowed: none required (Bash + Edit + Write only)
- Forbidden: `chrome-devtools` (reserved for Lumen ✨ in phase 02)
