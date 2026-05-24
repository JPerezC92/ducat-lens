---
Status: active
Started: 2026-01-15 09:00
Subject: Example plan for validator fixture
Layout: subfolder pattern
---

# Plan — Example plan for validator fixture

## Context

- Prompted by: validator integration test
- Goal: confirm validate_plan.py exits 0 on a well-formed plan directory
- Outcome: green integration test in test_validate_plan.py

## Body

| Task | Owner | Output |
|---|---|---|
| Phase 01 | Forge | Implementation artifact |
| Phase 02 | Cipher | Review sign-off |

## Phase index — dispatch table

| # | Phase | Owner | Runbook | Output |
|---|---|---|---|---|
| 1 | Implementation | Forge | `phase-01-forge.md` | `output/artifact.txt` |
| 2 | Review | Cipher | `phase-02-cipher.md` | Sign-off confirmation |

## Critical files / tools

- `phase-01-forge.md`
- `phase-02-cipher.md`

## Verification

- ⬜ Phase 01 artifact produced and valid
- ⬜ Phase 02 review sign-off received

## Out of scope

- Deployment steps
- External system calls
