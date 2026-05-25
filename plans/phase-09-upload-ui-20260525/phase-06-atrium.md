# Phase 06: Build + type verify

## Owner

Atrium 🏛️ (Frontend Architect)

## Pre

- Phase 05 complete: 5 components implemented

## Reads

- `frontend/src/components/*.tsx`: all new components
- `frontend/src/layouts/BaseLayout.astro`
- `frontend/src/pages/index.astro`
- `frontend/tsconfig.json`
- `frontend/astro.config.mjs`
- `frontend/dist/index.html` (post-build)

## Writes

- None (read-only audit)

## Steps

1. `cd D:\projects\ducat-lens\frontend`
2. `pnpm install`; must exit 0, 0 peer warnings (or only acceptable react-dropzone peer warning)
3. `pnpm build`; must exit 0; record build time
4. Inspect each new component for clean architecture violations:
   - State colocation (no prop drilling >2 levels)
   - No leaked side effects in render
   - Tailwind tokens used (not hex literals or `style` props)
   - React 19 patterns (no deprecated `forwardRef`, hooks only)
   - Astro vs React island boundary respected
5. TypeScript strict pass; no `any`, no `@ts-ignore`, no `@ts-expect-error` without comment justification
6. Verify `dist/index.html` SEO markers: `application/ld+json`, `canonical`, `<h1`
7. Verify `dist/index.html` contains Google Fonts `<link>` references (preconnect + stylesheet)

## Output

- Structured `[PASS]` / `[FAIL]` / `[UNCERTAIN]` report per Atrium 🏛️ (Frontend Architect) spec

## Gate

- `pnpm build` exit 0
- 0 TypeScript errors
- SEO markers preserved
- No clean-architecture violations Critical/High
- No raw hex / inline style in new components

## Abort conditions

- Any FAIL → return to Forge 🔨 (Implementation Agent) (phase 05) with specific violation list
- UNCERTAIN on architecture call → escalate to Cipher 🔓 (Dev-Team Orchestrator) with options

## MCP whitelist/blacklist

- Allowed: Bash for `pnpm install`, `pnpm build`
- Forbidden: git
