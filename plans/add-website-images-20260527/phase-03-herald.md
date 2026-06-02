# Phase 03 — Commit + branch + PR

## Owner

Herald 📯 (Release Manager) — owns this runbook end-to-end. Inquisitor 🔎 (PR Reviewer) gate is post-phase Cipher 🔓 (Dev-Team Orchestrator) orchestration; tracked in plan.md Verification, not this runbook.

## Pre

- Phase 01 Gate PASS (build + Atrium 🏛️ (Frontend Architect))
- Phase 02 Gate PASS (Lumen ✨ (Visual Director) visual audit clean or Medium-only)
- Working tree contains: `frontend/public/images/hero-prime.png`, `frontend/public/images/example-kiosk.jpg`, edited `frontend/src/pages/index.astro`, edited `frontend/src/styles/global.css`, new `knowledge/audits/lumen-images-20260527.md`
- All other files unchanged (verify via `git status` — only the above paths)

## Reads

- `git status` + `git diff main...HEAD` — full diff via Herald Bash registry
- `plans/add-website-images-20260527/plan.md` — for PR body Test plan section
- `knowledge/audits/lumen-images-20260527.md` — for PR body Visual audit section

## Writes

- New git branch (name from `git-branch-name` skill)
- New commit (message from `git-commit` skill → `commit.txt` → `git commit -F commit.txt`)
- Pushed remote branch
- Opened PR (body from `git-pr` skill → `pr-draft.md` → `gh pr create --body-file pr-draft.md`)

## Steps

1. Invoke `git-branch-name` skill → returns suggestion (expected pattern: `feat/landing-crt-images-20260527` or similar). Create branch: `git checkout -b <name>`.
2. Stage explicit paths only (no `git add -A`):
   ```
   git add frontend/public/images/hero-prime.png \
           frontend/public/images/example-kiosk.jpg \
           frontend/src/styles/global.css \
           frontend/src/pages/index.astro \
           knowledge/audits/lumen-images-20260527.md \
           plans/add-website-images-20260527/
   ```
3. Invoke `git-commit` skill → writes `commit.txt`. Verify message:
   - No AI attribution (no `Co-Authored-By:` AI bot, no `🤖 Generated with`, no AI tool URLs) per CLAUDE.md HARD RULE
   - Conventional commits format
   - Subject ≤ 72 chars
4. `git commit -F commit.txt`. Verify with `git log -1 --pretty=full`.
5. Push: `git push -u origin <branch>`.
6. Invoke `git-pr` skill → writes `pr-draft.md` with Summary + Test plan + Visual audit sections.
   - Test plan checklist MUST mirror plan.md Verification items (one ⬜ per item)
   - Body MUST be free of AI attribution per CLAUDE.md HARD RULE
7. `gh pr create --base main --head <branch> --title "<title>" --body-file pr-draft.md`. Capture PR URL.
8. Return PR URL to Cipher 🔓 (Dev-Team Orchestrator). Herald's runbook ends here. Post-phase Inquisitor 🔎 (PR Reviewer) dispatch is Cipher orchestration per CLAUDE.md test-plan verification gate — tracked in plan.md Verification, not in this runbook.

## Output

- PR URL (returned to Cipher 🔓 (Dev-Team Orchestrator))
- Pushed remote branch
- New commit on remote

## Gate

- `gh pr create` exit 0
- PR body Test plan section has same number of ⬜ items as plan.md Verification
- Zero AI attribution artifacts in commit message, PR title, PR body, branch name (per CLAUDE.md HARD RULE)
- All staged paths match phase-03 Pre working-tree list (no extras)

## Abort conditions

- `git push` rejected (force-push needed) → halt, return to Cipher 🔓 (Dev-Team Orchestrator); never `--force` to main
- `gh pr create` 4xx error → halt, return to Cipher 🔓 (Dev-Team Orchestrator)
- Pre-commit hook fail → fix root cause + create NEW commit (never `--amend`, never `--no-verify`)
- `git-commit` or `git-pr` skill emits AI attribution → strip + re-run skill before commit/PR

## MCP whitelist/blacklist

- Allowed: `Bash` (git + gh per CLAUDE.md Herald Bash registry)
- Forbidden: any direct file edit outside `commit.txt` / `pr-draft.md` (those are skill outputs); never edit `frontend/src/`
