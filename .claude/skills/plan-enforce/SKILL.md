---
name: plan-enforce
description: Enforce plan-first discipline for non-trivial tasks. Creates a subfolder plan artifact in plans/ (plan.md + per-phase runbooks) from the project template by default; single-file layout only as narrow exception. Resumes existing active plan when found. Use when the user asks to plan something, types /plan, or when Cipher 🔓 (Dev-Team Orchestrator) is about to dispatch Forge 🔨 (Implementation Agent) for any implementation task. ALWAYS invoke this skill before any code-writing work begins.
disable-model-invocation: false
argument-hint: "task description (e.g. 'migrate auth module' or 'fix pedido null bug')"
metadata:
  author: Philip Perez Castro
  version: 1.2.0
---

## Purpose

Enforce the `plans/` directory as the single source of truth for all non-trivial tasks.
Every implementation task must have a plan artifact under `plans/` before work begins.
This skill creates that artifact (or resumes an existing active one), validates it against an optional schema, and surfaces it via `ExitPlanMode`.

**Bundled validator:** `scripts/validate_plan.py` — config-driven, project-agnostic. Auto-invoked before `ExitPlanMode` when a config is present. See § 2.6 + `references/plan-config-schema.md`.

**Default to **subfolder**.** Single-file is a narrow exception (see § 2.1).

- **Subfolder** (default): `plans/<task-slug>-YYYYMMDD/plan.md` + `phase-NN-<owner>.md` siblings
- **Single-file** (exception only): `plans/<task-slug>-YYYYMMDD.md` — only when ALL five strict criteria in § 2.1 pass

## When to Trigger

- User types `/plan` or says "plan X", "make a plan for X", "create a plan"
- Cipher 🔓 (Dev-Team Orchestrator) is about to dispatch Forge 🔨 (Implementation Agent) for any code-writing task
- User asks "what's the plan?", "show the current plan", "resume the plan"
- Keywords: "plan", "planear", "planning", "antes de empezar", "forge", "implementar"

## Arguments

From `$ARGUMENTS`, extract:
- **task-description** — free-text description of what will be done (e.g. "migrate auth module")

If not provided and no active plan found, ask the user for a 1-sentence task description.

---

# SECTION 1: CHECK FOR ACTIVE PLAN

Two sources to scan:
1. `Glob "plans/*.md"` — single-file plans (excluding `plans/_template.md`)
2. `Glob "plans/*/plan.md"` — subfolder plans

For each result, use `Read` to check if the file contains `Status: active`.

**Branch A — Active plan found:**
- Read the full plan file.
- If subfolder pattern detected (path matches `plans/*/plan.md`), also `Glob "plans/<found-subfolder>/phase-*.md"` to list runbook siblings.
- Show a summary to the user:

```
┌─ Active Plan ──────────────────────────────────────
│ Layout:  single-file | subfolder
│ Path:    plans/<filename> | plans/<task-slug>-YYYYMMDD/
│ Subject: <Subject line from metadata>
│ Started: <Started date>
│ Open verification items: <count of ⬜ items>
│ Phase runbooks: <list if subfolder>
└─────────────────────────────────────────────────────
Continuing this plan. Type "new plan" to start a fresh one.
```

- **Scope drift check:** if the active plan is single-file but the current task context is non-trivial (≥2 phases, ≥2 agents, or cross-file edits), warn the user and offer to upgrade to subfolder. Show:

```
┌─ Active Plan ──────────────────────────────────────
│ Layout:  single-file ⚠️ scope drift detected
│ Path:    plans/<filename>
│ Subject: <Subject>
│ Warning: task now requires ≥2 phases / ≥2 agents / cross-file edits.
│ Recommend: upgrade to subfolder before resuming.
└─────────────────────────────────────────────────────
Type "upgrade plan" to create subfolder layout. Type "continue" to proceed as-is.
```

- Proceed to Section 3 (ExitPlanMode) with this plan's content.

**Branch B — No active plan:**
- Proceed to Section 2 (create new plan).

---

# SECTION 2: CREATE NEW PLAN

> **HARD RULE — anti-improvisation:** Plans must give the agent a complete execution path. Agent improvisation forbidden — every command, file, gate must be explicit.

## 2.1 — Decide layout

