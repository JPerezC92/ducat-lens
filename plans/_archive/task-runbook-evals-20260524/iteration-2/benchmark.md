# Benchmark — task-runbook iteration-2 (clean baselines)

**Date:** 2026-05-24
**Changes from iter-1:** `eval_metadata.json` moved to `_grading/<eval-name>.json` (sibling, hidden from executors). All 3 baselines re-spawned. `with_skill` runs copied verbatim (no skill changes).

## Aggregate

| Configuration | Pass rate | Time (s) | Tokens |
|---|---|---|---|
| `with_skill` | **100%** (17/17) | 158.9 | 55,280 |
| `without_skill` (clean) | 88.9% (15/17) | 148.8 | 48,643 |
| Δ | **+11.1%** | +10.1 | +6,637 |

## Per-eval

| Eval | with_skill | without_skill |
|---|---|---|
| novel-task-scaffold | 6/6 (100%) | 5/6 (83%) — missed "validator was invoked" |
| exact-replay | 5/5 (100%) | 5/5 (100%) — baseline reasoned correctly |
| structural-replay | 6/6 (100%) | 5/6 (83%) — missed "APAC identified as differing value" |

## Headline findings

1. **Clean baseline confirms skill value is moderate** — eval prompts are well-specified enough that a competent agent solves the core problem (verdict + scaffold) without the skill. Skill differentiates on **structural rigor** (validator integration, identifier-source chaining wording).
2. **Sole differentiating assertions are 2 across 3 evals** — validator invocation (eval-1) + APAC differentiator wording (eval-3).
3. **Skill cost** — +6.8% time, +13.6% tokens vs clean baseline. Cheaper than iter-1 false delta.
4. **Verdict correctness is not skill-differentiated for these prompts** — all 6 runs (3 evals × 2 configs) reached the correct verdict label. Skill makes the verdict **reproducibly correct under structure**, but does not unlock correctness baseline agents lack.

## Assertion design caveat

Current assertions check verdict labels + file presence. A cargo-cult output that names the right verdict passes the same as a deeply reasoned one. To measure semantic depth: add LLM-judge assertions like "does the finding explain WHY this is structural (not exact) replay" or "does the partial scaffold actually omit the hypothesis phase per Section 4.3".

## Skill verdict

**Ship v1.0.0.** Real but moderate value over a competent baseline. Best ROI in:
- Validator integration (knows where to invoke + with which config)
- Identifier-source chaining for structural-replay
- Consistent output format (finding block schema)
- Sectioned discipline (replay-yes halts cleanly; replay-structural produces partial scaffold per Section 4.3)

Low-priority future iterations:
- LLM-judge assertions for semantic depth
- Eval 4: ambiguous match (halt-and-ask path)
- Eval 5: empty prior-art dir (degradation behavior)
