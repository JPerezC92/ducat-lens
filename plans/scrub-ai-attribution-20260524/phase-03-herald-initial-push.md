# Phase 03 — Bootstrap main + feature branch + PR

## Owner

Herald 📯 (Release Manager)

## Pre

- Phase 1 done: `git-commit` + `git-pr` + Herald spec + persona + CLAUDE.md scrubbed
- Phase 2 done: Sentinel 🛡️ (Quality Guardian) verdict = PASS
- Remote `origin` (https://github.com/JPerezC92/ducat-lens.git) confirmed empty (`git ls-remote origin` returns no refs)
- Local `main` has no commits, all migration work is untracked
- User confirmed: PR pattern, not direct push to main

## Reads

- `git status --short` to enumerate untracked files
- `.gitignore` to confirm exclusions
- All files Herald 📯 (Release Manager) will stage (for commit message generation via `git-commit` skill)

## Writes

- 2 commits total:
  1. `chore: initial repository scaffold` on `main` — stages only `README.md` + `.gitignore`
  2. `chore: bootstrap ducat-lens agent orchestration tooling` on `chore/initial-scaffold` — stages everything else
- 1 PR opened from `chore/initial-scaffold` → `main`

## Steps

1. **Bootstrap main**:
   - `git status --short` — confirm untracked working tree intact
   - `git add README.md .gitignore`
   - Invoke `git-commit` skill → produces `commit.txt` with title `chore: initial repository scaffold` (style match: prior pre-nuclear initial scaffold commit)
   - Manually verify `commit.txt` has NO `Co-Authored-By:` line, NO `🤖 Generated with` footer, NO AI tool URL — if any present, strip them before commit
   - `git commit -F commit.txt`
   - `git push -u origin main`
2. **Branch off for the migration content**:
   - Invoke `git-branch-name` skill → expect `chore/initial-scaffold` (or accept Herald 📯 (Release Manager)'s alternate suggestion if more apt)
   - `git checkout -b chore/initial-scaffold`
3. **Stage everything else**:
   - `git status --short` — list all remaining untracked
   - `git add <each path explicitly>` (HARD RULE: no `git add -A` / `git add .`)
   - Flag suspicious files per Herald spec (`.env`, `*.pem`, `*.key`, `*secret*`, `*token*`) — none expected, but verify
4. **Commit**:
   - Invoke `git-commit` skill → produces `commit.txt`
   - Manually verify NO AI attribution in `commit.txt` (Co-Author, footer, URL)
   - `git commit -F commit.txt`
5. **Push branch**:
   - `git push -u origin chore/initial-scaffold`
6. **Open PR**:
   - Invoke `git-pr` skill → produces `pr-draft.md` (post-Phase-1 scrub: no `🤖 Generated with` footer)
   - Manually verify `pr-draft.md` body has NO AI attribution
   - `gh pr create --title "<title from pr-draft.md>" --body "$(cat pr-draft.md | tail -n +4)" --base main --head chore/initial-scaffold`
   - Capture PR URL from gh output
7. **Return to main**:
   - `git checkout main`
8. **Report**:
   - PR URL, both commit SHAs, branch name → Cipher 🔓 (Dev-Team Orchestrator)
   - Cipher 🔓 (Dev-Team Orchestrator) surfaces to user
   - User merges (sole merge authority — Cipher 🔓 (Dev-Team Orchestrator) NEVER runs `gh pr merge`)

## Output

- `origin/main` with 1 commit: `chore: initial repository scaffold` (no AI attribution)
- `origin/chore/initial-scaffold` with 1 commit: `chore: bootstrap ducat-lens agent orchestration tooling` (no AI attribution)
- PR URL (open state, awaiting user merge)

## Gate

- `git log --format="%B" origin/main` shows no `Co-Authored-By:`, no `🤖`, no `Generated with`, no `claude.com`/`anthropic.com`
- `git log --format="%B" origin/chore/initial-scaffold` — same check
- `gh pr view <N> --json title,body` — title + body free of AI attribution
- `git status` on `main` after checkout = clean

## Abort conditions

- Sentinel Phase 2 verdict = FAIL → do not start Phase 3
- `commit.txt` or `pr-draft.md` contains AI attribution despite Phase 1 scrub → strip manually, do NOT proceed; route back to Marshal 🎖️ (HR Director) to harden skill template further
- `git push` rejected (non-fast-forward or auth) → halt, report to Cipher 🔓 (Dev-Team Orchestrator); never `--force` per Herald spec
- Pre-commit hook fails → standard Herald hook-failure handling (stop, report, wait, new commit not amend)
- User decides direct push to main instead → halt PR flow, await new instruction (Herald spec forbids direct push to main for PR workflows)

## MCP whitelist/blacklist

- Allowed: `gh` CLI for PR creation only
- Forbidden: `gh pr merge` (user sole merge authority); any `--force`/`--no-verify`/`--no-gpg-sign` flag
