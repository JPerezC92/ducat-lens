# Phase 03 — Commit + push (amend PR #12)

## Owner

Herald 📯 (Release Manager)

## Pre

- Phase 01 Gate PASS + Phase 02 Gate PASS
- On branch `feat/frontend/add-crt-image-figures`
- Working tree contains: `frontend/public/images/bg-warframe.png` (new), updated `frontend/src/styles/global.css`, updated `knowledge/audits/lumen-images-20260527.md`

## Reads

- `git status` — confirm only expected paths changed
- `plans/add-landing-bg-image-20260602/plan.md` — for commit context

## Writes

- New commit on `feat/frontend/add-crt-image-figures`
- Pushed to remote (PR #12 auto-updates)

## Steps

1. Verify on branch `feat/frontend/add-crt-image-figures`: `git branch --show-current`
2. Stage explicit paths only:
   ```
   git add frontend/public/images/bg-warframe.png
   git add frontend/src/styles/global.css
   git add knowledge/audits/lumen-images-20260527.md
   git add plans/add-landing-bg-image-20260602/
   ```
3. Invoke `git-commit` skill → writes `commit.txt`. Strip any AI attribution before committing (HARD RULE).
4. `git commit -F commit.txt`. Verify with `git log -1 --pretty=full`.
5. `git push origin feat/frontend/add-crt-image-figures`. PR #12 auto-updates.
6. Return push confirmation + updated PR URL to Cipher 🔓 (Dev-Team Orchestrator).

## Output

- New commit SHA on remote `feat/frontend/add-crt-image-figures`
- PR #12 updated at https://github.com/JPerezC92/ducat-lens/pull/12

## Gate

- `git push` exits 0
- `git log -1` shows new commit, no AI attribution
- PR #12 visible at GitHub with updated file list

## Abort conditions

- `git push` rejected → halt, return to Cipher 🔓 (Dev-Team Orchestrator); never `--force` to any branch without explicit user approval
- Pre-commit hook fail → fix root cause + create NEW commit (never `--amend`, never `--no-verify`)
- `git-commit` skill emits AI attribution → strip before running `git commit -F`

## MCP whitelist/blacklist

- Allowed: `Bash` (git + gh per CLAUDE.md Herald Bash registry)
- Forbidden: any direct file edit
