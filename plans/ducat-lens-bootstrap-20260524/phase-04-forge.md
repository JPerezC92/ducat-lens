# Phase 04 — Refactor `validate_runbook.py` to config-driven

## Owner

Forge 🔨 (Implementation Agent)

## Pre

- Validator config schema written: `.claude/skills/task-runbook/references/runbook-config-schema.md` v1.0
- Example configs exist: `example-config-belcorp.yaml`, `example-config-minimal.yaml`
- Original validator present at project root: `D:/projects/ducat-lens/validate_runbook.py`
- Python ≥3.10 + `pyyaml` available (no other dependencies allowed without Warden gate)

## Reads

- `D:/projects/ducat-lens/validate_runbook.py` — original Belcorp validator (635 lines)
- `D:/projects/ducat-lens/.claude/skills/task-runbook/references/runbook-config-schema.md` — schema spec
- `D:/projects/ducat-lens/.claude/skills/task-runbook/references/example-config-belcorp.yaml` — full-fidelity Belcorp config
- `D:/projects/ducat-lens/.claude/skills/task-runbook/references/example-config-minimal.yaml` — minimal config

## Writes

- `D:/projects/ducat-lens/.claude/skills/task-runbook/scripts/validate_runbook.py` — refactored, config-driven
- `D:/projects/ducat-lens/.claude/skills/task-runbook/scripts/test_validate_runbook.py` — pytest test suite
- `D:/projects/ducat-lens/.claude/skills/task-runbook/scripts/fixtures/runbook-belcorp-valid/` — integration test fixture: complete runbook conforming to belcorp config
- `D:/projects/ducat-lens/.claude/skills/task-runbook/scripts/fixtures/runbook-minimal-valid/` — integration test fixture: conforming to minimal config
- (delete) `D:/projects/ducat-lens/validate_runbook.py` — root copy removed at end

## Steps

1. **Move** original `validate_runbook.py` to `.claude/skills/task-runbook/scripts/validate_runbook.py`. Verify file copies cleanly (byte-identical).
2. **Add CLI arg** `--config <path>`. Loading order:
   - `--config <path>` if provided
   - `<runbook_dir>/runbook.config.yaml` if present
   - `None` (validator only checks `runbook_file` exists and parses as YAML frontmatter; no schema checks)
3. **Replace hardcoded constants with config lookups.** Map each hardcoded constant in the original to its config equivalent:
   - `REQUIRED_PHASE_FILES` → `config.phase_files.required`
   - `REQUIRED_PHASE_SECTIONS` → `config.required_sections`
   - `REQUIRED_BLOCKQUOTE_LABELS` → `config.required_blockquote_labels`
   - `KILL_MAX_HYPOTHESES` / `KILL_MAX_QUERIES` / `KILL_MAX_RERUNS` → `config.kill_switches[].max`
   - `SLA_WARN_PCT` → `config.sla_window.warn_pct_remaining`
   - 600-second concurrent threshold → `config.concurrent_session.warn_seconds`
   - `ALLOWED_REPLAY_CANDIDATE_VALUES` → `config.required_headers[].allowed` for enum-typed fields
   - 7 hardcoded `required_keys` in `parse_runbook_header` → `config.required_headers[].name`
4. **Generalize header type checking.** Add a `_validate_header_value(value, spec)` helper that dispatches on `spec.type` (`string` / `int` / `datetime` / `enum` / `fraction`). Apply to every entry in `config.required_headers`.
5. **Generalize kill-switch loop.** Replace 3 hardcoded `try/except` blocks with a single loop over `config.kill_switches`. Each item: read `header_field`, parse per `type`, compare against `max`, emit `<violation_code>: <name> cap exceeded`.
6. **Skip-if-absent rule.** When a config section is absent (e.g. no `kill_switches` key), the corresponding check family produces zero violations and zero warnings. Tested explicitly in step 8.
7. **Preserve exit codes.** `0` = pass (warnings allowed). `1` = ≥1 violation. Per-phase mode (`--phase NN`) unchanged: validates header + that one phase file.
8. **Write pytest suite** (`test_validate_runbook.py`). Test classes:
   - `TestConfigLoading` — load belcorp example, load minimal example, no config (legal), malformed YAML (error), unsupported version (error)
   - `TestHeaderValidation` — int / datetime / enum / fraction types each with valid + invalid samples
   - `TestPhaseFiles` — required-list violations, highest-present logic, glob-only mode (no required list)
   - `TestSections` — missing `##` heading, missing blockquote label, all sections present
   - `TestKillSwitches` — under-cap, at-cap, over-cap, missing field, malformed fraction
   - `TestSlaWindow` — over threshold (warn), under threshold (no warn), placeholder (skip)
   - `TestConcurrentSession` — recent update (warn), old update (no warn)
   - `TestIntegrationFixtures` — run validator end-to-end on `fixtures/runbook-belcorp-valid/` with `example-config-belcorp.yaml` (exit 0); on `fixtures/runbook-minimal-valid/` with `example-config-minimal.yaml` (exit 0)
9. **Create fixtures.** Each fixture: a `runbook.md` with valid YAML frontmatter per its config + 1-2 `phase-NN-*.md` files with all required sections + blockquote labels.
10. **Run tests.** `cd .claude/skills/task-runbook/scripts && python -m pytest test_validate_runbook.py -v`. All pass.
11. **Delete root copy** `rm D:/projects/ducat-lens/validate_runbook.py`.

## Output

- Refactored validator at `.claude/skills/task-runbook/scripts/validate_runbook.py` (~700 lines after refactor, +pytest suite)
- pytest suite ≥25 test cases, all green
- 2 fixture runbook dirs that exercise both example configs
- Root `validate_runbook.py` deleted

## Gate

- `pytest test_validate_runbook.py -v` exits 0
- `python validate_runbook.py fixtures/runbook-belcorp-valid --config ../references/example-config-belcorp.yaml` exits 0
- `python validate_runbook.py fixtures/runbook-minimal-valid --config ../references/example-config-minimal.yaml` exits 0
- `python validate_runbook.py fixtures/runbook-belcorp-valid` (no config, falls through to legacy `runbook.config.yaml` lookup in dir — should also pass if fixture ships its own config)
- Original Belcorp behavior reproducible end-to-end via `example-config-belcorp.yaml` (sanity-check: violation messages, kill-switch codes, SLA-WARN message format all match the original validator's output strings)
- Bastion 🧱 audit PASS on backend (Python) rules
- Crucible 🔥 audit PASS on test pyramid

## Abort conditions

- A hardcoded constant in the original cannot be mapped cleanly to a config field → escalate to Cipher 🔓 to extend schema (and re-version v1.0 → v1.1)
- pytest suite reveals the original validator had undocumented behavior (e.g. silent edge cases) → halt, document, ask Cipher 🔓 whether to preserve or change behavior in refactor
- Bastion 🧱 returns >3 critical violations → halt, fix before continuing

## MCP whitelist/blacklist

- Allowed: Read, Glob, Grep, Edit, Write, Bash (for pytest invocation + file moves)
- Forbidden: WebFetch, WebSearch (no external deps)
