# Finding — bug-501 (auth.sso, APAC, production)

## Decision

**Scaffolded** runbook at `tasks/bug-501/runbook/` using template directory.

## Prior-art verdict: structural replay

Two strong prior-art matches on identical symptom signature in module `auth.sso`:

| Prior case | Region | Date | Match strength |
|---|---|---|---|
| bug-401 | EU | 2026-04-14 | Strong — identical symptom (90s timeout, `/api/me` 401, valid-looking token) |
| bug-422 | US | 2026-04-20 | Strong — identical symptom, explicit related-to bug-401, rollout gap pattern |

## Root cause (replayed)

SSO token TTL is 60s. Backend session-refresh middleware reads token at minute boundaries (cron-style scheduler). When token issuance + first request crosses a minute boundary, refresh fires AFTER token expiry. Race condition.

bug-401 fix (continuous timer with 30s pre-expiry margin) was rolled out to EU only. bug-422 confirmed US was an untreated rollout gap with the same root cause. APAC fits the same untreated-gap pattern.

## Recommended action (handed off, NOT executed)

1. Verify APAC session-refresh config still uses minute-boundary scheduler (configuration check, not investigation).
2. Apply bug-401 fix pattern to APAC: continuous timer with 30s pre-expiry margin.
3. Validate post-deploy with APAC synthetic monitor + 72h timeout-report count (per bug-401/bug-422 validation pattern).

## SLA

Deadline 2026-05-30T18:00 — comfortable runway for a config-rollout fix replicating a known-good patch.

## Scaffold contents

- `tasks/bug-501/runbook/runbook.md` — header with Replay-candidate=`structural`, prior-art finding block
- `tasks/bug-501/runbook/phase-01-triage.md` — populated from template
- `tasks/bug-501/runbook/phase-02-priorart.md` — populated with the three prior-art match outcomes
- `tasks/bug-501/runbook/runbook.config.yaml` — copied verbatim from template

Phases 03+ not scaffolded — structural replay skips fresh hypothesis framing; remaining work is apply-and-validate against a known fix.

## Validator

No validator script located under `task-runbook-workspace/`. `validator-output.txt` not produced.
