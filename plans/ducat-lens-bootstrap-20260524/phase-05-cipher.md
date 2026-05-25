# Phase 05 — Draft `task-runbook` SKILL.md

## Owner

Cipher 🔓 (L2 Lead) — skill drafting is Cipher-direct (not Forge; not a code task, not Marshal; not an agent spec)

## Pre

- Validator config schema locked (phase 04 dependency for spec wording, but does not block — schema doc exists)
- Source sources analyzed (see plan `## Resolved decisions` + prior transcript audit)
- skill-creator workflow understood (see `claude-api:skill-creator` SKILL.md)

## Reads

- `D:/projects/ducat-lens/.claude/skills/sdp-runbook/SKILL.md` — primary source for feature extraction
- `D:/projects/ducat-lens/.claude/skills/plan-enforce/SKILL.md` — overlap reference + section-structure style
- `D:/projects/ducat-lens/.claude/skills/git-commit/SKILL.md` — short-form SKILL.md style reference
- `D:/projects/ducat-lens/.claude/skills/task-runbook/references/runbook-config-schema.md` — validator hook interface

## Writes

- `D:/projects/ducat-lens/.claude/skills/task-runbook/SKILL.md`

## Steps

1. **Frontmatter.** Fields: `name: task-runbook`, `description` (pushy, lists trigger contexts: "starting new investigation task with prior art catalog", "scaffolding incident/feature/scan runbook", "skill works in any project that has a prior-art directory and a runbook template"), `argument-hint: "task-id [optional prior-art-dir] [optional template-dir]"`, `disable-model-invocation: false`, `metadata: {author, version: 1.0.0}`.
2. **Purpose section.** 3-5 lines. Generalize sdp-runbook purpose stripped of incident-specific terms.
3. **When to Trigger section.** List 4-6 trigger conditions. Avoid Belcorp / SDP / Activo / ticket terms. Example triggers: "user provides task identifier and project has a prior-art directory", "user types `/task-runbook <id>`", "Cipher 🔓 about to dispatch implementing agent for a task that may have been done before".
4. **Arguments section.** Document `task-id` (required), and optional config knobs: prior-art-dir, template-dir, output-dir, validator-config. All extractable from `$ARGUMENTS` or project conventions.
5. **Section 1 — Read task context.** Skill expects the orchestrator (Cipher 🔓) to have already read whatever task spec exists (ticket, issue, feature request, scan brief). Skill itself does NOT fetch external resources; it consumes a task-id + identifying metadata passed in.
6. **Section 2 — Prior-art search.** Configurable sources ordered list. Default sources Glob from project root:
   - `problems/**/*.md` (curated past cases)
   - `knowledge/patterns.md` (recurring failure modes register)
   - `docs/decisions/*.md` (ADR-style records)
   - `<prior-art-dir>/*.md` if passed
   - RAG / semantic-search MCP only as fallback (threshold ≥0.85)
   Match criterion: ≥2 of (identifier-field, module-field, symptom-keywords) align. Configurable via skill args.
7. **Section 3 — Verdict ladder.** Reproduce 3-tier ladder from sdp-runbook generalized:
   - `replay-yes` — exact match → halt, return finding, skip scaffold
   - `replay-structural` — pattern match w/ different identifying values → scaffold partial (skip "frame hypothesis" phase, run "validate" phase with adapted queries)
   - `replay-no` — novel → full scaffold
8. **Section 4 — Scaffold runbook.** Copy from `<template-dir>` (default: `runbook-templates/` if present in repo root, else error). Write to `<output-dir>/<task-id>/runbook/`. Initialize `runbook.md` header per project config. Skip when verdict is `replay-yes`.
9. **Section 5 — Validate scaffold.** Optional. Invoke `.claude/skills/task-runbook/scripts/validate_runbook.py <runbook_dir> --config <path>` if a `runbook.config.yaml` exists in the runbook dir or in repo root. Skip silently otherwise.
10. **Section 6 — Hand-off signal.** Skill does NOT dispatch other agents. Skill reports: verdict, runbook path (or none), validator status (or none), recommended next action. Cipher 🔓 owns dispatch decisions.
11. **Examples section.** 3 examples:
    - `replay-yes`: exact match found, finding block returned, no scaffold
    - `replay-structural`: pattern match, partial scaffold, hand-off block returned
    - `replay-no`: novel task, full scaffold, validator runs clean, hand-off block returned
12. **Troubleshooting section.** 4-5 entries covering: missing template-dir, missing prior-art-dir, validator fails, ambiguous match between 2 prior-art entries, RAG MCP unavailable.
13. **Length target.** ≤300 lines. If overshooting, push detail into `references/` files (e.g. `references/prior-art-search-strategies.md`).
14. **Style audit.** No Belcorp / SDP / Activo / ticket / Quill / Ledger / Atlas / Ember / Ranger / Lex / Gate / Vault / Scribe references. Grep before declaring done.

## Output

- `.claude/skills/task-runbook/SKILL.md` — ≤300 lines, agnostic, references the config schema for validator hook

## Gate

- `grep -E "Belcorp|SDP|Activo|ticket|Quill|Ledger|Atlas|Ember|Ranger|Lex|Gate|Vault|Scribe" .claude/skills/task-runbook/SKILL.md` returns zero hits
- SKILL.md frontmatter parses as valid YAML
- All 11 sections present (Purpose, When to Trigger, Arguments, Section 1-6, Examples, Troubleshooting)
- Sentinel 🛡️ audit PASS on SKILL.md (dev-side markdown rules apply)

## Abort conditions

- Generalization breaks coherence (skill becomes too vague to trigger reliably) → escalate to Cipher 🔓; consider narrower repurpose (e.g. "feature-runbook" instead of fully agnostic)
- Verdict-ladder semantics cannot survive generalization (e.g. `structural` requires domain-specific phase skip logic) → halt, ask Cipher 🔓 to drop structural tier or document as opt-in

## MCP whitelist/blacklist

- Allowed: Read, Glob, Grep, Write
- Forbidden: Edit (write-once draft), Bash, WebFetch, WebSearch
