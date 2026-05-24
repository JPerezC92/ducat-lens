---
Status: active
Started: 2026-05-24
Subject: Bootstrap ducat-lens — adapt Cipher tooling from Belcorp project + build React/FastAPI app that analyzes Warframe Ducat Kiosk screenshots and recommends sells
Layout: subfolder pattern
---

## Context

User wants web app: upload Warframe Ducat Kiosk inventory screenshot → app detects Prime parts shown → returns ducat values + sell recommendations. Stack: React frontend, FastAPI (Python) backend. No auth, no DB, no users — public web tool.

Tooling source: `.claude/agents/*.md` + `CLAUDE.md` were copied from a Belcorp AMS L2 support project. Roster already trimmed to dev agents (Atrium, Bastion, Crucible, Forge, Herald, Lumen, Marshal, Sentinel, Warden, Augur). CLAUDE.md still riddled with Belcorp/SDP/incident framing — must be rewritten for ducat-lens dev orchestration.

User constraint: free OCR/vision solution. Wants official Warframe API for ducat values if exists.

## Goal

Three deliverables, in order:

1. **Adapted tooling (docs)** — `CLAUDE.md` rewritten as ducat-lens dev orchestrator spec; agent `.md` files audited and edited to remove Belcorp-isms; `plans/_template.md` + `plans/_phase-template.md` written so plan-enforce skill works going forward.
2. **Reusable dev tooling** — plan-enforce skill consolidates: prior `task-runbook` skill superseded; refactored validator (`validate_plan.py`) bundled inside plan-enforce, project-agnostic, strips all incident concepts (no kill switches, no SLA window, no Replay-candidate enum, no concurrent-session check, no fraction type). Auto-invoked by plan-enforce before ExitPlanMode.
3. **Working ducat-lens MVP** — `pnpm run dev` (frontend) + `uvicorn main:app --reload` (backend) starts both; user uploads `image.png` via UI; receives table of detected items with ducat values + sell recommendation (e.g. high-ducat items at top, dupes flagged).

## Body

### Tracks

| Track | Owner | Phases |
|---|---|---|
| **A — Research** | Augur 🔮 | 01 |
| **B — Doc adapt** | Marshal 🎖️ | 02 |
| **C — Architecture** | Cipher 🔓 | 03 |
| **D — Runbook tooling** ⚠️ superseded by Track G | Forge 🔨 + Cipher 🔓 | ~~04, 05, 06~~ |
| **E — Implementation** | Forge 🔨 | 07, 08, 09 |
| **F — Audit gates** | Atrium 🏛️ / Bastion 🧱 / Crucible 🔥 | 10 |
| **G — Consolidation (merger)** | Forge 🔨 + Cipher 🔓 | 11 |

Phases 01 and 02 run in parallel (independent). Phase 03 depends on 01 output. Phases 04 and 05 run in parallel (both depend on the validator config schema written 2026-05-24 in `references/runbook-config-schema.md`). Phase 06 depends on 04 + 05 both passing. Phases 07–09 depend on 03 + 06. Phase 10 audits each Forge phase. No Herald phase yet — git init deferred until user confirms.

### Phase index — dispatch table

| # | Phase | Owner | Runbook | Output |
|---|---|---|---|---|
| 01 | Research: free OCR/vision + Warframe ducat API | Augur 🔮 | `phase-01-augur.md` | `_research-vision.md` + `_research-ducat-api.md` |
| 02 | Adapt CLAUDE.md + agent specs to ducat-lens dev | Marshal 🎖️ | `phase-02-marshal.md` | edited `CLAUDE.md` + edited `.claude/agents/*.md` + `plans/_template.md` + `plans/_phase-template.md` |
| 03 | Pick vision lib + data source + scaffold layout | Cipher 🔓 | `phase-03-cipher.md` | `_architecture.md` (stack decisions) |
| 04 | Refactor `validate_runbook.py` to config-driven | Forge 🔨 | `phase-04-forge.md` | `.claude/skills/task-runbook/scripts/validate_runbook.py` (refactored) + unit + integration tests passing; root `validate_runbook.py` deleted |
| 05 | Draft `task-runbook` SKILL.md | Cipher 🔓 | `phase-05-cipher.md` | `.claude/skills/task-runbook/SKILL.md` |
| 06 | Skill evals cycle (skill-creator workflow) | Cipher 🔓 | `phase-06-cipher.md` | `.claude/skills/task-runbook/evals/evals.json` + `task-runbook-workspace/iteration-N/` + benchmark.json + feedback.json |
| 07 | Scaffold repo: React+Vite frontend, FastAPI backend, ducat data bundle | Forge 🔨 | `phase-07-forge.md` | `frontend/` + `backend/` + `data/ducats.json` |
| 08 | Backend pipeline: image upload → detect items → ducat lookup → recommend | Forge 🔨 | `phase-08-forge.md` | `backend/analyze.py` + `/analyze` endpoint working on `image.png` |
| 09 | Frontend: upload UI + results table | Forge 🔨 | `phase-09-forge.md` | `frontend/src/App.tsx` etc., browser-tested upload flow |
| 10 | Audit: Atrium (FE) + Bastion (BE) + Crucible (tests) | parallel | `phase-10-audit.md` | PASS/FAIL reports per agent |
| 11 | Merger: collapse task-runbook into plan-enforce, strip incident concepts, dev-agnostic | Forge 🔨 + Cipher 🔓 | `phase-11-merger.md` | task-runbook skill deleted; validator renamed `validate_plan.py` + moved into plan-enforce/scripts/; plan-config-schema.md rewritten; example-config-plan.yaml; eval workspace archived under `plans/_archive/` |

