# Plan Config Schema

Defines the shape of `plan.config.yaml` consumed by `scripts/validate_plan.py`. The validator is **fully config-driven**: nothing is hardcoded. Without a config, the validator only checks that `plan.md` exists and parses as YAML frontmatter.

## Top-level keys

| Key | Required | Type | Purpose |
|---|---|---|---|
| `version` | yes | string | Schema version. Currently `"1.0"`. Validator rejects unknown versions. |
| `plan_file` | no | string | Filename of the plan header file inside the plan directory. Default: `plan.md`. |
| `phase_files` | no | object | Rules for phase file presence and ordering. Omit to skip phase-file checks. |
| `required_headers` | no | list | YAML frontmatter fields the plan file must contain. Omit to skip. |
| `required_sections` | no | list | `## headings` every phase file must contain. Omit to skip. |
| `required_blockquote_labels` | no | list | `> **Label:**` lines every phase file must contain. Omit to skip. |

Each section is independently optional. Drop a section → validator silently skips that family of checks.

---

## `phase_files`

```yaml
phase_files:
  pattern: "phase-*.md"
  number_extract_regex: '^phase-(\d+)-'
  required:
    - phase-01-forge.md
    - phase-02-herald.md
```

| Field | Required | Type | Purpose |
|---|---|---|---|
| `pattern` | yes | string | Glob matching all phase files in the plan directory. |
| `number_extract_regex` | no | string | Regex with one capture group yielding the phase number. Used for ordering and "highest written phase" logic. Default: `'^phase-(\d+)-'`. |
| `required` | no | list[string] | Exact filenames that MUST exist. Missing files with number ≤ highest-present → violation. Missing files with number > highest-present → warning (plan in progress). |

When `required` is omitted: validator checks all matched files conform to `required_sections` + `required_blockquote_labels`.

---

## `required_headers`

```yaml
required_headers:
  - name: Status
    type: enum
    allowed: [active, completed, draft]
  - name: Started
    type: string
  - name: Subject
    type: string
  - name: Layout
    type: enum
    allowed: ["single-file", "subfolder pattern"]
```

| Field | Required | Type | Purpose |
|---|---|---|---|
| `name` | yes | string | YAML frontmatter key in the plan file. |
| `type` | yes | string | One of: `string`, `int`, `datetime`, `enum`. |
| `format` | conditional | string | strftime format for `datetime` type. |
| `allowed` | conditional | list | Allowed values for `enum` type. |
| `regex` | no | string | Additional pattern check applied to the raw string value. |

**Type semantics:**
- `string` — present and non-empty.
- `int` — parses as integer.
- `datetime` — parses against `format`. Placeholders (`<...>`, contain `Y`) skip the check.
- `enum` — value must be in `allowed`.

Missing field → `HEADER-MISSING: <name>`. Type mismatch → `HEADER-TYPE: <name> expected <type>, got <value>`.

---

## `required_sections`

```yaml
required_sections:
  - Owner
  - Pre
  - Reads
  - Writes
  - Steps
  - Output
  - Gate
  - Abort conditions
```

List of `## heading` strings. Every phase file matched by `phase_files.pattern` must contain each heading exactly (case-sensitive, leading `## ` stripped). Missing → `MISSING-SECTION: <file> is missing ## <name>`.

---

## `required_blockquote_labels`

```yaml
required_blockquote_labels:
  - Owner
  - Pre
```

Match pattern: `^>\s+\*\*(\w[\w\s-]*):\*\*` per line. Every phase file must contain each label. Missing → `MISSING-SECTION: <file> is missing **<name>:**`.

Note: the plan-enforce `_phase-template.md` uses `## headings` for all 8 mandatory sections (Owner, Pre, Reads, Writes, Steps, Output, Gate, Abort conditions). Use `required_sections` for those. Reserve `required_blockquote_labels` for legacy or custom phase formats that use `> **Label:**` style.

---

## Validator CLI

```
python scripts/validate_plan.py <plan_dir> [--config <path>] [--phase NN]
```

| Arg | Purpose |
|---|---|
| `plan_dir` | Directory containing `plan.md` (or `plan_file` per config) and phase files. |
| `--config <path>` | Path to `plan.config.yaml`. If omitted, validator looks for `<plan_dir>/plan.config.yaml`. If still absent, validator only checks the plan file exists and parses as YAML frontmatter (no schema checks). |
| `--phase NN` | Validate only `phase-NN-*.md` plus header. Useful for per-phase gate checks. |

Exit codes:
- `0` — all violations cleared. Warnings printed to stderr but do not affect exit.
- `1` — one or more violations.

---

## Minimal valid config

```yaml
version: "1.0"
phase_files:
  pattern: "phase-*.md"
```

This config makes the validator check:
- `plan.md` exists and parses as YAML frontmatter
- Any `phase-*.md` files in the directory

Nothing else is enforced. Useful as a starting point.

---

## Config auto-discovery

The plan-enforce skill auto-discovers config in this order (first match wins):

1. `plans/<task-slug>-YYYYMMDD/plan.config.yaml` — per-plan override
2. `plans/_plan-config.yaml` — project-wide default
3. None → skip validation silently

To opt into project-wide validation, copy `references/example-config-plan.yaml` to `plans/_plan-config.yaml` and adjust.
