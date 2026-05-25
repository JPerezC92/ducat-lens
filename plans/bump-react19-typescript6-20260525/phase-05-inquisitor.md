# Phase 05 — Test-plan verification

## Owner

Inquisitor 🔎 (PR Reviewer)

## Pre

- Phase 04 complete: PR URL available
- All prior phases (01–03) evidence available in this conversation context

## Reads

- PR body (via `gh pr view <N> --json body --jq .body`)
- `frontend/package.json`
- `frontend/pnpm-lock.yaml`
- `frontend/dist/index.html`
- `git log` for no-AI-attribution scan

## Writes

- PR body (via `gh pr edit <N> --body-file <temp-file>`)

## Steps

1. `gh pr view <N> --json body --jq .body` → parse test-plan checkboxes
2. Per checkbox, identify verifier:
   - Pin version items (react 19.2.6, @types/react 19.2.15, @types/react-dom 19.2.3, typescript 6.0.3) → Inquisitor self (grep frontend/package.json)
   - `pnpm install` exit 0 → Atrium 🏛️ dispatch or evidence from Phase 02
   - `pnpm build` exit 0 + dist/index.html SEO markers → Atrium 🏛️ dispatch or evidence from Phase 02
   - `pnpm audit` 0 vulns → Warden 🔒 dispatch or evidence from Phase 03
   - No AI attribution → Inquisitor self (git log + PR body scan)
3. Collect evidence for each item
4. Rewrite PR body: `- [x] (evidence: …)` per pass; `- [ ] BLOCKED: <reason>` per fail
5. Write updated body to temp file; `gh pr edit <N> --body-file <temp-file>`
6. Return PASS (all ticked) or BLOCK (any failure) to Cipher

## Output

- All PR test-plan checkboxes ticked `[x]` with inline evidence
- Gate signal: PASS or BLOCK

## Gate

- All `- [ ]` items in the original PR body converted to `- [x]` with evidence
- No BLOCK items remain

## Abort conditions

- `gh pr view` fails (PR not found, auth error) → halt, report to Cipher
- Any checkpoint fails verification → mark BLOCK, halt, return BLOCK signal to Cipher for specialist fix dispatch
- AI attribution found in any git artifact → mark BLOCK, report to Cipher immediately
