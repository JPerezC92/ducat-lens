---
Status: active
Started: 2026-05-24 11:30
Subject: Scrub AI attribution from commits/PRs/repo and re-push local work to remote via PR
Layout: subfolder pattern
---

# Plan — Scrub AI attribution + clean re-push

## Context

> User went nuclear on the prior repo state after discovering `Co-Authored-By: Claude` trailers and `🤖 Generated with [Claude Code]` footer on PR #1. Local working tree intact; remote `JPerezC92/ducat-lens` is empty; local `main` has no commits. Need to (1) future-proof tooling so no AI/agent attribution ever leaks into git artifacts again, and (2) re-push the migration work cleanly via a PR.

- Prompted by: user discovery of AI co-author trailers on merged PR #1; user wants outside reviewers to see human-only authorship.
- Goal: remote `main` rebuilt from local working tree via PR; zero AI/agent attribution in any tracked file, commit, branch name, PR title, or PR body — now and forward.
- Outcome: PR opened (user merges), clean `main`, hardened tooling that refuses to inject AI attribution regardless of which AI tool runs Herald 📯 (Release Manager).

## Body

| Concern | Action |
|---|---|
| Skill templates inject AI footer/trailer | Marshal 🎖️ (HR Director) scrubs `git-commit` + `git-pr` SKILL.md |
| Herald spec silent on attribution rule | Marshal 🎖️ (HR Director) adds HARD RULE: strip any AI co-author trailer / bot footer / generator URL before commit, PR, or push |
| Persona profile silent on rule | Marshal 🎖️ (HR Director) mirrors rule in `agents/herald/profile.md` |
| CLAUDE.md silent | Marshal 🎖️ (HR Director) adds entry under Operational gates |
| Existing tracked files may still hold AI markers | Sentinel 🛡️ (Quality Guardian) greps repo for trailer/footer/bot-URL patterns; fails if any hit |
| Remote empty | Herald 📯 (Release Manager) bootstrap-commit on main (README + .gitignore), push, branch `chore/initial-scaffold`, commit rest, push, open PR → user merges |

**Rule (agent-agnostic — applies to Claude, GPT, Gemini, Copilot, Cursor, any LLM):**

Forbidden in any commit message, PR title, PR body, branch name, or tracked repo file:
- `Co-Authored-By:` trailer naming an AI/bot account or pointing to a bot email (`noreply@anthropic.com`, `bot@openai.com`, `*@users.noreply.github.com` for AI bots, etc.)
- "Generated with [X]" / "🤖" footers naming any AI tool
- `--author="<AI name>"` flags
- Signatures linking to AI tool URLs (`claude.com/claude-code`, `cursor.sh`, `copilot.github.com`, `openai.com`, `anthropic.com`)

Human authors only.

## Phase index — dispatch table

| # | Phase | Owner | Runbook | Output |
|---|---|---|---|---|
| 1 | Template + spec scrub | Marshal 🎖️ (HR Director) | `phase-01-marshal-template-scrub.md` | Edited skills + Herald spec + persona + CLAUDE.md |
| 2 | Repo-wide grep audit | Sentinel 🛡️ (Quality Guardian) | `phase-02-sentinel-audit.md` | `_audit-report.md` with zero AI-attribution hits in tracked tree |
| 3 | Bootstrap + branch + PR | Herald 📯 (Release Manager) | `phase-03-herald-initial-push.md` | PR URL → user merges |

## Critical files / tools

- `.claude/skills/git-commit/SKILL.md`
- `.claude/skills/git-pr/SKILL.md`
- `.claude/agents/herald.md`
- `agents/herald/profile.md`
- `CLAUDE.md`
- Sentinel grep patterns: `Co-Authored-By.*(noreply|bot|users\.noreply)`, `Generated with`, `🤖`, `claude\.com`, `openai\.com`, `cursor\.sh`, `copilot\.github\.com`, `anthropic\.com`
- `gh` CLI for PR

## Verification

- ⬜ Phase 1: `git-commit` SKILL.md contains explicit "no AI attribution" rule; `git-pr` SKILL.md no longer emits `🤖 Generated with` footer
- ⬜ Phase 1: Herald spec has HARD RULE forbidding AI co-author / bot footer / generator URL injection (agent-agnostic wording)
- ⬜ Phase 1: `agents/herald/profile.md` mirrors rule
- ⬜ Phase 1: `CLAUDE.md` Operational gates section adds "Commit/PR hygiene" entry
- ⬜ Phase 2: `_audit-report.md` shows zero hits across tracked files for all 8 grep patterns
- ⬜ Phase 3: bootstrap commit on `main` (`README.md` + `.gitignore` only) pushed, no AI attribution in commit message
- ⬜ Phase 3: feature branch `chore/initial-scaffold` pushed with single commit covering all remaining files
- ⬜ Phase 3: PR opened, title + body free of AI attribution
- ⬜ Phase 3: `git log origin/main..origin/chore/initial-scaffold` shows clean commits
- ⬜ User merges PR (sole merge authority — Cipher 🔓 (Dev-Team Orchestrator) never runs `gh pr merge`)

## Out of scope

- Re-creating PR #1 or its merge SHA (PR #1 is dead with the nuked repo state)
- Editing Claude Code's built-in system prompt (cannot — only project-level overrides)
- Resuming the `ducat-lens-bootstrap-20260524` plan (separate active plan, paused; will resume after this scrub ships)
- Adding pre-commit git hooks to enforce (deferred — Marshal spec rule + Sentinel audit cover this scope)

## Pending

- [waiting for] user merge of PR after Herald 📯 (Release Manager) opens it
