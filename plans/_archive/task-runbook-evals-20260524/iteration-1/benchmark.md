# Benchmark — task-runbook iteration-1

**Date:** 2026-05-24
**Runs per configuration:** 1
**Evals:** novel-task-scaffold, exact-replay, structural-replay

## Aggregate

| Configuration | Pass rate | Time (s) | Tokens |
|---|---|---|---|
| `with_skill` | **100%** (17/17) | 158.9 (87.9–242.6) | 55,280 |
| `without_skill` | 88.9% (15/17) | 129.8 (106.1–175.5) | 47,609 |
| Δ | **+11.1%** | +29.1 | +7,671 |

## Per-eval

| Eval | with_skill | without_skill |
|---|---|---|
| novel-task-scaffold | 6/6 (100%) — 146s / 57K tokens | 5/6 (83%) — 175s / 47K tokens ⚠️ contaminated |
| exact-replay | 5/5 (100%) — 88s / 51K tokens | 5/5 (100%) — 106s / 48K tokens ⚠️ contaminated |
| structural-replay | 6/6 (100%) — 243s / 58K tokens | 5/6 (83%) — 108s / 48K tokens ⚠️ contaminated |

## Headline findings

1. **`with_skill` perfect across all 3 evals** — every verdict tier triggered correctly, every assertion satisfied.
2. **Baseline contamination invalidates comparison** — all 3 baseline subagents likely read sibling `eval_metadata.json`. True baseline performance is unknown. Iteration 2 must isolate metadata from executor's working tree.
3. **Skill cost = +22% time, +16% tokens** — full SKILL.md reading before acting. Acceptable trade for the structural rigor.
4. **Longest run is structural-replay with_skill (243s)** — Section 4.3 partial-scaffold logic + identifier-source chaining is the most complex skill path.
5. **Assertion design gap** — assertions check presence + verdict labels, not semantic depth. A hallucinated but well-labeled output passes. Future iterations should add LLM-judge assertions for "does the finding's reasoning actually hold up."

## Recommended next steps

| Priority | Action |
|---|---|
| HIGH | Iteration 2: move `eval_metadata.json` to `_grading/` sibling not visible to executor |
| MED | Add 1-2 LLM-judge assertions per eval ("does the prior-art match reasoning actually hold up?") |
| LOW | Add eval 4: ambiguous match (two prior-art entries match equally well) — should trigger halt-and-ask, NOT auto-scaffold |
| LOW | Run 3 iterations per config to compute meaningful stddev |
