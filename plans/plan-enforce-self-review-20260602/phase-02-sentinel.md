# Phase 02 — Audit SKILL.md for consistency and edge cases

## Owner

Sentinel 🛡️ (Quality Guardian)

## Pre

- Phase 01 gate passed: `## 2.4.5 — Self-Review Loop` present in SKILL.md
- `## 2.5 — Quality gate before ExitPlanMode` still present and unmodified

## Reads

- `.claude/skills/plan-enforce/SKILL.md` — full file post-Phase 01
- `plans/plan-enforce-self-review-20260602/plan.md` — R1–R8 row definitions for Step 6 comparison

## Writes

- None — audit only; fixes route back to Forge via Cipher

## Steps

1. Read full updated `.claude/skills/plan-enforce/SKILL.md`
2. Check §2.4.5 does not duplicate §2.5 checks (§2.5 checks must remain the load-bearing gate; §2.4.5 is a pre-gate pre-filter)
3. Check §2.4.5 loop logic handles edge cases:
   a. Empty plan (no phases) → rows R1/R6/R7 return 0 findings (no runbooks = nothing to check — not an error)
   b. Single-file plan (no runbooks) → R1/R4/R5/R8 must apply to Body lines, not phase runbooks
   c. Plan with all Steps already concrete → loop exits after iteration 1 with 0 findings (no false positives)
4. Check that the max_iterations=3 guard is explicit in the pseudocode block
5. Check that the user-surface instruction at halt (max iterations reached) tells Cipher to ask the user — not silently skip
6. Check that checklist rows R1–R8 in SKILL.md exactly match the rows defined in `plans/plan-enforce-self-review-20260602/plan.md` (no row added/dropped/reworded without plan update)
7. Report: `[PASS]` if all 6 checks pass; `[FAIL]` with specific line numbers and findings otherwise

## Output

- Inline audit report: `[PASS]` or `[FAIL] <line-level findings list>`

## Gate

- Sentinel returns `[PASS]`, OR all `[FAIL]` findings routed to Forge and resolved, then Sentinel re-audits and returns `[PASS]`

## Abort conditions

- `.claude/skills/plan-enforce/SKILL.md` unreadable after Phase 01 → halt, report path error
- `plan.md` unreadable (needed for R1–R8 row comparison) → skip step 6 only; note in report

## MCP whitelist/blacklist

- Forbidden: all MCP tools (read-only local audit, no external systems needed)