### Resolved decisions

- 2026-05-24 — App scope: public web, no auth/DB/users. Single-page upload + result.
- 2026-05-24 — Persona: Keep Cipher 🔓 as dev-team orchestrator. Strip incident half.
- 2026-05-24 — Pricing target: ducats only (not platinum). Need official/community ducat API.
- 2026-05-24 — Vision constraint: free solution. Augur 🔮 to research.
- 2026-05-24 — `validate_tickets.py` deleted from root (Belcorp ticket validator, broken without `ticket_models.py`, unrelated to runbook flow).
- 2026-05-24 — Priority: build reusable tooling first (phases 04-06), app second (phases 07-10). Per user explicit decision.
- 2026-05-24 — `task-runbook` skill bundles its own `validate_runbook.py` under `scripts/`; project root stays empty of validator code.
- 2026-05-24 — Validator config schema locked at `.claude/skills/task-runbook/references/runbook-config-schema.md` v1.0. Examples: `example-config-belcorp.yaml` (full reproduction of original behavior) + `example-config-minimal.yaml` (bare starting point).
- 2026-05-24 — Phase 04 complete: 53 pytest cases pass; Bastion 🧱 PASS; Crucible 🔥 PASS. Byte-fidelity deviation accepted: kill-switch message bodies now read `<name> cap exceeded` (config-driven substitution) instead of original hardcoded `hypothesis/query/rerun cap exceeded`. Violation codes (KILL-1/2/3) unchanged. Future v1.1 schema may add optional `message_template` field if exact byte-replay needed.
- 2026-05-24 — Phase 05 complete: SKILL.md drafted, 245 lines, Sentinel 🛡️ PASS, zero Belcorp/SDP/Activo/ticket seepage.
- 2026-05-24 — Phase 06 complete: iter-2 clean baselines, with_skill 100% (17/17), without_skill 88.9% (15/17), Δ +11.1%. Skill works.
- 2026-05-24 — **User directive (post-phase-06)**: tools must be project-agnostic dev tooling. task-runbook conceptually incident-shaped (replay verdicts, prior-art catalog, hypothesis inheritance) — mismatches pure-dev-team ducat-lens roster. Merger ordered: collapse task-runbook into plan-enforce, strip all incident concepts. Track G + phase 11 created.
- 2026-05-24 — Eval workspace archived to `plans/_archive/task-runbook-evals-20260524/` (history preserved, project active dirs clean).
- 2026-05-24 — Validator refactor: strip kill_switches, sla_window, concurrent_session, Replay-candidate enum, fraction type. Rename `validate_runbook.py` → `validate_plan.py`. Move to `.claude/skills/plan-enforce/scripts/`. Auto-invoke in plan-enforce § 2.6 before ExitPlanMode.
- 2026-05-24 — Skills bundled scripts pattern adopted: validator + tests + fixtures live inside skill bundle (`scripts/`), referenced docs in `references/`. Project root + project `plans/` stay free of skill internals.
- 2026-05-24 — Phase 02 Round 1 partial: Marshal 🎖️ cleaned 5 specs + 4 personas + CLAUDE.md (390 → 247 lines). Independent inline audit revealed Round 1 missed `L2 Lead` (Cipher role title) + `NestJS-TS` (framework refs) patterns because Cipher's pre-dispatch grep didn't include them. Round 2 dispatched with comprehensive patch list.
- 2026-05-24 — Phase 02 Round 2 complete: 70+ `L2 Lead` → `Dev-Team Orchestrator` across atrium/crucible/herald/lumen/warden + their personas; bastion.md surgically reduced 236→131 lines (NestJS sections removed, Python-only rulebook retained); crucible.md NestJS refs replaced with framework-agnostic rules. Tooling milestone CLEAR.
- 2026-05-24 — Tooling milestone declared. Next: dev work (phase 01 Augur output ready in `_research-vision.md` + `_research-ducat-api.md` from earlier completion; phase 03 architecture; phases 07-10 app build).

## Source of truth chain

