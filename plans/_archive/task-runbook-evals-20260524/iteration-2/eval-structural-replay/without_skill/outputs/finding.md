# Finding — bug-501 runbook scaffold

## Decision: SCAFFOLD (structural replay)

Scaffolded runbook at `tasks/bug-501/runbook/`. Prior-art search returned a strong structural match; full investigation is not required, but a per-region config confirmation step is, so the runbook is needed.

## Task

- **ID:** bug-501
- **Module:** auth.sso
- **Country:** APAC
- **Environment:** production
- **Symptom:** Users in APAC production are kicked back to login ~90s after SSO redirect; `/api/me` returns 401 with a valid-looking token.
- **SLA-due:** 2026-05-30T18:00

## Prior-art scan

Searched `_fixtures/prior-art/` (3 entries):

| Prior task | Module | Country | Match | Relevance |
|---|---|---|---|---|
| **bug-401** | auth.sso | EU | exact symptom + module | Root cause = SSO token TTL 60s + minute-boundary cron scheduler racing token expiry. Fix = continuous timer with 30s pre-expiry margin. Resolved 2026-04-14. |
| **bug-422** | auth.sso | US | exact symptom + module + structural | Same RC as bug-401; resurfaced in US because the bug-401 fix rollout was region-scoped. Same fix applied. Resolved 2026-04-20. |
| feature-001 | commerce.cart | — | none | Unrelated. |

## Replay verdict: `structural`

bug-401 and bug-422 together establish the failure mode is *recurring per region* because of region-scoped rollouts. APAC is the third region exhibiting an identical signature. The fix is known, but we still need to verify APAC config before applying it (cannot blind-apply on prior art alone — see hard rule "User-Authority-Only" / discovery-before-fix).

## H1 (high confidence)

APAC `auth.sso` session-refresh middleware still runs on the minute-boundary cron scheduler from before the bug-401 fix. Confirm/refute: inspect APAC `auth.sso` session-refresh config; check scheduler type and pre-expiry margin. If continuous-timer with >=30s pre-expiry margin → refute and reopen hypothesis budget.

## Recommended next action

1. Phase 03 (not yet scaffolded — owned by domain agent per process): pull APAC session-refresh config; verify scheduler type.
2. If H1 confirmed: prepare region-scoped rollout of the bug-401 fix to APAC; consider also widening the fix to a config audit across all regions to prevent a bug-50x recurrence.
3. KBA/RCA opportunity: this is the third recurrence of the same RC in different regions — promote bug-401's fix to a cross-region config policy.

## Files written (all under outputs dir)

- `finding.md` (this file)
- `tasks/bug-501/runbook/runbook.md`
- `tasks/bug-501/runbook/phase-01-triage.md`
- `tasks/bug-501/runbook/phase-02-priorart.md`
- `tasks/bug-501/runbook/runbook.config.yaml`
- `metrics.json`

No validator was found in the workspace; `validator-output.txt` not produced.
