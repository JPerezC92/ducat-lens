# Phase 09: Commit + branch + PR

## Owner

Herald 📯 (Release Manager)

## Pre

- Phases 01-08 complete; all gates PASS or ADVISORY accepted by user
- Pre-coding sync gate confirmed at plan start (branch in sync with origin/main)

## Reads

- `frontend/` working tree: all phase 03-05 changes
- `.claude/skills/git-branch-name/SKILL.md`
- `.claude/skills/git-commit/SKILL.md`
- `.claude/skills/git-pr/SKILL.md`

## Writes

- New git branch (from `git-branch-name` skill)
- New git commit (no AI attribution)
- Remote branch push
- GitHub PR

## Steps

1. Invoke `git-branch-name` skill → derive name from scope. Expected: `feat/frontend/phase-09-upload-ui` or similar
2. `git checkout -b <branch>`
3. `git status`; verify ONLY frontend files changed (no backend drift; no plan/* drift unless plan was modified mid-execution; no knowledge/ drift unless audit reports updated this run)
4. `git add` ONLY frontend/ + knowledge/audits/phase-09-visual-audit-20260525.md + plan files updated this run
5. Invoke `git-commit` skill → draft commit message. NO Co-Authored-By trailer, NO `🤖 Generated with`, NO AI tool URLs
6. `git commit -F <message-file>`
7. `git push -u origin <branch>`
8. Invoke `git-pr` skill → draft PR title + body with test plan checkboxes. NO AI attribution
9. `gh pr create --title "<title>" --body-file <body-file>`

## Output

- PR URL (return to Cipher 🔓 (Dev-Team Orchestrator))

## Gate

- Branch diff: ONLY frontend/ + knowledge/audits/ + plan files
- Commit message: zero AI attribution artifacts
- PR body: test-plan checkboxes `- [ ]` for every plan §Verification item (10 boxes)
- `gh pr create` exits 0

## Abort conditions

- Sync gate fails at PR time (origin/main moved during work) → halt, merge main, re-run from step 1
- Any AI attribution detected → strip + re-run from `git commit`
- `git push` fails → halt; do NOT force-push without user explicit ok (escalate to Cipher 🔓 (Dev-Team Orchestrator))

## MCP whitelist/blacklist

- Allowed: Bash for git, gh
- Forbidden: any code edits; force-push; rebase -i
