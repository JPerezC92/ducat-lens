# Research Brief — Inquisitor Test-Plan Verification Ownership

**Date:** 2026-05-25
**Prepared by:** Augur 🔮 (Senior Research Analyst)
**Requested by:** Cipher 🔓 (Dev-Team Orchestrator)
**Consumer:** Marshal 🎖️ (HR Director) — for spec and CLAUDE.md edits
**Decision locked:** Inquisitor owns test plan verification post-PR-open (Model B: coordinator + specialist dispatch)

---

## Objective

Map every test-plan command family observed across PRs #1–#5 to an existing agent with a current bash grant. Identify gaps, propose grant assignments, define Inquisitor's allowlist delta, specify the dispatch/collect/tick protocol, enumerate edge cases, and produce exact CLAUDE.md diff recommendations.

---

## Sources

| Source | Path / Reference |
|--------|-----------------|
| Bash grant registry (fact) | `D:\projects\ducat-lens\CLAUDE.md` lines 222–235 |
| Inquisitor runtime spec (fact) | `D:\projects\ducat-lens\.claude\agents\inquisitor.md` |
| Inquisitor persona (fact) | `D:\projects\ducat-lens\agents\inquisitor\profile.md` |
| Atrium spec (fact) | `D:\projects\ducat-lens\.claude\agents\atrium.md` |
| Bastion spec (fact) | `D:\projects\ducat-lens\.claude\agents\bastion.md` |
| Crucible spec (fact) | `D:\projects\ducat-lens\.claude\agents\crucible.md` |
| Forge spec (fact) | `D:\projects\ducat-lens\.claude\agents\forge.md` |
| Warden spec (fact) | `D:\projects\ducat-lens\.claude\agents\warden.md` |
| Lumen spec (fact) | `D:\projects\ducat-lens\.claude\agents\lumen.md` |
| Herald spec (fact) | `D:\projects\ducat-lens\.claude\agents\herald.md` |
| PR #1 body (fact) | `gh pr view 1 --json body` |
| PR #2 body (fact) | `gh pr view 2 --json body` |
| PR #3 body (fact) | `gh pr view 3 --json body` |
| PR #4 body (fact) | `gh pr view 4 --json body` |
| PR #5 body (fact) | `gh pr view 5 --json body` |

---

## Section 1 — Specialist-to-Command Matrix

### Command families observed in PRs #1–#5 (fact — extracted from PR bodies)

| # | Command family | Observed in PR(s) | Current owner | Grant evidence (CLAUDE.md line) |
|---|---------------|------------------|---------------|----------------------------------|
| A | `pnpm install` | #3, #4, #5 | Atrium 🏛️ (Frontend Architect) [production deps] / Crucible 🔥 (Test Architect) [test deps] | Line 231 (Atrium), Line 232 (Crucible) |
| B | `pnpm audit` | #5 | Warden 🔒 (Dependency Warden) | Line 229 |
| C | `pnpm agent-browser *` | #5 | Lumen ✨ (Visual Director) | Line 230 |
| D | `pnpm build` | #3 | **NO OWNER — gap** | Not in grant registry (proposed: Atrium 🏛️) |
| E | `pnpm dev` | #3 | **NO OWNER — gap** | Not in grant registry |
| F | `uv sync` | #4 | **NO OWNER — gap** | Not in grant registry |
| G | `uv run pytest tests/ -v` | #4 | **NO OWNER — gap** | Not in grant registry |
| H | `uv run uvicorn backend.main:app` + `curl` smoke | #4 | **NO OWNER — gap** | Not in grant registry |
| I | `uv run python -m backend.scripts.fetch_ducats` | #3, #4 | **NO OWNER — gap** | Not in grant registry |
| J | Static file existence/content check (`data/ducats.json` keys, size) | #3 | Inquisitor 🔎 (PR Reviewer) [file read tools] | Inquisitor has Read, Glob, Grep — no Bash needed |
| K | JSON-LD / SEO meta presence check on built HTML | #3 | Inquisitor 🔎 (PR Reviewer) [file read tools] | Inquisitor has Read, Grep — scans `frontend/dist/index.html` after build |
| L | Version-pin verification (`package.json`, `pyproject.toml` — no `^`/`~`/`>=`) | #4 | Inquisitor 🔎 (PR Reviewer) [file read tools] | Read + Grep against `frontend/package.json`, `backend/pyproject.toml` |
| M | Python smoke-test: `python .claude/skills/plan-enforce/scripts/test_validate_plan.py` | #1 | **NO OWNER — gap** (one-off script) | Not in grant registry |

