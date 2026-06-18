---
Status: active
Started: 2026-06-02 14:00
Subject: Add autonomous self-review loop to plan-enforce skill — post-creation quality iteration until zero issues found
Layout: subfolder pattern
---

# Plan — plan-enforce self-review loop

## Context

- Prompted by: user feedback — after plan creation, manual double-checks kept finding issues; user wants plan-enforce to self-iterate until clean
- Goal: After §2.4 writes the plan artifact, plan-enforce runs a structured self-review checklist, fixes any issues found, and repeats — exits only when 0 findings or max iterations reached
- Outcome: plans ship already reviewed; no manual re-check cycle needed

## Body

New section **§2.4.5 — Self-Review Loop** inserts between §2.4 (Write the artifact) and §2.5 (Quality gate before ExitPlanMode).

### Review checklist (per iteration)

| ID | Check | Scope | Fix if failed |
|----|-------|-------|---------------|
| R1 | Every file referenced in Steps exists in Reads or Writes | All phase runbooks | Add missing path to Reads or Writes |
| R2 | Every ⬜ verification item traces to exactly one phase Output | `plan.md` | Add Output to runbook or remove orphaned ⬜ |
| R3 | No ambiguous Step verbs (`add appropriate`, `handle`, `consider`, `update as needed`) | All phase runbooks | Replace with concrete command or value |
| R4 | Every Gate is a concrete, verifiable condition (no subjective language) | All phase runbooks | Rewrite Gate with exact command / expected output |
| R5 | Every Abort condition is concrete (not `if something goes wrong`) | All phase runbooks | Rewrite with specific trigger |
| R6 | Phase ordering has no circular IO deps (phase N's Output not required by phase M where M < N) | Phase index table | Reorder phases or split |
| R7 | Cross-cutting agents present when needed: UI changes → Lumen phase; dep changes → Warden phase; doc surface changes → Sentinel phase | Phase index + Body | Add phase or explicitly list in Out of scope |
| R8 | No `TBD` placeholders in Steps, Output, Gate, or Abort of any runbook | All phase runbooks | Fill with known content or escalate to user |

### Loop logic

```
max_iterations = 3
iteration = 0

loop:
  findings = run_checklist(R1..R8)
  log("[Self-review iteration {iteration+1}/3] — {len(findings)} finding(s)")
  if len(findings) == 0:
    exit loop → proceed to §2.5
  fix_all(findings)
  iteration += 1
  if iteration == max_iterations:
    halt → surface remaining findings to user, ask to resolve before ExitPlanMode
```

Max-iterations guard prevents infinite loop when a finding cannot be auto-resolved (e.g., R8 TBD that only the user can fill).

## Phase index — dispatch table

| # | Phase | Owner | Runbook | Output |
|---|-------|-------|---------|--------|
| 01 | Implement §2.4.5 self-review loop in SKILL.md | Forge 🔨 | `phase-01-forge.md` | Updated `.claude/skills/plan-enforce/SKILL.md` |
| 02 | Audit SKILL.md for consistency + edge cases | Sentinel 🛡️ | `phase-02-sentinel.md` | Inline audit report — PASS or findings list |

## Critical files / tools

- `.claude/skills/plan-enforce/SKILL.md` — file being modified (add §2.4.5)
- `plans/_template.md` — no changes
- `plans/_phase-template.md` — no changes

## Verification

- ⬜ `## 2.4.5 — Self-Review Loop` section present in SKILL.md between §2.4 and §2.5
- ⬜ Checklist table rows R1–R8 defined with ID / Check / Scope / Fix columns
- ⬜ Loop logic block specifies max_iterations=3, exit condition, and halt+surface condition
- ⬜ Sentinel audit returns PASS or all findings resolved

## Out of scope

- Changes to `scripts/validate_plan.py` — self-review is prompt-driven, not script-driven
- Modifying existing §2.5, §2.6, or §2.7 logic
- Applying self-review to Branch A (active plan resume) flow
- Adding automated test coverage for the skill

## Pending

- [branch] Current working branch is `feat/frontend/add-crt-image-figures` — Cipher dispatches Herald 📯 directly (no runbook phase) to create `feat/tooling/plan-enforce-self-review` off `main` before Phase 01 starts
