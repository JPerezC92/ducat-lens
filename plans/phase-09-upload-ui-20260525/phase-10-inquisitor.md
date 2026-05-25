# Phase 10: Test-plan verification gate

## Owner

Inquisitor 🔎 (PR Reviewer)

## Pre

- Phase 09 complete: PR URL available

## Reads

- PR body via `gh pr view <N> --json body --jq .body`
- `frontend/package.json`
- `frontend/pnpm-lock.yaml`
- `frontend/dist/index.html` (post-build)
- `frontend/src/components/*.tsx` (post-Forge)
- `knowledge/audits/phase-09-visual-audit-20260525.md`
- `plans/phase-09-upload-ui-20260525/plan.md`: phase outputs cross-reference
- `git log main...HEAD` for no-AI-attribution scan
- `git diff main...HEAD --stat` for scope drift

## Writes

- PR body via `gh pr edit <N> --body-file <temp-file>`

## Steps

1. `gh pr view <N> --json body --jq .body` → parse test-plan checkboxes
2. Per checkbox, identify verifier (self vs specialist dispatch):
   - Stack/build items → self-verify via `pnpm build` log + lockfile read
   - Visual items → re-dispatch Lumen ✨ (Visual Director) if needed OR cite phase-07 audit report
   - Behavior items (POST /analyze wiring, sort, mobile breakpoint) → cite phase-05/06 outputs + DOM inspection via agent-browser
   - Accessibility items → cite phase-07 audit contrast table + computed style snapshot
   - No-AI-attribution → self-scan git log + PR body + diff
3. Collect evidence for each item
4. Rewrite PR body: `- [x] (evidence: <one-line>)` per pass; `- [ ] BLOCKED: <reason>` per fail
5. Write updated body to temp file; `gh pr edit <N> --body-file <temp-file>`
6. Return PASS (all ticked) or BLOCK (any failure) to Cipher 🔓 (Dev-Team Orchestrator)

## Output

- All PR test-plan checkboxes ticked `[x]` with inline evidence
- Gate signal: PASS or BLOCK

## Gate

- All `- [ ]` items in original PR body converted to `- [x]` with evidence
- No BLOCK items remain
- No AI attribution anywhere in git artifacts

## Abort conditions

- `gh pr view` fails → halt; report to Cipher 🔓 (Dev-Team Orchestrator)
- Checkpoint fails → mark BLOCK; halt; return BLOCK to Cipher 🔓 (Dev-Team Orchestrator) for specialist fix dispatch
- AI attribution found in commit/PR body → BLOCK; report immediately to Cipher 🔓 (Dev-Team Orchestrator)

## MCP whitelist/blacklist

- Allowed: Bash for `gh pr view`, `gh pr edit`, `gh pr comment`, `git diff main...HEAD`, `git log main...HEAD --oneline`
- Forbidden: any code edits; force-push