### Disambiguation notes (fact)

- **`pnpm install`** (item A): Atrium 🏛️ (Frontend Architect) owns production + build-tooling deps; Crucible 🔥 (Test Architect) owns test-runner deps. For test-plan verification the command is always `pnpm install` with no new packages (lockfile already committed) — it is a "confirm lockfile is in sync" check. Either agent can execute it. Atrium is the natural coordinator because it owns more of the dep surface; dispatch to Atrium unless the context explicitly names test-only packages.
- **Static / file checks** (items J, K, L): these require only Read and Grep, which Inquisitor 🔎 (PR Reviewer) already holds. No new Bash grant is required. Inquisitor executes these itself without dispatching to a specialist.
- **`python .claude/skills/plan-enforce/scripts/test_validate_plan.py`** (item M): one-time PR #1 item. No ongoing pattern. Not a recurring command family. Gap noted but no grant assignment proposed for it — file it as an anomaly; Forge 🔨 (Implementation Agent)'s existing Bash grant (linter/formatter autofix scope) does not cover arbitrary Python scripts.

---

## Section 2 — Grant Gaps

### Gaps identified (fact — nothing in grant registry covers these)

| Gap | Command family | Proposed owner | Justification |
|-----|---------------|----------------|---------------|
| G1 | `pnpm build` | Atrium 🏛️ (Frontend Architect) | Atrium owns build-tooling deps and frontend build output. `pnpm build` is a frontend build command — same family as `pnpm install` for build tooling. Atrium already uses Read/Glob/Grep to verify frontend artifacts; adding `pnpm build` keeps the command family cohesive. |
| G2 | `pnpm dev` | Atrium 🏛️ (Frontend Architect) | `pnpm dev` starts the Vite/Astro dev server — a frontend build-tooling operation. Same ownership rationale as G1. Scope: start server for smoke test only; Atrium does not own the running server lifecycle beyond the test step. |
| G3 | `uv sync` | Bastion 🧱 (Backend Architect) | Bastion owns backend Python files. `uv sync` installs the backend's locked dep tree — the backend-side analogue of `pnpm install`. Bastion currently has no Bash grant (spec: `tools: Read, Glob, Grep`); adding `uv sync` is a minimal single-family extension. |
| G4 | `uv run pytest tests/ -v` | Bastion 🧱 (Backend Architect) | Running the Python test suite is backend verification work — Bastion's domain. Single family with G3 (`uv run *` within the backend working directory). |
| G5 | `uv run uvicorn backend.main:app --port <N>` + `curl -s -X POST ... http://localhost:<N>/analyze` | Bastion 🧱 (Backend Architect) | Backend server smoke test. Same `uv run *` family as G4; curl is the HTTP probe needed to verify the endpoint is reachable. Scope: start server, fire one curl, report JSON, kill server. Bastion must not leave servers running. |
| G6 | `uv run python -m backend.scripts.fetch_ducats` | Bastion 🧱 (Backend Architect) | Build-time data-fetch script lives in `backend/scripts/`. Same `uv run *` family; backend ownership is unambiguous. |

### Grant assignment conditions (per CLAUDE.md §"Bash grant registry")

All six gaps route to Bastion 🧱 (Backend Architect) or extend Atrium 🏛️ (Frontend Architect). Both satisfy the gate registry rule: single operation family, justification in Augur 🔮 (Senior Research Analyst)'s brief (this document), requires Marshal 🎖️ (HR Director) review and Sentinel 🛡️ (Quality Guardian) gate before CLAUDE.md is edited.

**Bastion grant scope proposed:** `uv sync` (within `backend/`), `uv run pytest <args>` (within `backend/`), `uv run uvicorn <args>`, `curl -s -X POST -F <args> http://localhost:<port>/analyze`, `uv run python -m backend.scripts.<script>`. All commands scoped to `backend/` working directory.

**Atrium grant scope extension proposed:** add `pnpm build` and `pnpm dev` to existing Atrium Bash grant. Current grant is `pnpm install` only; extension is same `pnpm *` family, frontend directory.

