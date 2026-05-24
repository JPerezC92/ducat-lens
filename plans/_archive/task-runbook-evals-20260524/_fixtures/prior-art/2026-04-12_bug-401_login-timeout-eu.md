---
identifier: bug-401
module: auth.sso
country: EU
environment: production
resolved: 2026-04-14
---

# Login timeout after SSO redirect — EU production

## Symptom
Users in EU region report being kicked back to the login screen ~90 seconds after successful SSO redirect from identity provider. Session token appears valid but `/api/me` returns 401.

## Root cause
SSO token TTL is 60s; backend session-refresh middleware reads token at minute boundaries due to cron-style scheduler. When token issuance + first request crosses a minute boundary, refresh fires AFTER token expiry. Race condition affects 100% of EU traffic during peak hours due to load-balancer affinity.

## Fix
Move session-refresh to a continuous timer with 30s pre-expiry margin. Drop minute-boundary scheduling.

## Validation
After deploy: 0 timeout reports in 72h. Synthetic monitor in EU region confirmed.
