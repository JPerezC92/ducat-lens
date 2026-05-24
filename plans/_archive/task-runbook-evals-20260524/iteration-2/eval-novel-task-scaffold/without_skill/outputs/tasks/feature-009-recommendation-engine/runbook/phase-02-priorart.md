# Phase 02 — Prior art

> **Owner:** <fill>
> **Pre:** Phase 01 complete
> **Reads:** prior-art catalog
> **Writes:** prior-art finding block

## Steps

1. Scan prior-art directory for matches on identifier / module / symptom.
2. Note match-strength per hit.

## Output

- Finding block in runbook.md

## Gate

- Replay-candidate field set to verdict

## Abort conditions

- Ambiguous match between two equally strong prior cases

## Prior-art finding (initial scan, 2026-05-24)

Searched `_fixtures/prior-art/` for hits on `ml.recommender`, `recommendation`, `collaborative filtering`, `home page`.

| Prior entry | Module | Match? |
|---|---|---|
| 2026-04-12_bug-401_login-timeout-eu | auth.sso | No |
| 2026-04-18_bug-422_login-timeout-us | auth.sso | No |
| 2026-05-02_feature-001_cart-desktop | commerce.cart | No |

Verdict: **no prior-art match**. Replay-candidate = `no`. Proceed with fresh design phases.
