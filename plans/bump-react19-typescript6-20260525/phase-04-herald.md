# Phase 04 — Commit + PR

## Owner

Herald 📯 (Release Manager)

## Pre

- Phases 01–03 complete: package.json updated; pnpm-lock.yaml updated; build passes; 0 audit vulns
- Pre-coding sync gate confirmed: branch is in sync with origin/main

## Reads

- `frontend/package.json`
- `frontend/pnpm-lock.yaml`
- `.claude/skills/git-branch-name/SKILL.md`
- `.claude/skills/git-commit/SKILL.md`
- `.claude/skills/git-pr/SKILL.md`

## Writes

- New git branch (from git-branch-name skill output)
- New git commit
- Remote branch push
- GitHub PR

## Steps

1. Invoke `git-branch-name` skill → derive branch name from task type (chore) + scope (frontend) + bump description
2. `git checkout -b <branch>`
3. `git add frontend/package.json frontend/pnpm-lock.yaml` — stage only these two files
4. Invoke `git-commit` skill → draft commit message: no AI attribution, no Co-Authored-By trailer
5. `git commit -m "$(cat <<'EOF'\n<commit message>\nEOF\n)"`
6. `git push -u origin <branch>`
7. Invoke `git-pr` skill → draft PR title + body with test plan checkboxes; no AI attribution, no "Generated with" footer
8. `gh pr create --title "<title>" --body "$(cat <<'EOF'\n<body>\nEOF\n)"`

## Output

- PR URL (e.g. https://github.com/JPerezC92/ducat-lens/pull/8)

## Gate

- Branch diff: only `frontend/package.json` + `frontend/pnpm-lock.yaml` changed
- Commit message: no `Co-Authored-By`, no `🤖`, no AI tool URLs
- PR body: includes test-plan checkboxes `- [ ]` for all verification items; no AI attribution
- `gh pr create` exits 0 and returns PR URL

## Abort conditions

- Sync gate fails (branch behind origin/main) → halt, merge main, then re-run from Step 2
- Any AI attribution detected in commit message or PR body → strip and re-run before pushing
- `git push` fails → report error to Cipher; do not retry force-push
