# Phase 04: Wire Google Fonts in BaseLayout

## Owner

Forge 🔨 (Implementation Agent)

## Pre

- Phase 03 complete: deps installed

## Reads

- `frontend/src/layouts/BaseLayout.astro`: current `<head>` structure
- `knowledge/design/phase-09-upload-ui-brief.md` §Implementation Notes (Google Fonts strategy)

## Writes

- `frontend/src/layouts/BaseLayout.astro`: add 3 `<link>` tags to `<head>`

## Steps

1. Read current `BaseLayout.astro` `<head>` block
2. Inside `<head>`, BEFORE any other style/script links, insert:
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com" />
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
   <link rel="stylesheet"
     href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@700&family=IBM+Plex+Mono:wght@400;500&family=Roboto:wght@400;500&display=swap" />
   ```
3. Verify SEO `<title>`, `<meta>`, JSON-LD remain unchanged
4. Run `pnpm build` from `frontend/`; must exit 0; `dist/index.html` must still contain `application/ld+json`, `canonical`, `<h1`
5. Smoke check: `dist/index.html` now contains `fonts.googleapis.com` reference

## Output

- Updated `frontend/src/layouts/BaseLayout.astro` with 3 Google Fonts `<link>` tags

## Gate

- 3 new `<link>` tags in `<head>` (preconnect + preconnect + stylesheet)
- `pnpm build` exit 0
- SEO markers preserved
- `dist/index.html` references Google Fonts URL

## Abort conditions

- `pnpm build` fails after font links added → halt; report full log
- SEO markers missing from rebuilt `dist/index.html` → halt; restore from backup

## MCP whitelist/blacklist

- Allowed: Bash for `pnpm build`
- Forbidden: git
