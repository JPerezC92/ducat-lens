# Phase 11 — Consolidation: merge task-runbook into plan-enforce, strip incident concepts

## Owner

Forge 🔨 (Implementation Agent) for validator refactor + Cipher 🔓 (L2 Lead) for skill SKILL.md + plan + workspace ops.

## Pre

- User directive 2026-05-24: tools must be project-agnostic dev tooling. ducat-lens is pure-dev (Atrium 🏛️ / Bastion 🧱 / Crucible 🔥 / Forge 🔨 / Herald 📯 / Lumen ✨ / Sentinel 🛡️ / Warden 🔒 / Augur 🔮 / Marshal 🎖️). No incident agents. task-runbook conceptually incident-shaped — must be collapsed into plan-enforce.
- Phases 04, 05, 06 marked superseded but retained as history in plan.md.
- Eval workspace already archived to `plans/_archive/task-runbook-evals-20260524/` (Cipher 🔓 done).

## Reads

- `D:/projects/ducat-lens/.claude/skills/task-runbook/scripts/validate_runbook.py` — source validator (580 lines)
- `D:/projects/ducat-lens/.claude/skills/task-runbook/scripts/test_validate_runbook.py` — source tests (53 cases)
- `D:/projects/ducat-lens/.claude/skills/task-runbook/references/runbook-config-schema.md` — source schema
- `D:/projects/ducat-lens/.claude/skills/plan-enforce/SKILL.md` — destination skill
- `D:/projects/ducat-lens/plans/_template.md` + `_phase-template.md` — generic dev plan conventions to validate

## Writes

- `D:/projects/ducat-lens/.claude/skills/plan-enforce/scripts/validate_plan.py` — refactored + renamed validator
- `D:/projects/ducat-lens/.claude/skills/plan-enforce/scripts/test_validate_plan.py` — slimmed test suite (~30-40 cases)
- `D:/projects/ducat-lens/.claude/skills/plan-enforce/scripts/fixtures/plan-valid/` — fresh fixture (plan.md + 2 phase files)
- `D:/projects/ducat-lens/.claude/skills/plan-enforce/references/plan-config-schema.md` — rewritten dev-only schema doc
- `D:/projects/ducat-lens/.claude/skills/plan-enforce/references/example-config-plan.yaml` — generic plan validation config
- `D:/projects/ducat-lens/.claude/skills/plan-enforce/SKILL.md` — added § 2.6 + § 2.7 + Troubleshooting entries (Cipher 🔓 done)
- (delete) `D:/projects/ducat-lens/.claude/skills/task-runbook/` — entire skill bundle removed

## Steps

1. **Forge** moves validator + tests + fixtures (see Forge dispatch prompt in Cipher's session): strip kill_switches, sla_window, concurrent_session, Replay-candidate enum, fraction type. Rename `validate_runbook.py` → `validate_plan.py`. Move into `plan-enforce/scripts/`. Build fresh `fixtures/plan-valid/`. Update tests. Delete old fixtures + scripts at `task-runbook/scripts/`.
2. **Cipher** (post-Forge) deletes remaining task-runbook surfaces: `SKILL.md` + `evals/`. Skill bundle dir removed entirely.
3. **Cipher** updates `plan-enforce/SKILL.md` with §§ 2.6, 2.7 + Troubleshooting entries (done in this phase).
4. **Cipher** updates this bootstrap plan: phases 04-06 marked superseded; phase 11 added; Resolved decisions appended (done).
5. **Cipher** dispatches Bastion 🧱 + Crucible 🔥 + Sentinel 🛡️ audits after Forge completes.

## Output

- task-runbook skill: gone (zero files under `.claude/skills/task-runbook/`)
- plan-enforce skill bundle: `SKILL.md` + `scripts/{validate_plan.py, test_validate_plan.py, fixtures/plan-valid/}` + `references/{plan-config-schema.md, example-config-plan.yaml}`
- All references in `CLAUDE.md` / `plan.md` updated to mention `plan-enforce/scripts/validate_plan.py`, never `validate_runbook.py`
- Eval evidence preserved at `plans/_archive/task-runbook-evals-20260524/`

## Gate

- `ls .claude/skills/task-runbook/` returns "No such file or directory"
- `pytest .claude/skills/plan-enforce/scripts/test_validate_plan.py -v` exits 0
- `python .claude/skills/plan-enforce/scripts/validate_plan.py .claude/skills/plan-enforce/scripts/fixtures/plan-valid --config .claude/skills/plan-enforce/references/example-config-plan.yaml` exits 0
- `grep -rE "kill|sla|concurrent|fraction|replay|belcorp|sdp|incident" .claude/skills/plan-enforce/` returns zero hits in code + comments
- Bastion 🧱 PASS on refactored validator + tests
- Crucible 🔥 PASS on slimmed test pyramid
- Sentinel 🛡️ PASS on updated plan-enforce SKILL.md

## Abort conditions

- Renaming a `validate_runbook.py` symbol breaks a still-needed CLI flag → halt, document
- Stripping `fraction` type breaks an unrelated test that still passes → keep the type but mark as "unused; reserved for future"
- Schema doc rewrite leaves a doc-test failing → fix doc-test or remove
- Forge declares done but root `validate_runbook.py` still exists (regression of phase 04 cleanup) → halt, delete
- Sentinel 🛡️ flags more than 2 critical violations in plan-enforce SKILL.md → halt, fix before continuing

## MCP whitelist/blacklist

- Allowed: Read, Glob, Grep, Edit, Write, Bash (file moves + pytest invocation), Agent (Forge + auditors dispatch)
- Forbidden: WebFetch, WebSearch