---

## Section 3 — Inquisitor Allowlist Delta

### New commands Inquisitor needs (minimal — Inquisitor coordinates, does NOT execute specialist commands)

```
gh pr view <number> --json body --jq .body
gh pr edit <number> --body-file <file>
gh pr edit <number> --body "<inline string>"
```

**Rationale:**
- `gh pr view <number> --json body --jq .body` — fetch the current PR body for parsing. This is a superset of the existing `gh pr view <number> --json title,body,files,state` grant; the `--jq` flag is a filter variant of the same command. It is additive, not a new family.
- `gh pr edit <number> --body-file <file>` — push the rewritten body (checkbox ticks + evidence) back to GitHub. This is the only state-mutation Inquisitor 🔎 (PR Reviewer) needs that Herald 📯 (Release Manager) does not own — PR body content is review evidence, not a git artifact.
- `gh pr edit <number> --body "<inline string>"` — short-form tick for single-item updates without a temp file.

**Why not Herald?** Herald 📯 (Release Manager) owns PR lifecycle (create, push, merge) but does not own review-evidence updates to the PR body. Making Herald a middleman for checkbox ticks on every test-plan item would require Inquisitor to relay specialist evidence through Cipher 🔓 (Dev-Team Orchestrator) to Herald — unnecessary round-trip that reintroduces the Cipher-forgets problem. Inquisitor writing the ticked body is the same pattern as Inquisitor already writing `gh pr comment` — it is review output, not a git operation.

**Inquisitor must NOT gain:**
- `pnpm *` — Atrium 🏛️ (Frontend Architect), Crucible 🔥 (Test Architect), Warden 🔒 (Dependency Warden) own those families
- `uv *` — Bastion 🧱 (Backend Architect) owns that family (proposed)
- `curl *` — Bastion owns that family (within the smoke-test scope above)
- Any `git *` — Herald 📯 (Release Manager) owns all git
- `gh pr merge`, `gh pr close` — Herald/user only

---

## Section 4 — Dispatch Protocol

### Preconditions
- Herald 📯 (Release Manager) has opened the PR and returned the PR URL + number to Cipher 🔓 (Dev-Team Orchestrator).
- Cipher 🔓 (Dev-Team Orchestrator) dispatches Inquisitor 🔎 (PR Reviewer) with: PR number, branch name, task context (used for scope-creep evaluation and N/A determination).

### Sequence

```
INQUISITOR ENTRY
│
├─ 1. FETCH PR BODY
│     gh pr view <N> --json body --jq .body
│     → raw_body: string
│
├─ 2. PARSE CHECKBOXES
│     Extract all lines matching /^- \[[ x]\] .+/
│     Classify each:
│       - already ticked (- [x])  → skip (already verified)
│       - unchecked (- [ ])       → needs verification
│       - struck-through / N/A comment → mark as N/A, skip
│
├─ 3. FOR EACH UNCHECKED ITEM → MAP TO SPECIALIST
│     Parse item text → command family → agent (Section 1 matrix):
│
│     "pnpm install"           → Atrium 🏛️ (Frontend Architect)
│     "pnpm build"             → Atrium 🏛️ (Frontend Architect)
│     "pnpm dev"               → Atrium 🏛️ (Frontend Architect)
│     "pnpm audit"             → Warden 🔒 (Dependency Warden)
│     "pnpm agent-browser *"   → Lumen ✨ (Visual Director)
│     "uv sync"                → Bastion 🧱 (Backend Architect)
│     "uv run pytest *"        → Bastion 🧱 (Backend Architect)
│     "uv run uvicorn * + curl"→ Bastion 🧱 (Backend Architect)
│     "uv run python -m *"     → Bastion 🧱 (Backend Architect)
│     "Verify file exists / contains key"  → Inquisitor 🔎 (PR Reviewer) self (Read/Grep)
│     "Verify package.json / pyproject.toml pins"  → Inquisitor 🔎 (PR Reviewer) self (Read/Grep)
│     "JSON-LD / SEO meta in built HTML"  → Inquisitor 🔎 (PR Reviewer) self (Read/Grep on dist/)
│     UNMATCHED               → flag as UNROUTABLE (see edge cases)
│
├─ 4. DISPATCH SPECIALISTS (parallel where independent)
│     Agent call per specialist with:
│       - Literal command to run
│       - Expected outcome (exit code 0 / output pattern / file path+size)
│       - Working directory
│     Specialist returns:
│       - PASS: exit code, relevant stdout excerpt (≤ 5 lines), artifact path if any
│       - FAIL: exit code, stderr excerpt, reason
│
├─ 5. COLLECT RESULTS
│     For each item: (item_text, agent, outcome, evidence_snippet)
│
├─ 6. REWRITE BODY FILE
│     Read raw_body again (in case PR was updated during dispatch)
│     For each verified item:
│       - [x] item text → - [x] item text (evidence: <agent> <outcome> — <1-line snippet>)
│     For each failed item:
│       - [ ] item text → - [ ] item text (BLOCKED: <reason>)
│     For each N/A item:
│       - leave as-is if already marked, or append (N/A: <reason>) if Inquisitor determined N/A
│     Write rewritten body to temp file: /tmp/pr-<N>-body-updated.md
│
├─ 7. PUSH UPDATED BODY
│     gh pr edit <N> --body-file /tmp/pr-<N>-body-updated.md
│
├─ 8. GATE SIGNAL TO CIPHER
│     PASS   — all unchecked items now ticked; no failures
│     BLOCK  — ≥1 item FAILED or UNROUTABLE; list which items blocked and why
│
└─ END
```

