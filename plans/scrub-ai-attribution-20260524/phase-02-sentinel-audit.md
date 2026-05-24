# Phase 02 — Repo-wide AI-attribution grep audit

## Owner

Sentinel 🛡️ (Quality Guardian)

## Pre

- Phase 1 complete: Marshal 🎖️ (HR Director) edits applied to skills + Herald spec + persona + CLAUDE.md
- No tracked files on `main` yet (audit operates on the staged-for-tracking working tree)

## Reads

- All files Herald 📯 (Release Manager) plans to stage in Phase 3 (everything except gitignored paths)
- `.gitignore` to determine the exact tracked set

## Writes

- `plans/scrub-ai-attribution-20260524/_audit-report.md` — grep results table

## Steps

1. Compute the tracked-file set: list every untracked file via `git status --short`, then filter out anything matched by `.gitignore` (`git check-ignore` per path or `git status --ignored --short`).
2. Run grep across the tracked-set for each of the 8 patterns (case-insensitive where relevant):
   - `Co-Authored-By:.*noreply@anthropic\.com`
   - `Co-Authored-By:.*bot@`
   - `Co-Authored-By:.*\.bot\b`
   - `Generated with \[Claude Code\]`
   - `🤖`
   - `claude\.com/claude-code`
   - `openai\.com|cursor\.sh|copilot\.github\.com`
   - `anthropic\.com`
3. Allowlist for legitimate references (rule wording itself MUST mention these patterns):
   - `plans/scrub-ai-attribution-20260524/**` (this plan's own files)
   - `.claude/skills/git-commit/SKILL.md` (rule statement)
   - `.claude/skills/git-pr/SKILL.md` (rule statement)
   - `.claude/agents/herald.md` (rule statement)
   - `agents/herald/profile.md` (rule statement)
   - `CLAUDE.md` (rule statement)
4. Build `_audit-report.md` with a table: `pattern | hit count | file:line refs` and a final verdict line `VERDICT: PASS` or `VERDICT: FAIL`.
5. If any hit lands outside the allowlist → verdict FAIL, halt phase, report to Cipher 🔓 (Dev-Team Orchestrator).

## Output

- `plans/scrub-ai-attribution-20260524/_audit-report.md` with table + verdict
- Final line of report must read either `VERDICT: PASS` or `VERDICT: FAIL` (no other strings)

## Gate

- `_audit-report.md` final line reads `VERDICT: PASS`
- Zero hits outside the allowlist
- Cipher 🔓 (Dev-Team Orchestrator) reads the report and confirms PASS before dispatching Phase 3

## Abort conditions

- Verdict FAIL → halt, surface offending file:line refs to Cipher 🔓 (Dev-Team Orchestrator), route fix back to Marshal 🎖️ (HR Director) for additional scrub, re-run audit
- Any of the 5 Phase-1-edited files missing the rule statement entirely (rule not added) → halt, route back to Marshal 🎖️ (HR Director)
- Grep tool unavailable → fall back to manual `Grep` tool calls per pattern; do not skip

## MCP whitelist/blacklist

- Not applicable — local grep only