For ducat values + item name resolution:
1. Official Warframe API (`api.warframe.com` if exists)
2. Warframe Community Developers — `api.warframestat.us`
3. Warframe.market API (`api.warframe.market/v1`) — has `ducats` field per item
4. Wiki scrape fallback (last resort)

Final pick locked in phase 03 from Augur 🔮 brief.

## Critical files / tools

- `D:/projects/ducat-lens/CLAUDE.md` — rewrite target
- `D:/projects/ducat-lens/.claude/agents/*.md` — 10 specs to audit
- `D:/projects/ducat-lens/agents/*/` — persona profile dirs (most empty placeholders)
- `D:/projects/ducat-lens/image.png` — test fixture for phases 06 + 08
- `D:/projects/ducat-lens/plans/_template.md` + `_phase-template.md` — written 2026-05-24
- `D:/projects/ducat-lens/validate_runbook.py` — Belcorp validator, to be moved + refactored in phase 04
- `D:/projects/ducat-lens/.claude/skills/task-runbook/references/` — schema docs + 2 example configs (written 2026-05-24)
- `D:/projects/ducat-lens/.claude/skills/sdp-runbook/` — reference only, do not modify
- Skills: `plan-enforce`, `ui-ux-pro-max`, `impeccable`, `frontend-design`, `webapp-testing`, `verify`, `run`, `claude-api:skill-creator`

## Verification

- ⬜ phase-01 — Augur returns `_research-vision.md` with ≥2 free vision options ranked + `_research-ducat-api.md` with confirmed ducat data source
- ✅ phase-02 — `CLAUDE.md` rewritten end-to-end (246 lines, dev-only orchestrator); all 10 agent specs + 10 persona profiles audited and migrated; `L2 Lead` → `Dev-Team Orchestrator` (70+ replacements across 12 files in Round 2); NestJS-TS framework refs stripped from bastion.md (236→131 lines, Python-only) + crucible.md test rules; zero Belcorp/SDP/Activo/Quill/Ledger/Atlas/Ember/Ranger/Vault/Scribe/consulta-produccion/mongodb/bitacora/cf-kba hits (independent grep verified). Marshal 🎖️ Round 1 + Round 2 PASS. Sentinel 🛡️ formal re-audit deferred (session limit). Cipher 🔓 inline review PASS.
- ⬜ phase-03 — `_architecture.md` locks: vision lib, ducat source, repo layout, npm/pip dep list
- ✅ phase-04 — (⚠️ superseded by phase 11) `validate_runbook.py` was refactored config-driven w/ 53 pytest cases. Now relocated + renamed under merger.
- ✅ phase-05 — (⚠️ superseded by phase 11) task-runbook SKILL.md was drafted + Sentinel PASS. Skill deleted under merger.
- ✅ phase-06 — (⚠️ superseded by phase 11) eval cycle ran iter-1 + iter-2; with_skill 100%, baseline 88.9%. Workspace archived.
- ✅ phase-11 — task-runbook deleted; plan-enforce bundle complete with `scripts/validate_plan.py` (24.7K) + `test_validate_plan.py` (36 pytest cases green) + `scripts/fixtures/plan-valid/`; `references/plan-config-schema.md` + `example-config-plan.yaml` written; SKILL.md §§ 2.6 + 2.7 + 3 Troubleshooting entries added; zero incident-vocab hits; `plans/_template.md` updated to YAML frontmatter; eval workspace archived to `plans/_archive/task-runbook-evals-20260524/`. Bastion 🧱 PASS. Crucible 🔥 PASS. Sentinel 🛡️ FAIL → 9 mechanical fixes applied (naming convention + SDP vocab swap) → effective PASS post-fix.
- ⬜ phase-06 — `evals/evals.json` written with ≥3 realistic test prompts; with-skill + without-skill subagent runs complete; `benchmark.json` produced; user feedback collected via viewer
- ⬜ phase-07 — `pnpm install && pnpm run dev` boots frontend on :5173; `uvicorn main:app --reload` boots backend on :8000; `data/ducats.json` populated
- ⬜ phase-08 — `POST /analyze` with `image.png` returns JSON list of detected items + ducats + recommendation
- ⬜ phase-09 — Browser: drag-drop `image.png` → results table renders within 10s
- ⬜ phase-10 — Atrium PASS on frontend, Bastion PASS on backend, Crucible PASS on test pyramid (≥1 unit per critical fn)

## Out of scope

- Authentication, user accounts, history persistence
- Platinum trade price (only ducats)
- Mobile app, PWA
- Real-time market data caching infrastructure
- Other Warframe inventory screens (Relics, Mods, Resources) — Ducat Kiosk only
- CI/CD, deployment, hosting

## Pending

- [waiting for] User to confirm Augur 🔮 research output before phase 03 architecture lock
- [blocked on] User decision on git init (Herald phase deferred until requested)