### Parallelism rule

Dispatch all independent specialist calls in one parallel batch (single assistant message, multiple Agent tool calls). Items are independent unless one produces an artifact another depends on (e.g., `pnpm build` must complete before a JSON-LD check on `dist/` can run — serial dependency).

### Dependency ordering (fact — derived from PR #3 test plan structure)

```
Serial chain (when all present):
  pnpm install → pnpm build → [JSON-LD/SEO check on dist/]
  uv sync → uv run pytest → uv run uvicorn + curl smoke

Independent of the above:
  pnpm audit
  pnpm agent-browser *
  Static file existence checks (no build dependency if file pre-exists in repo)
  Version-pin verification (static file read)
```

---

## Section 5 — Edge Cases and Risks

### EC-1: Test plan is empty

Condition: PR body contains no `- [ ]` or `- [x]` lines.

Action: Inquisitor 🔎 (PR Reviewer) skips dispatch. Returns `[PASS]` to Cipher 🔓 (Dev-Team Orchestrator) with note: "Test plan section absent or empty — no items to verify." Appends observation to audit report. Does not block.

Risk: empty test plans should be flagged as a Herald 📯 (Release Manager) quality issue, not an Inquisitor 🔎 (PR Reviewer) BLOCK. Inquisitor notes it; Cipher 🔓 (Dev-Team Orchestrator) decides whether to route back to Herald 📯 (Release Manager) for a test plan addition.

### EC-2: Item is N/A for current PR phase

Pattern observed: PR #3, item 8 — `POST /analyze` endpoint test — marked `~~strikethrough~~ — N/A: phase 07 scope is scaffold only`.

Rule: Inquisitor 🔎 (PR Reviewer) checks each item's text for N/A markers (`~~...~~`, `N/A:` inline annotation, or a parenthetical `(N/A ...)` appended by the PR author). Items with an existing N/A annotation are skipped — do not dispatch, do not overwrite. Inquisitor 🔎 (PR Reviewer) records them in the audit report as "skipped — N/A by PR author."

Inquisitor 🔎 (PR Reviewer) does NOT determine N/A autonomously based on task context. Only the PR author's explicit annotation confers N/A status. If an item is unchecked and has no N/A annotation but appears out of scope for the current phase, Inquisitor 🔎 (PR Reviewer) flags it to Cipher 🔓 (Dev-Team Orchestrator) as UNROUTABLE rather than silently skipping it.

### EC-3: Command does not match any specialist (UNROUTABLE)

