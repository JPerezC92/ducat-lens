# Phase 01 — Template + spec scrub (AI attribution rule)

## Owner

Marshal 🎖️ (HR Director)

## Pre

- Working tree intact (untracked but present)
- No tracked files on `main` yet (remote + local both empty of commits)
- Rule wording locked in `plan.md` Body section (agent-agnostic — covers Claude, GPT, Gemini, Copilot, Cursor, any LLM)

## Reads

- `.claude/skills/git-commit/SKILL.md` — current template
- `.claude/skills/git-pr/SKILL.md` — currently emits `🤖 Generated with [Claude Code]` footer (line 50)
- `.claude/agents/herald.md` — Herald spec, Hard Rules section
- `agents/herald/profile.md` — Herald persona principles
- `CLAUDE.md` — Operational gates section

## Writes

- `.claude/skills/git-commit/SKILL.md` — add Rule entry: "Never write any AI/agent attribution into the commit message (no `Co-Authored-By:` trailer naming a bot, no `🤖 Generated with` footer, no AI tool URL). Human authors only. Applies regardless of which AI tool runs this skill."
- `.claude/skills/git-pr/SKILL.md` — remove the `🤖 Generated with [Claude Code](https://claude.com/claude-code)` line from the Body template; add Rule entry mirroring the git-commit wording (no AI attribution in PR title, body, or footer)
- `.claude/agents/herald.md` — add Hard Rule entry: "Never inject AI/agent attribution into commits, PRs, branch names, or tags. Strip any `Co-Authored-By:` trailer naming a bot/AI account, any `🤖 Generated with` / `Generated with [X]` footer, and any AI tool URL (claude.com/claude-code, cursor.sh, copilot.github.com, openai.com, anthropic.com) before running `git commit -F commit.txt` or `gh pr create`. Rule is agent-agnostic — applies to Claude, GPT, Gemini, Copilot, Cursor, any current or future LLM."
- `agents/herald/profile.md` — add matching principle under Herald's operating principles
- `CLAUDE.md` — under `## Operational gates`, add new subsection: "### Commit / PR hygiene (HARD RULE) — no AI/agent attribution in commit messages, PR titles, PR bodies, branch names, tags, or any tracked file. Human authors only. Applies to Claude, GPT, Gemini, Copilot, Cursor, any LLM. Herald 📯 (Release Manager) enforces; Sentinel 🛡️ (Quality Guardian) audits."

## Steps

1. Edit `.claude/skills/git-commit/SKILL.md`: append new bullet under `## Rules` section:
   - `Never include any AI/agent attribution in the commit message — no \`Co-Authored-By:\` trailer naming a bot/AI account (e.g. \`noreply@anthropic.com\`, \`bot@openai.com\`), no \`🤖 Generated with [X]\` footer, no AI tool URL. Human authors only. Rule is agent-agnostic.`
2. Edit `.claude/skills/git-pr/SKILL.md`:
   - Remove line 50: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
   - Append new bullet under `## Rules` section mirroring git-commit's wording (no AI attribution anywhere in title/body)
3. Edit `.claude/agents/herald.md` `## Hard Rules` section: append the agent-agnostic rule from the Writes section above.
4. Edit `agents/herald/profile.md`: append matching principle to the operating principles section (read file first to find the right anchor).
5. Edit `CLAUDE.md` `## Operational gates` section: add new subsection `### Commit / PR hygiene (HARD RULE)` with the wording from the Writes section above. Position immediately above `### Auto-run code verifiers`.

## Output

- 5 files edited, each containing the agent-agnostic AI-attribution-forbidden rule with consistent wording
- No code changes outside the 5 files listed

## Gate

- Sentinel 🛡️ (Quality Guardian) Phase 2 grep audit returns zero hits for all 8 AI-attribution patterns across the entire tracked tree
- All 5 edited files contain the literal string `agent-agnostic` (proof the rule is not Claude-specific)
- `CLAUDE.md` `## Operational gates` section now has `### Commit / PR hygiene` subsection above `### Auto-run code verifiers`

## Abort conditions

- Any edit attempt fails (file not found, edit conflict) → halt, report to Cipher 🔓 (Dev-Team Orchestrator)
- User pushback on rule wording → halt, request revised wording before edit
- Discovery of additional locations that need the rule (e.g. other skills, other agent specs) → halt, expand Writes list before proceeding

## MCP whitelist/blacklist

- Not applicable — local file edits only, no external services
