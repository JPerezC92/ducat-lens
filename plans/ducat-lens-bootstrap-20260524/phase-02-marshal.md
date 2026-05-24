# Phase 02 — Adapt CLAUDE.md + agent specs to ducat-lens dev

## Owner

Marshal 🎖️ (HR Director)

## Pre

- Roster already trimmed: only dev agents present (`atrium`, `bastion`, `crucible`, `forge`, `herald`, `lumen`, `marshal`, `sentinel`, `warden`, `augur`). No incident agents (Atlas, Ember, Ranger, Lex, Gate, Quill, Ledger, Scribe, Vault) exist.
- User confirmed: keep Cipher 🔓 as dev-team orchestrator persona.

## Reads

- `D:/projects/ducat-lens/CLAUDE.md` — current Belcorp incident spec (~30K)
- `D:/projects/ducat-lens/.claude/agents/*.md` — 10 agent specs
- `D:/projects/ducat-lens/agents/cipher/profile.md` — Cipher persona (if exists)
- `D:/projects/ducat-lens/agents/<each>/profile.md` — persona files

## Writes

- `D:/projects/ducat-lens/CLAUDE.md` — rewritten end-to-end
- `D:/projects/ducat-lens/.claude/agents/<name>.md` — for each agent that references Belcorp/SDP/Activos/tickets, surgical edits removing those references
- `D:/projects/ducat-lens/agents/cipher/profile.md` — confirm exists; create if missing

## Steps

1. Glob `.claude/agents/*.md` and `agents/*/profile.md`; for each, Grep for terms: `Belcorp`, `SDP`, `Activo`, `Cipher 🔓 (L2 Lead)`, `ticket`, `Quill`, `Ledger`, `Atlas`, `Ember`, `Ranger`, `Lex`, `Gate`, `Vault`, `Scribe`, `bitacora`, `runbook`, `phase-NN`, `incident`, `consulta-produccion`, `mongodb-ffvv`, `sdp-`, `cf-kba`. Build deletion/edit list per file.
2. Rewrite `CLAUDE.md` from scratch using this skeleton (≤ 250 lines):
   - **Identity & Role** — Cipher 🔓 is dev-team orchestrator for ducat-lens (React + FastAPI web app analyzing Warframe Ducat Kiosk screenshots)
   - **Cipher Mission** — single team (dev). Route tasks to Atrium 🏛️ / Bastion 🧱 / Crucible 🔥 / Forge 🔨 / Herald 📯 / Lumen ✨ / Sentinel 🛡️ / Warden 🔒. Augur 🔮 + Marshal 🎖️ cross-cut.
   - **Evidence discipline** — keep verbatim from source (universally applicable)
   - **Roster** — table of 10 dev agents only; drop incident table
   - **Workspace map** — `frontend/`, `backend/`, `data/`, `plans/`, `.claude/`, `agents/`. Drop `tickets/`, `confluence/`, `problems/`, `sessions/`, `mcp-servers/`, `BITACORA*.xlsx`.
   - **Skill routing** — keep `git-*` (Herald), `plan-enforce`, `ui-ux-pro-max`, `impeccable`, `frontend-design`, `webapp-testing`, `verify`, `run`, `caveman:*`. Drop all `sdp-*`, `sb-*`, `gana-*`, `ffvv-*`, `prol-*`, `cd-*`, `unete-*`, `cf-kba-*`, `bitacora-n2`, `vault-pattern-prompt`.
   - **Plan format** — keep subfolder default + lifecycle rules verbatim
   - **Operational gates** — keep Roster edit gate (Marshal-routed, Sentinel audits dev specs), Auto-run code verifiers (Atrium/Crucible), Dev work gate chain (Lumen/Warden/Herald), Pre-coding sync gate, Bash grant registry. Drop incident-specific gates.
   - **Coding discipline** — keep verbatim
   - **Cipher Hard Rules** — keep universally applicable (Grounding-First, Stop-and-clarify, User-Authority-Only, Evidence-discipline). Drop ticket-specific rules (Attachment-first, Phase ownership for runbook/phase-NN, G3.5 explicit gate, No-inline-prose, No-direct-ticket-edits, Pattern-check at close-out, Per-phase Ledger sync, Auth refresh, Kill Switches table).
   - **Project context** — short section: stack (React+Vite+TS frontend / FastAPI Python backend), goal (Warframe ducat analyzer), no auth/DB/users, public web tool, test fixture `image.png` at root.
3. For each agent spec in `.claude/agents/*.md`:
   - Remove every Belcorp/SDP/Activo/ticket reference identified in step 1
   - Rewrite domain examples in the spec to use ducat-lens equivalents (e.g. Atrium examples → React+Vite+TS components; Bastion examples → FastAPI Python routers)
   - Preserve architecture rules (clean-arch layering, dep boundaries, audit checklists) verbatim — those are language/stack rules, not project rules
   - Update "Activo / Specialty" labels in any roster references to match dev-team-only roster
4. Verify `agents/cipher/profile.md` exists; if missing, write a short persona file: "Cipher 🔓 — L2 dev-team orchestrator for ducat-lens. Decisive, evidence-based, dry-humored. Routes tasks to specialist agents."
5. Sentinel 🛡️ self-audit per Roster edit gate: after Marshal finishes, dispatch Sentinel 🛡️ to audit edited dev agent specs.

## Output

- `CLAUDE.md` ≤ 250 lines, zero Belcorp/SDP/ticket references
- `.claude/agents/*.md` — each edited file passes `grep -E "Belcorp|SDP|Activo|ticket|Quill|Ledger|Atlas|Ember|Ranger|Lex|Gate|Vault|Scribe|bitacora|sdp-|cf-kba" returns zero results (excluding any genuine English use of "ticket" as branch/PR description noun if applicable)
- `agents/cipher/profile.md` exists
- Sentinel audit PASS

## Gate

- Cipher 🔓 reads new `CLAUDE.md` end-to-end and confirms it reflects ducat-lens dev orchestrator role
- All grep checks above return zero
- Sentinel 🛡️ returns PASS on edited agent specs

## Abort conditions

- An agent spec is so Belcorp-coupled (>50% of file) that surgical edit is impossible → escalate to Cipher 🔓; consider full rewrite of that spec from clean dev template
- Sentinel 🛡️ FAIL with >3 critical violations → halt, fix violations before continuing

## MCP whitelist/blacklist

- Allowed: Read, Glob, Grep, Edit, Write
- Forbidden: Bash (no shell needed for doc edits)
