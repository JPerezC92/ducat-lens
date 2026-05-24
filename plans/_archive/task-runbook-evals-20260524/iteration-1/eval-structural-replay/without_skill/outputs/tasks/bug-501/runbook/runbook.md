---
Phase: 1
Updated: 2026-05-24T00:00
SLA-due: 2026-05-30T18:00
Replay-candidate: structural
Hypotheses-outstanding: 1/3
Query-budget: 6/6
Same-query-reruns: 0/2
---

# Runbook

Task ID: bug-501
Module: auth.sso
Symptom: Users in APAC production are being kicked back to the login screen ~90 seconds after SSO redirect; `/api/me` returns 401 with a valid-looking token.

## Prior-art finding

Structural replay of bug-401 (EU) and bug-422 (US). Both share identical symptom signature (90s timeout, `/api/me` 401, valid-looking token) in module `auth.sso`. Root cause in both cases: minute-boundary scheduler race in session-refresh middleware; SSO token TTL 60s, refresh fires after expiry when issuance crosses a minute boundary.

- bug-401 (2026-04-14, EU): root cause identified; fix = continuous timer with 30s pre-expiry margin.
- bug-422 (2026-04-20, US): same root cause; rollout gap — US configs not patched in original EU fix.

APAC appears to be the same untreated rollout gap. Replay-candidate: **structural**.