Examples: `python .claude/skills/plan-enforce/scripts/test_validate_plan.py` (PR #1 one-off), Lighthouse manual score (PR #4 item 8 — "manual, optional this PR").

Action: Inquisitor 🔎 (PR Reviewer) marks item `(UNROUTABLE: no agent holds the grant for this command)` and returns BLOCK signal citing the unroutable items. Cipher 🔓 (Dev-Team Orchestrator) must either: assign the item to a specialist who gains a new grant (Augur 🔮 (Senior Research Analyst) research → Marshal 🎖️ (HR Director) spec edit → Sentinel 🛡️ (Quality Guardian) gate), or acknowledge it as a manual/optional item and instruct Inquisitor 🔎 (PR Reviewer) to skip.

Exception for "manual, optional" items: if the item text includes the word "manual" or "optional", Inquisitor 🔎 (PR Reviewer) flags it as ADVISORY rather than BLOCK — the PR author explicitly signaled human verification is acceptable.

### EC-4: Specialist command fails (non-zero exit)

Action: Inquisitor 🔎 (PR Reviewer) marks the item `(BLOCKED: <agent> returned exit code <N> — <stderr excerpt ≤ 3 lines>)`. Returns BLOCK signal to Cipher 🔓 (Dev-Team Orchestrator). Cipher 🔓 (Dev-Team Orchestrator) routes the failure to Forge 🔨 (Implementation Agent) for remediation. After Forge 🔨 (Implementation Agent) fixes and Herald 📯 (Release Manager) commits, Cipher 🔓 (Dev-Team Orchestrator) re-dispatches Inquisitor 🔎 (PR Reviewer) for the failed item only (not the full test plan).

### EC-5: PR body was updated between Inquisitor fetch and push

Risk: if Cipher or another process edits the PR body between step 1 (fetch) and step 7 (push), the `gh pr edit --body-file` call overwrites the intermediate edit.

Mitigation: Inquisitor 🔎 (PR Reviewer) reads the body a second time immediately before step 6 (rewrite), merges the tick state with any new content, then pushes. If the second fetch differs from the first in ways beyond checkbox ticks (new content sections added), Inquisitor 🔎 (PR Reviewer) reports the divergence to Cipher 🔓 (Dev-Team Orchestrator) and waits for instruction rather than overwriting blindly.

### EC-6: `pnpm build` produces `dist/` but a subsequent JSON-LD check is part of the same PR

Inquisitor 🔎 (PR Reviewer) must dispatch Atrium 🏛️ (Frontend Architect) for `pnpm build` first (serial), wait for PASS, then execute the JSON-LD/SEO self-check using Read/Grep on `frontend/dist/index.html`. This is a data dependency — enforce serial ordering, not parallel.

### EC-7: Bastion currently has no Bash grant

This is the single highest-risk gap. Until Marshal 🎖️ (HR Director) edits Bastion 🧱 (Backend Architect)'s spec and CLAUDE.md, and Sentinel 🛡️ (Quality Guardian) gates those edits, Bastion 🧱 (Backend Architect) cannot run any `uv *` command. Any PR with uv-based test-plan items (all backend PRs after #4) cannot be fully verified by the automated flow.

Interim mitigation: Inquisitor 🔎 (PR Reviewer) marks uv-family items as UNROUTABLE with note "Bastion 🧱 (Backend Architect) uv grant pending spec edit — manual verification required." Returns BLOCK for those items. Cipher 🔓 (Dev-Team Orchestrator) escalates to Marshal 🎖️ (HR Director) / Sentinel 🛡️ (Quality Guardian) for the spec edit.

### EC-8: Inquisitor's current spec prohibits `gh pr edit`

The current Inquisitor 🔎 (PR Reviewer) spec Hard Rules section explicitly lists `gh pr edit` as prohibited: "Any `gh pr merge`, `gh pr close`, `gh pr edit` — state mutations beyond read and comment." This prohibition must be lifted by Marshal 🎖️ (HR Director) + Sentinel 🛡️ (Quality Guardian) before the new workflow is live.

---

## Section 6 — CLAUDE.md Change Recommendations

### 6a — Dev work gate chain table

Add a new row after "Cross-file PR review":

**Current table:**

```
| Gate | Owner | Trigger | Blocks |
|---|---|---|---|
| Visual/UX | Lumen (Visual Director) | Changes touching visual surfaces | Herald (Release Manager) until Critical/High clear |
| Dep/security | Warden (Dependency Warden) | New dep, lockfile diff | Herald (Release Manager) until PASS/ADVISORY |
| Cross-file PR review | Inquisitor (PR Reviewer) | Pre-Herald PR creation OR user manual request | Herald (Release Manager) until PASS/ADVISORY |
| Release | Herald (Release Manager) | All prior gates passed | User (sole merge authority) |
```

**Add after "Cross-file PR review" row:**

```
| Test-plan verification | Inquisitor (PR Reviewer) | After Herald returns PR URL — Cipher dispatches Inquisitor to tick all test-plan checkboxes | Cipher does not mark PR ready until Inquisitor returns PASS or BLOCK items are resolved |
```

**Trigger description elaboration (prose, to appear below the table or as a note):**

> Inquisitor 🔎 (PR Reviewer) runs test-plan verification immediately after Herald 📯 (Release Manager) opens the PR and returns the URL. Inquisitor 🔎 (PR Reviewer) fetches the PR body, parses unchecked `- [ ]` items, dispatches each to the specialist agent that holds the relevant bash grant, collects evidence, rewrites the PR body with ticked items and evidence annotations, then returns PASS or BLOCK to Cipher 🔓 (Dev-Team Orchestrator).

### 6b — Bash grant registry table

**Current Inquisitor 🔎 (PR Reviewer) row:**

```
| Inquisitor 🔎 (PR Reviewer) | `git diff main...HEAD`, `git diff main...HEAD -- <file>`, `git log main...HEAD --oneline`, `gh pr view <number>`, `gh pr view <number> --json title,body,files,state`, `gh pr review <number> --comment --body "<body>"`, `gh pr comment <number> --body "<body>"` |
```

**Updated Inquisitor 🔎 (PR Reviewer) row (add three commands):**

```
| Inquisitor 🔎 (PR Reviewer) | `git diff main...HEAD`, `git diff main...HEAD -- <file>`, `git log main...HEAD --oneline`, `gh pr view <number>`, `gh pr view <number> --json title,body,files,state`, `gh pr view <number> --json body --jq .body`, `gh pr review <number> --comment --body "<body>"`, `gh pr comment <number> --body "<body>"`, `gh pr edit <number> --body-file <file>`, `gh pr edit <number> --body "<inline string>"` |
```

**New Atrium 🏛️ (Frontend Architect) row (add two commands to existing grant):**

Current: `pnpm install` for production/build-tooling deps

Updated: `pnpm install` for production/build-tooling deps; `pnpm build`; `pnpm dev` (both scoped to `frontend/` working directory; dev server must be stopped after test-plan item completes)

**New Bastion 🧱 (Backend Architect) row (currently no Bash grant — new row):**

```
| Bastion 🧱 (Backend Architect) | `uv sync` (within `backend/`), `uv run pytest <args>` (within `backend/`), `uv run uvicorn <args>`, `uv run python -m backend.scripts.<script>`, `curl -s -X POST -F <args> http://localhost:<port>/analyze` |
```

### 6c — Cipher Hard Rules additions

Add one new rule to the "Cipher 🔓 (Dev-Team Orchestrator) Hard Rules" section:

```
- **Test-plan-verification-gate.** After Herald 📯 (Release Manager) returns a PR URL, Cipher 🔓 (Dev-Team Orchestrator) MUST dispatch Inquisitor 🔎 (PR Reviewer) for test-plan verification before marking the PR ready. Cipher 🔓 (Dev-Team Orchestrator) does not manually tick test-plan checkboxes — Inquisitor 🔎 (PR Reviewer) owns that surface. Exception: empty test plan (Inquisitor 🔎 (PR Reviewer) returns PASS immediately with a note).
```

### 6d — Inquisitor spec (`inquisitor.md`) — Bash Command Allowlist section

Remove from Prohibited list:
> `gh pr merge`, `gh pr close`, `gh pr edit` — state mutations beyond read and comment

Replace with:
> `gh pr merge`, `gh pr close` — lifecycle mutations; Herald and user own those. `gh pr edit` is permitted ONLY for `--body-file` and `--body` flags (test-plan tick updates). All other `gh pr edit` flags (title, labels, milestone, assignees, reviewers) remain prohibited.

Also add to Permitted list:
```
gh pr view <number> --json body --jq .body
gh pr edit <number> --body-file <file>
gh pr edit <number> --body "<inline string>"
```

---

## Summary of Key Findings

Comprehensive analysis of test-plan verification workflow ownership and specialist dispatch protocol. Identifies 6 critical Bash grant gaps (Bastion 🧱 (Backend Architect) `uv *` family, Atrium 🏛️ (Frontend Architect) `pnpm build`/`pnpm dev`, Inquisitor 🔎 (PR Reviewer) `gh pr edit`). Proposes updated Inquisitor 🔎 (PR Reviewer) spec, CLAUDE.md table additions, and detailed dispatch protocol with serialization rules, edge cases, and interim mitigations.

---

## Key Findings Summary

| # | Finding | Type | Relevance |
|---|---------|------|-----------|
| 1 | Bastion (Backend Architect) has zero Bash grant; `uv sync`, `uv run pytest`, `uv run uvicorn`, `curl` smoke test are all unowned | Fact | Critical — blocks all backend test-plan items |
| 2 | Atrium (Frontend Architect) has `pnpm install` grant but not `pnpm build` or `pnpm dev`; both appear in PRs #3 and #4 | Fact | High — blocks frontend build/smoke test items |
| 3 | Inquisitor's current spec explicitly prohibits `gh pr edit`; the new workflow requires it | Fact | Critical — spec must be edited before workflow is live |
| 4 | Static file checks (JSON, SEO meta, version-pin scan) require no new grants — Inquisitor already holds Read/Grep | Fact | Positive — reduces grant scope creep |
| 5 | Serial ordering is required for build-then-check chains (pnpm build → JSON-LD check; uv sync → pytest → uvicorn+curl) | Fact | Medium — dispatch protocol must enforce this |
| 6 | PR #3 established the N/A annotation pattern (`~~strikethrough~~ — N/A: ...`) used to signal out-of-scope items | Fact | Medium — Inquisitor must parse and respect this pattern |
| 7 | PR #1 contained a one-off Python script item (`test_validate_plan.py`) with no recurring pattern; no grant assignment recommended | Fact | Low — anomaly, not a recurring family |

---

## Gaps

- **No evidence of PR #3 or #4 test plans being verified by an automated agent** (fact: all tick marks present in merged PR bodies, but Cipher's smoke test notes confirm manual verification). This is the pain point the new workflow addresses.
- **Bastion spec edit timeline unknown** — Bastion gaining `uv *` requires Marshal (HR Director) + Sentinel (Quality Guardian) gate. Until that spec edit ships, all backend test-plan items remain UNROUTABLE.
- **`pnpm dev` server lifecycle** — Atrium would start the server for the smoke check but must stop it afterward. The spec should explicitly state this. Current `pnpm install`-only grant in Atrium's spec does not address server lifecycle. Marshal should add an explicit "must `kill` or `pkill` the dev server after the test step" clause to Atrium's grant.
- **`curl` port collision** — if a previous uv run left a uvicorn process running (e.g. from a prior failed test step), Bastion's `uv run uvicorn` on the same port will fail. Bastion's proposed grant should include `pkill -f uvicorn` as a pre-step cleanup command.

---

## Recommendations

1. **Immediate (blocks workflow launch):** Route to Marshal (HR Director) to edit Inquisitor's spec — remove `gh pr edit` prohibition, add permitted body-edit variants, add test-plan verification workflow section. Gate via Sentinel (Quality Guardian).

2. **Immediate:** Route to Marshal (HR Director) to add Bastion's Bash grant (`uv *` family + `curl` smoke) to Bastion's spec and CLAUDE.md. Gate via Sentinel (Quality Guardian). Without this, every backend PR test plan will BLOCK on Inquisitor returning UNROUTABLE for uv items.

3. **Immediate:** Route to Marshal (HR Director) to extend Atrium's Bash grant to include `pnpm build` and `pnpm dev` (with server-kill clause). Update CLAUDE.md and Atrium's spec.

4. **Immediate:** Add the Test-plan verification row to CLAUDE.md's Dev work gate chain table and the new Cipher Hard Rule (Section 6a, 6c above).

5. **Deferred (after launch):** Define a max-wait timeout for long-running specialist commands (e.g. `pnpm build` or `uv run pytest` on a slow machine). Recommend 120s per item; Inquisitor marks item BLOCKED with timeout note if exceeded.

6. **Deferred:** Add an explicit "empty test plan is a Herald quality warning" rule to Herald's spec — Herald should not author a PR body with an empty or placeholder test plan section.
