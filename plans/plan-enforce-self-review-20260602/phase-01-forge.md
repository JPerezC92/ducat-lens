# Phase 01 — Implement §2.4.5 self-review loop in SKILL.md

## Owner

Forge 🔨 (Implementation Agent)

## Pre

- Active plan `plan-enforce-self-review-20260602/plan.md` exists with `Status: active`
- Working branch is `feat/tooling/plan-enforce-self-review` — Cipher confirms Herald 📯 ran `git checkout -b feat/tooling/plan-enforce-self-review` off `main` before this phase starts
- `.claude/skills/plan-enforce/SKILL.md` readable and contains both `## 2.4 —` and `## 2.5 —` headers

## Reads

- `.claude/skills/plan-enforce/SKILL.md` — locate §2.4/§2.5 boundary for insertion point

## Writes

- `.claude/skills/plan-enforce/SKILL.md` — insert §2.4.5 block between §2.4 and §2.5

## Steps

1. Read full `.claude/skills/plan-enforce/SKILL.md`
2. Confirm `## 2.4 — Write the artifact` header exists; confirm `## 2.5 — Quality gate before ExitPlanMode` header exists immediately after — abort if either missing
3. Insert new section `## 2.4.5 — Self-Review Loop` between the end of §2.4 content and the `## 2.5` header. Section content must include:
   a. One-sentence purpose: "After writing the plan artifact, run a structured checklist; fix all findings; repeat until 0 findings or max iterations reached — then proceed to §2.5."
   b. Review checklist table with columns `ID | Check | Scope | Fix` and rows R1–R8 exactly as defined in `plan.md` Body
   c. Loop logic fenced block (pseudocode): `max_iterations=3`, iteration counter, `findings = run_checklist(R1..R8)`, log line `[Self-review iteration N/3] — N finding(s)`, exit-on-zero branch, fix-all branch, halt-on-max branch with surface-to-user instruction
   d. Note: "Max-iterations guard prevents infinite loop when a finding requires user input (e.g. R8 TBD only the user can fill)."
4. Do NOT modify any text outside the inserted §2.4.5 block
5. Verify: `grep -n "2.4.5" .claude/skills/plan-enforce/SKILL.md` returns exactly 1 hit

## Output

- `.claude/skills/plan-enforce/SKILL.md` — `## 2.4.5 — Self-Review Loop` section present between §2.4 and §2.5 with checklist + loop logic

## Gate

- `grep "## 2.4.5" .claude/skills/plan-enforce/SKILL.md` exits 0 with exactly 1 match
- `grep "## 2.5" .claude/skills/plan-enforce/SKILL.md` exits 0 (§2.5 still present and unmodified)
- `grep "## 2.4 —" .claude/skills/plan-enforce/SKILL.md` exits 0 (§2.4 still present and unmodified)

## Abort conditions

- §2.4 or §2.5 header not found in file → halt, report: "SKILL.md structure changed — expected headers not found; aborting to avoid corrupting the file"
- File unreadable → halt, report path error
- grep after insert returns 0 or >1 match for `2.4.5` → halt, report: "Insertion produced unexpected result — manual review needed"
