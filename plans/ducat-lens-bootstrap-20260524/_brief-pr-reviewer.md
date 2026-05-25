# Augur Brief — PR Reviewer Hire Requirements

> Prepared for Cipher 🔓 (Dev-Team Orchestrator) → Marshal 🎖️ (HR Director)
> Date: 2026-05-24
> Requested by: Cipher 🔓 (Dev-Team Orchestrator)

---

## Executive Recommendation

**Hire a new dedicated agent. Do not extend Sentinel 🛡️ (Quality Guardian).**

Sentinel's scope is markdown-convention compliance across doc surfaces — a fundamentally different contract from cross-file diff analysis on code PRs. Merging both into one agent creates a split-focus spec that neither task domain benefits from: Sentinel's rulebook is naming-convention and heading-order driven; the PR reviewer's rulebook is code-shape, scope-creep, and attribution-hygiene driven. The operational trigger differs (Marshal invokes Sentinel after spec edits; Cipher invokes the PR reviewer before Herald creates a PR), the tooling differs (Sentinel needs Edit to auto-fix markdown; the PR reviewer is read-only on all src), and the model tier required differs (a PR reviewer benefits from Sonnet's reasoning depth; Sentinel is correctly Haiku). Combining them would bloat the spec past one coherent identity and force awkward "only-when-not-markdown" conditionals throughout the workflow. A clean new hire with a focused scope is the correct call.

---

## 1. Naming Candidates

**Existing icon inventory (must not duplicate):**
`🔓 🎖️ 🔮 🏛️ 🧱 🔥 🔨 📯 ✨ 🛡️ 🔒`

Source: `CLAUDE.md` lines 80–90.

Candidates ranked by naming-style fit (short, evocative, profession-coded, no existing icon clash):

| Rank | Name | Icon | Rationale |
|------|------|------|-----------|
| 1 | **Arbiter** | ⚖️ | Judges the diff against the rules. Latin legal tradition — fits the Cipher/Sentinel/Warden register. Clear profession signal. |
| 2 | **Scrutator** | 🔬 | From Latin "scrutari" (to examine). Scientific precision tone. Less common but highly evocative. |
| 3 | **Tribune** | 🎙️ | Roman tribune had oversight and veto power — exact functional analog. Slightly more political than technical, but fits the project's Roman-naming pattern. |
| 4 | **Inquisitor** | 🔎 | Strong profession-coding for a reviewer. Slightly adversarial tone, which is accurate for a hard-gate agent. |
| 5 | **Praetor** | ⚖️ | Roman magistrate who enforced standards — direct analogy. Note: ⚖️ would be shared with Arbiter if both are candidates; Cipher must pick only one. |

**Augur recommendation:** Arbiter ⚖️ — fits the magistrate tradition of the roster (Sentinel, Warden, Bastion, Herald all carry civic/institutional weight), the ⚖️ icon has immediate professional readability, and "arbiter" is unambiguous in English as "one who judges."

Cipher 🔓 (Dev-Team Orchestrator) makes the final name selection.

---

## 2. Scope Boundaries vs Sentinel

### What Sentinel currently does
**Fact** (source: `.claude/agents/sentinel.md` lines 52–58, Hard-out list line 54):
- Audits markdown files that touch dev-roster naming conventions
- Explicit Hard-out: "Source code (`frontend/src/`, `backend/`, `e2e/`, `.tsx`/`.ts`/`.jsx`/`.js`, `.py`)"
- Explicit Hard-out: "Commit messages, PR descriptions (live outside repo files)"
- Does NOT read git diffs. Does NOT invoke `gh` commands. Does NOT audit PRs.

