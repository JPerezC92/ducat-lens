---
identifier: bug-422
module: auth.sso
country: US
environment: production
resolved: 2026-04-20
related: bug-401
---

# Login timeout after SSO redirect — US production

## Symptom
US users hit same login-timeout pattern as bug-401. Pattern: kicked back to login screen ~90s after SSO redirect, `/api/me` returns 401 with valid-looking token.

## Root cause
Same minute-boundary scheduler race condition documented in bug-401. US region was not patched in the original fix rollout — only EU configs were updated.

## Fix
Apply bug-401 fix to US session-refresh config. Same continuous-timer pattern.

## Validation
0 timeout reports in 72h post-deploy. US synthetic monitor green.
