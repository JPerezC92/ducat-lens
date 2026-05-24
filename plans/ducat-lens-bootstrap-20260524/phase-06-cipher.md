# Phase 06 — Skill evals cycle (skill-creator workflow)

## Owner

Cipher 🔓 (L2 Lead) — drives skill-creator workflow; spawns subagents for runs; grades results; iterates

## Pre

- Phase 04 PASS (validator refactored, tests green, fixtures exist)
- Phase 05 PASS (SKILL.md drafted, Sentinel 🛡️ clean)
- `claude-api:skill-creator` skill loaded and understood

## Reads

- `D:/projects/ducat-lens/.claude/skills/task-runbook/SKILL.md`
- `D:/projects/ducat-lens/.claude/skills/task-runbook/scripts/validate_runbook.py`
- `D:/projects/ducat-lens/.claude/skills/task-runbook/references/*` (all)
- skill-creator references: `references/schemas.md`, `agents/grader.md`

## Writes

- `D:/projects/ducat-lens/.claude/skills/task-runbook/evals/evals.json`
- `D:/projects/ducat-lens/.claude/skills/task-runbook-workspace/iteration-1/eval-<NAME>/with_skill/outputs/`
- `D:/projects/ducat-lens/.claude/skills/task-runbook-workspace/iteration-1/eval-<NAME>/without_skill/outputs/`
- `D:/projects/ducat-lens/.claude/skills/task-runbook-workspace/iteration-1/benchmark.json` + `benchmark.md`
- `D:/projects/ducat-lens/.claude/skills/task-runbook-workspace/iteration-1/feedback.json` (from user via viewer)

## Steps

1. **Write `evals/evals.json`** with 3 realistic test prompts that exercise each verdict tier:
   - Eval 1 (`novel-task-scaffold`): user starts new investigation with no prior art match → expect full scaffold + validator runs clean
   - Eval 2 (`exact-replay`): user provides task-id similar to an existing entry in a fixture prior-art dir → expect `replay-yes` verdict, finding returned, no scaffold
   - Eval 3 (`structural-replay`): user provides task-id matching pattern of fixture entry but different identifying values → expect `replay-structural` verdict, partial scaffold
   Each eval includes `prompt`, `expected_output`, optional `files` (fixture prior-art entries), and starter `expectations` list.
2. **Set up fixture prior-art dir** at `.claude/skills/task-runbook-workspace/_fixtures/prior-art/` with 2-3 sample `.md` entries (clearly synthetic, no Belcorp data) so eval 2 and 3 have something to match against.
3. **Spawn 6 subagents in parallel** (one assistant message, multiple `Agent` tool calls): for each eval, one `with_skill` agent + one `without_skill` baseline agent. Each agent receives:
   - skill path (`with_skill` only): `.claude/skills/task-runbook/`
   - prompt: from `evals.json`
   - input files: fixture prior-art dir
   - output dir: `task-runbook-workspace/iteration-1/eval-<NAME>/{with_skill,without_skill}/outputs/`
4. **Capture timing data** from each subagent completion notification into `<run-dir>/timing.json`. This is the only opportunity.
5. **Draft assertions** while runs are in progress. For each eval, write 3-5 verifiable assertions covering verdict correctness, file presence, validator exit code, output format. Update `evals.json` and per-eval `eval_metadata.json`.
6. **Spawn grader** subagent per run (or grade inline). Save `grading.json` per run dir with `expectations[].{text, passed, evidence}` schema.
7. **Aggregate benchmark.** Run `python -m scripts.aggregate_benchmark task-runbook-workspace/iteration-1 --skill-name task-runbook` from the skill-creator path. Produces `benchmark.json` + `benchmark.md`.
8. **Analyst pass.** Read benchmark; identify non-discriminating assertions, high-variance evals, time/token tradeoffs. Append observations to `benchmark.json` `notes` array.
9. **Launch viewer.** `nohup python <skill-creator-path>/eval-viewer/generate_review.py task-runbook-workspace/iteration-1 --skill-name task-runbook --benchmark task-runbook-workspace/iteration-1/benchmark.json &`. Tell user: "Outputs tab + Benchmark tab. Submit when done."
10. **Read feedback.** When user signals done, read `feedback.json`. Empty feedback = approval. Specific complaints = iteration trigger.
11. **Iterate if needed.** If feedback non-empty: improve SKILL.md per skill-creator guidance (generalize, lean, explain why, bundle helper scripts if subagents independently wrote the same one). Rerun all 6 subagents into `iteration-2/`. Launch viewer with `--previous-workspace task-runbook-workspace/iteration-1`. Repeat up to 3 iterations or until user approves.
12. **Description optimization (optional).** After user approves skill content, offer to run `run_loop.py` for description-trigger optimization. User decides go/no-go.
13. **Kill viewer.** `kill $VIEWER_PID` when done.

## Output

- `evals/evals.json` with 3 evals, full schema (prompt + expectations)
- `task-runbook-workspace/iteration-N/` with: 6 run dirs (3 evals × 2 configs), benchmark.json, benchmark.md, feedback.json
- User signoff that skill quality is acceptable

## Gate

- `evals.json` schema-valid (3 evals, each with id / prompt / expectations)
- All 6 subagent runs completed (no abort errors)
- `benchmark.json` produced with valid schema (matches `references/schemas.md`)
- User reviewed via viewer and either approved or submitted feedback
- If feedback received: at least one iteration performed AND user re-reviews
- Sentinel 🛡️ audit PASS on final SKILL.md (post-iteration)

## Abort conditions

- skill-creator scripts unavailable (`aggregate_benchmark`, `generate_review.py` not in expected paths) → halt, ask Cipher 🔓 to investigate skill-creator install
- 3 iterations completed without user approval → halt, escalate to Cipher 🔓; reassess whether skill design is fundamentally flawed
- Benchmark shows with_skill < without_skill on pass rate (skill HURTS performance) → halt, root-cause before any further iteration

## MCP whitelist/blacklist

- Allowed: Read, Glob, Grep, Write, Edit, Bash (subagent spawning + python scripts + viewer launch), Agent (subagents per eval)
- Forbidden: WebFetch, WebSearch
