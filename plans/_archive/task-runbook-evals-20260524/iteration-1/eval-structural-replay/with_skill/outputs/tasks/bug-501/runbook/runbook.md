---
Phase: 1
Updated: 2026-05-24T00:00
SLA-due: 2026-05-30T18:00
Replay-candidate: structural
Hypotheses-outstanding: 0/3
Query-budget: 6/6
Same-query-reruns: 0/2
Identifier-source: bug-401
---

# Runbook

Task ID: bug-501
Module: auth.sso
Symptom: Users in APAC production are being kicked back to the login screen about 90 seconds after SSO redirect; /api/me returns 401 with a valid-looking token

## Prior-art finding

- Verdict: replay-structural
- Matched prior: `.claude/skills/task-runbook-workspace/_fixtures/prior-art/2026-04-12_bug-401_login-timeout-eu.md` (primary)
- Related prior: `.claude/skills/task-runbook-workspace/_fixtures/prior-art/2026-04-18_bug-422_login-timeout-us.md`
- Matched fields: module (auth.sso), symptom-keywords (90s SSO redirect, /api/me 401, valid-looking token)
- Differing identifying value: country (APAC vs EU / US)
- Inherited hypothesis: minute-boundary scheduler race in session-refresh middleware — APAC region likely not patched in prior rollout (same gap pattern as US in bug-422).