### What the new PR reviewer does
**Fact** (source: Cipher's intent statement in this research request):
- Reads `git diff main...HEAD` — a Bash operation Sentinel has no grant for beyond its doc-file reads
- Reviews code + docs together across the PR diff boundary
- Posts `gh pr review` / `gh pr comment` on open PRs — GitHub API operations entirely outside Sentinel's scope
- Catches cross-file concerns (naming consistency across TS + Python files, AI attribution in tracked files, scope creep across modules, public API consistency)
- Read-only on all source files — never edits

### Overlap assessment
**Fact:** Sentinel's Hard-out list explicitly excludes source code and PR descriptions. There is zero operational overlap between Sentinel's current scope and the PR reviewer's intended scope.

**Hypothesis** (partial evidence): If the PR reviewer writes `knowledge/audits/pr-<N>-<date>.md`, Sentinel's scope-detection rule may pick up these files on a subsequent sweep (Sentinel audits `knowledge/audits/**/*.md` — `.claude/agents/sentinel.md` line 38). This is manageable: the PR reviewer writes the report; Sentinel audits the report for naming-convention compliance only. The scopes are additive, not overlapping.

**Recommendation:** New dedicated agent. Extending Sentinel would require adding Bash grants (git, gh), a new rulebook section for code-pattern checks, a new trigger model, and a new output format — all of which contradict Sentinel's Haiku model tier and auto-fix/judgment-call binary pattern.

---

## 3. Tool Grants

| Tool | Required | Justification |
|------|----------|---------------|
| Read | Yes | Read individual files surfaced by the diff |
| Glob | Yes | Enumerate changed files by pattern (e.g., find all `.ts` and `.py` touched) |
| Grep | Yes | Cross-file pattern search (find leaked strings, naming inconsistencies) |
| Bash | Yes — scoped | `git diff`, `gh pr view`, `gh pr review`, `gh pr comment` (see allowlist below) |
| Write | Yes — scoped | Write audit report to `knowledge/audits/pr-<N>-<date>.md` only |
| Edit | No | Never edits source. Write is sufficient for report-only output. |
| WebFetch / WebSearch | No | No external research role |

**Bash command allowlist (precise):**

```
git diff main...HEAD
git diff main...HEAD -- <file>
git log main...HEAD --oneline
gh pr view <number>
gh pr view <number> --json title,body,files,state
gh pr review <number> --comment --body "<body>"
gh pr comment <number> --body "<body>"
```

**Prohibited Bash commands for this agent:**
- Any `git add`, `git commit`, `git push`, `git checkout` (Herald owns all staging/committing)
- Any `pnpm` commands (Warden/Atrium/Crucible own those families)
- Any `gh pr merge`, `gh pr close`, `gh pr edit` (state mutations beyond comments)
- Any `git diff` against arbitrary SHA ranges not bounded by `main...HEAD`

**Justification for Bash grant** (required per CLAUDE.md Bash grant registry rule, source: `CLAUDE.md` line 226):
Single operation family: git-read + gh-comment. No install, no staging, no branch creation. Read-only on the repo tree; comment-only on GitHub. The diff-read and PR-comment family is non-overlapping with Herald's git/gh grant (Herald writes commits and creates PRs; this agent reads diffs and posts review comments on existing PRs — different verbs, different GitHub resource states).

---

## 4. Gate Position

Current Dev work gate chain (source: `CLAUDE.md` lines 197–203):

```
[Auto-run single-file verifiers]
  Atrium (frontend code edits)
  Bastion (backend code edits)
  Crucible (test file edits)
  Sentinel (doc/spec markdown edits)
        |
        v
[Dev work gate chain]
  Lumen (visual surfaces) ──────────────┐
  Warden (dep/lockfile changes) ────────┤──> Herald (Release Manager)
                                        │         |
                                        └─────────┘
                                                  v
                                             User (sole merge authority)
```

**Proposed insertion point for new PR reviewer:**

```
[Auto-run single-file verifiers]
  Atrium / Bastion / Crucible / Sentinel (unchanged — file-level, auto-triggered)
        |
        v
[Dev work gate chain]
  Lumen (visual surfaces) ──────────────┐
  Warden (dep/lockfile changes) ────────┤
  NEW: PR Reviewer (cross-file diff) ───┤──> Herald (Release Manager)
                                        │         |
                                        └─────────┘
                                                  v
                                             User (sole merge authority)
```

**Rationale for parallel-with-Lumen/Warden placement:**
- Fact: the single-file verifiers (Atrium, Bastion, Crucible, Sentinel) gate at the file-edit moment, before any PR exists. The PR reviewer operates at the PR boundary — after all file edits are staged, before Herald creates the PR. This is the same tier as Lumen and Warden.
- The PR reviewer does not depend on Lumen's or Warden's output. All three can run in parallel per Cipher's single-call rule (source: `CLAUDE.md` line 92).
- Herald is gated by all three: existing Lumen Critical/High threshold, existing Warden PASS/ADVISORY threshold, and new PR reviewer PASS/ADVISORY threshold (see gate signal protocol below).

**Gate signal protocol for PR reviewer:**

| Signal | Meaning | Herald behavior |
|--------|---------|-----------------|
| [PASS] | No critical findings | Herald may proceed to `gh pr create` |
| [ADVISORY] | Non-blocking findings present | Herald may proceed; Cipher acknowledges findings |
| [BLOCK] | Critical violation (e.g., AI attribution in tracked file, leaked secret pattern, major scope creep) | Herald pauses; Cipher routes fix to Forge 🔨 (Implementation Agent) |

---

## 5. Trigger Rules

**Auto-trigger (mandatory):**
- Before every `gh pr create` invocation by Herald 📯 (Release Manager). Cipher 🔓 (Dev-Team Orchestrator) dispatches the PR reviewer in parallel with Lumen ✨ (Visual Director) and Warden 🔒 (Dependency Warden) as part of the standard gate chain. Herald does not run `gh pr create` until all three return [PASS] or [ADVISORY] (with Cipher acknowledgment).

**Manual trigger (on demand):**
- When user explicitly requests a review of an existing open PR (by number or URL).
- When Cipher 🔓 (Dev-Team Orchestrator) requests a mid-development cross-file consistency check, even before a PR exists (reviewer reads `git diff main...HEAD` directly in this case and produces a report without posting to GitHub).

**Non-trigger (explicit exclusions):**
- Single-file edits that do not accumulate into a PR yet — those route to Atrium/Bastion/Crucible/Sentinel per the auto-run code verifier rule.
- Merges of main into feature branches — this is Herald's sync operation, not a review event.

---

## 6. Output Report Template

The PR reviewer produces two artifact types depending on context:

### Type A — Inline GitHub Review (open PR exists)
Posted via `gh pr review <number> --comment --body "..."` or `gh pr comment <number> --body "..."`.
Body follows this structure:

```
## PR Review — [scope summary in one line]

### Primary Goal Check
- Stated goal (from PR title/description): [X]
- Diff achieves the stated goal: Yes / Partial / No
- Scope creep detected: Yes (details below) / No

### Findings

| # | Severity | File(s) | Finding | Recommended Action |
|---|----------|---------|---------|-------------------|
| 1 | BLOCK    | path/to/file.ts | AI attribution string found: "Generated with Claude" | Remove before merge |
| 2 | ADVISORY | multiple | Naming inconsistency: `analyzePart` in TS vs `analyze_part` in Python — cross-language OK, but public API endpoint name differs from TS caller expectation | Align endpoint name |
| 3 | INFO     | backend/main.py | Dead import `os` — unused after refactor | Remove in follow-up |

Severity: BLOCK / ADVISORY / INFO

### Gate Signal
[PASS / ADVISORY / BLOCK] — one-sentence rationale.
```

### Type B — File Report (pre-PR or manual review)
Written to `knowledge/audits/pr-<N>-<date>.md` (or `pr-diff-<branch>-<date>.md` when no PR number exists yet).

```markdown
# PR Review — <PR number or branch> (<YYYY-MM-DD>)

## Scope
Branch: <branch name>
Base: main
Diff command: git diff main...HEAD
Files changed: [count] — [list or summary]

## Primary Goal Check
- Stated goal: [derived from branch name, last commit message, or plan file if available]
- Diff achieves stated goal: Yes / Partial / No

## Findings

| # | Severity | File(s) | Finding | Fix Routing |
|---|----------|---------|---------|-------------|

Severity: BLOCK / ADVISORY / INFO

## Cross-cutting Checks
- AI attribution scan: [PASS / BLOCK with locations]
- Naming consistency (cross-file): [PASS / findings]
- Scope creep: [PASS / findings — files changed outside stated goal]
- Dead code introduced: [PASS / findings]
- Public API consistency (if applicable): [PASS / findings]
- Dep hygiene (package.json changes without Warden gate): [PASS / BLOCK]

## Gate Signal
[PASS / ADVISORY / BLOCK] — rationale in one sentence.

## Fix Routing Summary
Which findings route to which agent, for Cipher 🔓 (Dev-Team Orchestrator) to act on.
```

---

## 7. Scope Statement (Cipher/Atrium style)

**What the PR reviewer does:**
- Reads `git diff main...HEAD` to scope review to changed surfaces only
- Checks cross-cutting concerns that single-file verifiers cannot see: naming consistency across file boundaries, AI attribution in any tracked file (Herald's Hard Rule, source: `herald.md` line 109), scope creep (files changed outside the stated PR goal), dead code introduced or left from prior commits, public API consistency between frontend callers and backend endpoints, dep hygiene (package.json edits that bypass the Warden gate)
- Posts a structured review comment on open PRs via `gh pr review` / `gh pr comment`
- Writes a structured audit report to `knowledge/audits/pr-<N>-<date>.md`
- Issues a gate signal ([PASS] / [ADVISORY] / [BLOCK]) to Cipher 🔓 (Dev-Team Orchestrator)

**What the PR reviewer does NOT do:**
- Never edits source code, test files, or spec files — read-only on all `src/`, `backend/`, `frontend/`, `.claude/`
- Never creates, merges, or closes PRs — Herald 📯 (Release Manager) owns all PR lifecycle actions
- Never runs `pnpm install`, `pnpm audit`, or any package-manager command — Warden 🔒 (Dependency Warden) owns dep auditing
- Never audits markdown naming-convention compliance in isolation — Sentinel 🛡️ (Quality Guardian) owns that
- Never reviews individual file architecture (layer violations, import paths) — Atrium 🏛️ (Frontend Architect) and Bastion 🧱 (Backend Architect) own single-file architecture
- Never makes hiring decisions — Marshal 🎖️ (HR Director)
- Never researches external technologies — Augur 🔮 (Senior Research Analyst)

---

## 8. Comparison: New Agent vs. Extending Sentinel

| Dimension | New dedicated agent | Extend Sentinel |
|-----------|--------------------|-----------------------|
| Scope clarity | Clean — one contract per agent | Muddled — two unrelated rulebooks in one spec |
| Model tier | Sonnet (reasoning depth for cross-file analysis) | Sentinel is Haiku — cost-optimized for mechanical rule application; extending would require tier upgrade or degraded PR reviews |
| Bash grants | New, scoped grant (git-read + gh-comment) | Sentinel currently has Bash per its frontmatter, but uses it only implicitly; adding git-diff + gh-comment would expand an already-broad tool surface without justification |
| Trigger model | Pre-Herald, parallel with Lumen/Warden | Sentinel is triggered by Marshal after spec edits — conflicting trigger semantics |
| Output format | Findings table + gate signal + gh comment | Sentinel's output is auto-fix log + judgment-call list — incompatible shape |
| Edit permissions | Read-only on all src | Sentinel has Edit (for auto-fixing markdown) — creating a "read-only when reviewing PR, writable when fixing markdown" conditional is error-prone |
| Naming convention | Inherits existing roster style naturally | No change needed |
| Risk | Overlap with Sentinel only on report markdown (Sentinel audits the output file — additive, not conflicting) | High: scope drift baked into the spec from day one |

**Verdict:** New agent, unanimous on all decision criteria.

---

## 9. Workflow Integration

Collaborators and handoff points:

| Interaction | Direction | Content |
|-------------|-----------|---------|
| Cipher 🔓 (Dev-Team Orchestrator) | Invokes PR reviewer | Branch context, PR number (if exists), gate-chain trigger |
| PR reviewer | Reports to Cipher 🔓 | Gate signal + findings summary |
| Herald 📯 (Release Manager) | Gated by PR reviewer | Must receive [PASS] or [ADVISORY] before `gh pr create` |
| Forge 🔨 (Implementation Agent) | Fix target | Cipher routes BLOCK findings to Forge for remediation |
| Sentinel 🛡️ (Quality Guardian) | Downstream auditor | Audits `knowledge/audits/pr-*.md` files for naming-convention compliance after PR reviewer writes them |
| Warden 🔒 (Dependency Warden) | Parallel gate | Both run in parallel before Herald; PR reviewer flags package.json edits that bypassed Warden; Warden audits dep content |
| Lumen ✨ (Visual Director) | Parallel gate | Both run in parallel before Herald; independent scopes |
| Atrium 🏛️ (Frontend Architect) | Upstream verifier | Atrium's [PASS]/[FAIL]/[UNCERTAIN] on frontend files runs before PR reviewer; PR reviewer does not re-run Atrium's checks but may note if Atrium flagged items remain unresolved in the diff |
| Bastion 🧱 (Backend Architect) | Upstream verifier | Same pattern as Atrium |
| Crucible 🔥 (Test Architect) | Upstream verifier | Same pattern as Atrium |

---

## 10. Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Scope creep into Atrium/Bastion territory | Medium | Hard rule: PR reviewer flags architecture violations as "route to Atrium/Bastion for judgment" — never re-audits file architecture independently |
| Double-review of same `knowledge/audits/` report (PR reviewer writes it; Sentinel audits it) | Low | Additive, not conflicting. Sentinel only checks naming conventions; PR reviewer writes content. No collision. |
| `gh pr review` posting noise on every PR | Low | [ADVISORY] and [PASS] signals can be configured to only post when findings exist; Cipher decides verbosity preference before Marshal drafts the spec |
| Bash grant creep (git-read + gh-comment is narrow but could be extended) | Medium | Allowlist is precise and enumerated in this brief. Marshal encodes it verbatim in the runtime spec's Hard Rules. Any future expansion requires new Augur brief per CLAUDE.md rule (source: `CLAUDE.md` line 226). |
| Model cost (Sonnet vs Haiku) | Low | PR reviews are infrequent (one per PR, not per file edit). Cost impact is bounded. |

---

## Sources

| Claim | Source |
|-------|--------|
| Sentinel Hard-out list (no code review, no PR descriptions) | `.claude/agents/sentinel.md` lines 52–58 |
| Sentinel audit scope (knowledge/audits included) | `.claude/agents/sentinel.md` lines 34–43 |
| Sentinel model tier (haiku) | `.claude/agents/sentinel.md` frontmatter line 6 |
| Sentinel Bash grant (present in frontmatter) | `.claude/agents/sentinel.md` frontmatter line 5 |
| Herald Hard Rule — no AI attribution | `.claude/agents/herald.md` lines 109 (HARD RULE block) |
| Herald opens PRs, does not review them | `.claude/agents/herald.md` lines 14, 50 |
| Dev work gate chain (Lumen/Warden → Herald) | `CLAUDE.md` lines 197–203 |
| Bash grant registry and future-agent rule | `CLAUDE.md` lines 214–226 |
| Single-call rule (parallel agents) | `CLAUDE.md` line 92 |
| Existing icon inventory | `CLAUDE.md` lines 80–90 |
| Atrium scope (single-file frontend, never cross-file PR diff) | `.claude/agents/atrium.md` lines 14–15 |
| Bastion scope (single-file backend only) | `.claude/agents/bastion.md` lines 14–16 |
| Crucible scope (test files only) | `.claude/agents/crucible.md` lines 14–15 |
| Warden scope (dep/lockfile only, never git diff) | `.claude/agents/warden.md` lines 23–26 |
| knowledge/audits/ directory exists | `knowledge/audits/.gitkeep` (Glob result) |
| plans/ducat-lens-bootstrap-20260524/ exists | Glob result confirming plan.md and siblings |

---

## Open Questions for Cipher

1. **Name selection** — Cipher must choose one of the five candidates. Augur recommends Arbiter ⚖️. Praetor ⚖️ would conflict on icon if Arbiter is also a candidate; Cipher must disambiguate.

2. **Report verbosity on [PASS]** — should the PR reviewer post a `gh pr comment` even when the gate signal is [PASS] (no findings), or only when [ADVISORY] or [BLOCK]? This affects the runtime spec's trigger behavior for the GitHub comment step.

3. **AI attribution scan scope** — the current Herald Hard Rule (`.claude/agents/herald.md` line 109) covers commit/PR artifacts. Should the PR reviewer also scan all changed file contents for AI attribution strings (e.g., `Generated with Claude`, `Co-Authored-By: noreply@anthropic.com` in file bodies, not just git artifacts)? Cipher must confirm scope so Marshal can encode the exact rule.

4. **Knowledge/audits path for pre-PR reports** — when the reviewer runs before a PR number exists (manual mid-dev check), the filename pattern `pr-<N>-<date>.md` cannot use `<N>`. Proposed fallback: `pr-diff-<branch>-<date>.md`. Cipher must confirm or supply alternate convention.

5. **Sentinel audit of PR reports** — Sentinel's scope-detection rule will pick up `knowledge/audits/pr-*.md` files (contains no roster mentions by default, but scope rule #4 matches the path). Should Sentinel explicitly include or exclude these files? Marshal should update Sentinel's spec accordingly after the hire.

6. **Model tier** — Augur recommends Sonnet for reasoning depth. Cipher may override to Haiku for cost reasons; if so, the cross-file reasoning capability degrades and the scope of what the agent can reliably catch narrows.
