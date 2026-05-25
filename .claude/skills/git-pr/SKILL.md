---
name: git-pr
description: Draft a pull request title and body by analyzing branch commits and diff vs main, writing output to pr-draft.md. Use when the user wants to open a PR, create a pull request, draft a PR description, or says "I'm done with this branch" / "ready to merge" / "submit my changes" — even if they don't say "pull request" explicitly.
disable-model-invocation: false
---

# PR Draft Generator

Analyze the current branch divergence from main and write a PR title + body to `pr-draft.md` at the repository root.

## Steps

1. Run these in parallel:
   - `git status`
   - `git log --oneline main...HEAD`
   - `git diff main...HEAD --stat`
   - `git log --oneline -5` (recent style reference)
2. If the diff stat is small (under 20 files), run `git diff main...HEAD` for the full diff. Otherwise, read the most relevant changed files selectively.
3. Check for a plan or ticket file that explains the motivation:
   - Look for `plans/*.md` with `Status: active` or `Status: completed`
   - Look for `tickets/` subdirs matching recent commit refs
   - If found, read the **Context** section for the why
4. Determine the PR title and body following the format below.
5. Ensure `pr-draft.md` is in `.gitignore` — if not, add it immediately before writing.
6. Write the output to `pr-draft.md` at the repository root.
7. Print the ready-to-run `gh pr create` command with the draft content inlined.

## PR Format

### Title

```
type(scope): concise summary under 70 characters
```

- Same `type` and `scope` conventions as conventional commits
- Imperative mood, lowercase after the colon
- No trailing period

### Body

```markdown
## Summary
- <bullet: what changed and why — one line each, max 3>

## Test plan
- [ ] <what to verify manually or via CI>
- [ ] <edge case or regression to check>
```

- **Summary**: focus on *why*, not *what* the diff shows — the diff is already visible
- **Test plan**: concrete steps a reviewer can follow; at least 2 items
- Keep the body under 20 lines total

### Breaking changes

If any commit title has `!` or the diff removes/renames a public interface, add before the test plan:

```markdown
## Breaking changes
- <what breaks>
- Migration: <one-line path>
```

## Output file

`pr-draft.md` content:

```
Title: <title here>

---

<body here>
```

## Rules

- Do NOT run `gh pr create` or any git command that mutates state — only write the draft file.
- Do NOT stage, commit, or push anything.
- If on main/master with no diverging commits, inform the user — no draft to write.
- If the branch has no commits ahead of main, check for uncommitted changes and suggest running `/git-commit` first.
- After writing the file, print the full ready-to-run command:
  ```
  gh pr create --title "<title>" --body "$(cat pr-draft.md | tail -n +4)"
  ```
- **HARD RULE — No AI/agent attribution:** Never include any AI/agent attribution in the PR title, body, or footer. No `🤖 Generated with [X]` or `Generated with [X]` footer. No AI tool URL (claude.com, anthropic.com, openai.com, cursor.sh, copilot.github.com). No `Co-Authored-By:` trailer naming a bot or AI account (e.g. `noreply@anthropic.com`, `bot@openai.com`, `*@users.noreply.github.com` for AI bots). Human authors only. Rule is agent-agnostic — applies to Claude, GPT, Gemini, Copilot, Cursor, and any current or future LLM. Strip any such artifact before writing `pr-draft.md`.
