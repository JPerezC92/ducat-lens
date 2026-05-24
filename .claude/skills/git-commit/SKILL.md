---
name: git-commit
description: Generate a conventional commit message by analyzing git changes and write it to commit.txt. Use when the user wants to commit, write a commit message, prepare staged changes, or says things like "commit this", "make a commit", "what should my commit say", or "I'm ready to push" — even if they don't say "commit message" explicitly.
disable-model-invocation: false
---

# Commit Message Generator

Analyze the current git changes and write a commit message to `commit.txt` at the repository root.

## Steps

1. Run `git status`, `git diff --stat`, `git diff --cached --stat`, and `git log --oneline -10` in parallel.
2. If the diff stat is small (under 20 files), run `git diff` and `git diff --cached` for the full diff. Otherwise, selectively read the most relevant changed files.
3. Detect if the repo is a monorepo (look for `pnpm-workspace.yaml`, `turbo.json`, `lerna.json`, `go.work`, or `[workspace]` in `Cargo.toml`).
4. Check if there are staged changes. If yes, write the message for staged changes only. If nothing is staged, write the message for all unstaged changes.
5. Analyze the commit log from step 1 to detect the existing commit message style (title format, body grouping, naming conventions). Match that style in the new message.
6. Ensure `commit.txt` is in `.gitignore` — if not, add it immediately before writing the file.
7. Write the commit message to `commit.txt` at the repository root.
8. Tell the user the commit message was written to `commit.txt`.

## Commit Format

Default to **conventional commits** format. If the existing commit log uses a different style, match that style instead.

### Title

```
type(scope): concise summary under 72 characters
```

- **type**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`, `perf`
- **scope**: required — derived from where the changes live
  - **Monorepo**: use the app/package directory name or a cross-cutting concern if changes span multiple packages
  - **Single repo**: use the module, feature, or layer affected (e.g., `auth`, `api`, `ui`, `config`)
- Description starts with a lowercase verb
- For breaking changes, add `!` after scope: `feat(api)!: remove deprecated endpoint`

### Body

Title focuses on the **why**. Body bullet points describe the **what** changed.

**Monorepo** — group changes by package/app path:

```
apps/web:
- what changed

apps/api:
- what changed
```

**Single repo** — use flat bullet points:

```
- what changed
- what changed
```

Only include sections for packages that actually have changes.

### Footer

For breaking changes:

```
BREAKING CHANGE: description of what breaks and migration path
```

Skip the body for small, single-scope changes where the title is self-explanatory.

## Rules

- Do NOT run `git commit` — only write the message to the file.
- Do NOT stage or unstage any files.
- Do NOT push to remote.
- If there are no changes, inform the user instead of writing an empty file.
- **HARD RULE — No AI/agent attribution:** Never include any AI/agent attribution in the commit message. No `Co-Authored-By:` trailer naming a bot or AI account (e.g. `noreply@anthropic.com`, `bot@openai.com`, `*@users.noreply.github.com` for AI bots). No `🤖 Generated with [X]` or `Generated with [X]` footer. No AI tool URL (claude.com, anthropic.com, openai.com, cursor.sh, copilot.github.com). No `--author="<AI name>"` flag. Human authors only. Rule is agent-agnostic — applies to Claude, GPT, Gemini, Copilot, Cursor, and any current or future LLM. Strip any such artifact before writing `commit.txt`.