**Default to **subfolder**.** Use single-file ONLY when ALL of:
- 1 owner agent total — no cross-agent handoffs
- ≤ 30 lines of total instructions — fits without phase isolation
- No phase IO contracts — no phase's output is another phase's input
- No external state mutation — no external service writes (DB, auth, third-party APIs), no multi-service coordination, no git operations beyond a single commit
- No risk of agent improvisation — instructions fit a single shell command or single file edit

If ANY criterion fails → subfolder.

If unsure → default subfolder, never single-file.

## 2.2 — Derive slug and path

- **task-slug**: lowercase kebab-case from `$ARGUMENTS` or user-provided description.
  - Strip articles, conjunctions, punctuation.
  - Max 5 words. Examples: `migrate-auth-module`, `fix-pedido-null`, `sb-gana-oferta-tallaje`.
- **date**: today's date in `YYYYMMDD` format (read from system context or `currentDate` memory).
- **Subfolder path** (default): `plans/<task-slug>-<date>/` containing `plan.md` + `phase-NN-<owner>.md` siblings
- **Single-file path** (exception): `plans/<task-slug>-<date>.md`

## 2.3 — Gather section content

Before writing, collect from the current conversation.

**Subfolder content table** (default):

| Section | Source |
|---|---|
| Subject | 1-sentence task description from user or `$ARGUMENTS` |
| Prompted by | Ticket ID, user request, or feature ask — from conversation |
| Goal | What done looks like (observable outcome) |
| Body | Cross-phase task overview (tables/bullets, not prose) |
| Phase index — dispatch table | One row per `phase-NN-*.md` (# / Phase / Owner / Runbook / Output) |
| Source of truth chain *(optional)* | Ordered list of data sources the script/agent reads |
| Critical files / tools | Files already identified, MCP tools needed, skills to invoke |
| Verification | One ⬜ per phase output |
| Out of scope | Anything explicitly NOT included |
| Pending *(optional)* | Blocked/waiting items that need user action before work resumes |
| Resolved decisions *(optional)* | Append-only log of locked choices with date stamps |

**Single-file content table** (exception only):

| Section | Source |
|---|---|
| Subject | 1-sentence task description |
| Prompted by | Ticket ID / user request |
| Goal | Observable outcome |
| Body | All steps inline (≤ 30 lines total) |
| Critical files / tools | Paths |
| Verification | One ⬜ per Body line item |
| Out of scope | Bullets |

If any required section has no information yet, write `TBD` — never leave placeholder `{...}` syntax.

## 2.4 — Write the artifact

**Subfolder (default):**
1. Copy `plans/_template.md` → `plans/<task-slug>-<date>/plan.md`
2. Copy `plans/_phase-template.md` → one `phase-NN-<owner>.md` per agent dispatch
3. Fill phase index table in `plan.md` with one row per `phase-NN-*.md`
4. Each runbook MUST have all 8 mandatory sections filled (no `TBD` placeholders for Steps / Output / Gate / Abort):
   - **Owner** (single agent or `agent-A → agent-B` chain)
   - **Pre** (what must be true)
   - **Reads** / **Writes** (file paths)
   - **Steps** (numbered, command-level)
   - **Output** (concrete artifact path + schema)
   - **Gate** (verification before next phase)
   - **Abort conditions** (when to halt)
   - **MCP whitelist/blacklist** (optional — required for read-only phases that touch external systems, e.g. production databases, third-party APIs)
5. Intermediate artifacts (CSV/JSON/TXT/audit reports) land in same subfolder with `_` prefix; no file-count cap
6. Wording rule: "If unsure → subfolder, never single-file"

**Single-file (exception only):** Copy `plans/_template.md` → `plans/<task-slug>-<date>.md`. Allowed ONLY when § 2.1 strict criteria all pass. Otherwise reject and fall through to subfolder. Fill all sections. Set:
- `Status: active`
- `Started: <today YYYY-MM-DD HH:MM>`
- `Subject: <one-line task description>`

## 2.5 — Quality gate before ExitPlanMode

Before calling `ExitPlanMode`, verify:

- Reject thin plans: every ⬜ verification item must trace to a phase runbook Output (subfolder) or a Body line item (single-file)
- Reject any phase runbook with empty/`TBD` Steps, Output, Gate, or Abort sections
- Reject any plan with > 0 phases but no `## Phase index` table in `plan.md`
- If quality gate fails → halt, ask user for missing content

## 2.6 — Validate plan via bundled script (auto-invoke)

After § 2.5 content checks pass, auto-invoke `scripts/validate_plan.py` against the new plan directory. The validator is config-driven — schema lives in `references/plan-config-schema.md`.

**Config auto-discovery** (first match wins, silent fallback):
1. `plans/<task-slug>-YYYYMMDD/plan.config.yaml` (per-plan override)
2. `plans/_plan-config.yaml` (project-wide default)
3. None → skip validation silently (script exits 0 with no checks)

**Invocation:**
```bash
python .claude/skills/plan-enforce/scripts/validate_plan.py plans/<task-slug>-YYYYMMDD/ [--config <path>]
```

Single-file plans pass the file's parent dir; script auto-detects single-file vs subfolder layout.

**Per-phase mode** (optional, used by Cipher 🔓 (Dev-Team Orchestrator) when advancing phase by phase):
```bash
python .claude/skills/plan-enforce/scripts/validate_plan.py plans/<task-slug>-YYYYMMDD/ --phase 03
```

Validates only `phase-03-*.md` + header. Used at phase-advance boundaries.

**Behavior:**
- Exit 0 → proceed to Section 3 (ExitPlanMode)
- Exit non-zero → halt; surface validator stderr to user; ask whether to fix the offending field or relax the config

**Reference example config:** `references/example-config-plan.yaml` — validates plan-enforce's own template conventions (Status / Started / Subject / Layout headers + 8 mandatory phase sections per `_phase-template.md`).

## 2.7 — Active plan re-validation (Branch A)

When § 1 detects an active plan, also auto-invoke `validate_plan.py` on the existing plan dir before showing the resumption block. This catches drift (e.g. a phase runbook with empty Steps section that was added since last session). Same exit-code semantics as § 2.6.

---

# SECTION 3: EXIT PLAN MODE

Call `ExitPlanMode` with the full plan content rendered as markdown.

The rendered output becomes the user-visible plan artifact. Ensure:
- Status header is visible at top
- Verification checklist shows all ⬜ items
- Pending section present only if there are blocked items

---

## Plan Lifecycle Rules

These rules apply after the plan is created — Cipher 🔓 (Dev-Team Orchestrator) enforces them throughout the task. For subfolder layout, "plan file" = `plan.md`; phase runbooks are append-only references.

| Event | Action |
|---|---|
| Step completes | Mark ⬜ → ✅ in `plan.md` (subfolder) or single-file `Verification` checklist |
| Scope change | Update Body + Verification in `plan.md`; if a phase scope changes, also update that `phase-NN-<owner>.md` |
| New phase added (subfolder) | Append row to `plan.md` `## Phase index` + write new `phase-NN-<owner>.md` sibling |
| Task done | Set `Status: completed`, add `Completed: YYYY-MM-DD HH:MM` in `plan.md` (or single file) |
| New Forge dispatch | Run Section 1 check — never dispatch Forge without an active plan |
| Mid-task scope grows beyond single-file criteria | Upgrade in place: create subfolder, move single-file content into new `plan.md`, author missing runbooks before resuming |

---

## Examples

**Example 1:** User types `/plan migrate auth module`
- Slug: `migrate-auth-module`
- Layout decision: subfolder (multi-file edits, ≥2 phases) — default
- Creates: `plans/migrate-auth-module-20260520/plan.md` + `phase-01-forge.md`, `phase-02-herald.md`
- Result: phase index table filled, each runbook has all 8 sections, ExitPlanMode called

**Example 2:** User says "let's implement the PROL limit validation skill"
- Cipher 🔓 (Dev-Team Orchestrator) checks plans/ → no active plan
- Slug: `prol-limite-venta-skill`
- Layout decision: subfolder (implementation task, code-writing → cross-file) — default
- Creates: `plans/prol-limite-venta-skill-20260520/plan.md` + `phase-01-forge.md`
- Result: plan written, ExitPlanMode called

**Example 3:** User says "what's the current plan?" with an existing active plan
- Section 1 finds `plans/migrate-auth-20260514/plan.md` with `Status: active`
- Shows summary block, calls ExitPlanMode with existing content

**Example 4:** Cipher 🔓 (Dev-Team Orchestrator) is about to dispatch Forge 🔨 (Implementation Agent)
- Section 1 check runs first
- If no active plan: Section 2 creates subfolder plan before Forge is dispatched
- Forge dispatch is blocked until ExitPlanMode confirms plan exists

**Example 5:** Multi-phase migration (canonical subfolder use case)
- User says: "reorganize 189 ticket folders across 9 phases with 5 agents"
- Layout decision: subfolder — default (≥4 phases, ≥3 agents, phase IO contracts)
- Slug: `reorganize-tickets-folder-names`
- Creates: `plans/reorganize-tickets-folder-names-20260519/plan.md` + 10 `phase-NN-<owner>.md` siblings
- Cipher 🔓 (Dev-Team Orchestrator) dispatches each phase by passing exact runbook path: `Agent(subagent_type="forge", prompt="Read plans/reorganize-tickets-folder-names-20260519/phase-2a-forge.md and execute")`

**Example 6:** Genuinely trivial single-file exception
- User says: "add a comment to line 5 of scripts/validate_skills.py explaining the regex"
- Layout decision: single-file (1 agent, 1 file edit, ≤5 lines of instructions, no IO contracts, no state mutation, no improvisation risk) — ALL five criteria pass
- Creates: `plans/add-validate-comment-20260520.md`
- Body is ≤30 lines; Verification has 1 ⬜ item; ExitPlanMode called

---

## Troubleshooting

**No `plans/` directory found:**
- Cause: directory does not exist yet
- Fix: create it with `mkdir plans` before writing the plan file

**Multiple active plans found:**
- Cause: prior task not marked completed
- Fix: show all active plans (both single-file `plans/*.md` AND subfolder `plans/*/plan.md`) to user, ask which to continue or whether to mark old ones completed first

**Subfolder active but phase runbooks missing:**
- Cause: `plan.md` created but per-phase runbooks not yet authored
- Fix: list missing phases from the phase index table in `plan.md`; ask user whether to author missing runbooks before dispatching agents

**`ExitPlanMode` not available (wrong context):**
- Cause: skill invoked outside plan mode
- Fix: write the plan file to disk anyway, then display the content inline as a fenced markdown block. Notify user that plan is saved at `plans/<filename>` for reference.

**Thin plan rejected by quality gate (§ 2.5):**
- Cause: ⬜ verification item has no matching phase Output / Body line item; OR phase runbook has empty Steps/Output/Gate/Abort.
- Fix: list each unbacked ⬜ item; ask user to either flesh out the corresponding phase runbook or remove the ⬜ item.

**Single-file plan flagged as scope drift:**
- Cause: active single-file plan now requires ≥2 phases / ≥2 agents / cross-file edits.
- Fix: run upgrade flow — `mkdir plans/<slug>-<date>/`, move file → `plan.md`, author phase runbooks, resume.

**Phase runbook missing `_phase-template.md` sections:**
- Cause: hand-written runbook lacks Owner / Pre / Reads / Writes / Steps / Output / Gate / Abort.
- Fix: open `_phase-template.md`, copy missing sections, populate before dispatch.

**Validator exits 1 after scaffold:**
- Cause: `scripts/validate_plan.py` (auto-invoked in § 2.6) found a violation in the just-scaffolded plan.
- Fix: read stderr from the validator; the violation cites the exact file + missing field / section. Either fill the missing content (preferred — content was probably skipped by mistake) or relax the config (if the rule shouldn't apply to this plan).

**No plan config present:**
- Cause: neither `plans/<slug>/plan.config.yaml` nor `plans/_plan-config.yaml` exists.
- Fix: not an error — validator silently skips. To opt into validation, copy `references/example-config-plan.yaml` to `plans/_plan-config.yaml` and adjust.

**Validator script missing or broken:**
- Cause: `scripts/validate_plan.py` failed to invoke (Python not installed, syntax error, missing pyyaml).
- Fix: report the Python error to the user; do NOT block `ExitPlanMode` on a broken validator. The plan content quality gate (§ 2.5) is the load-bearing check; § 2.6 is supplementary.
