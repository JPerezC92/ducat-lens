```
verdict:        replay-structural
prior-art:      .claude/skills/task-runbook-workspace/_fixtures/prior-art/2026-04-12_bug-401_login-timeout-eu.md
matched-fields: [module, symptom-keywords]
runbook:        .claude/skills/task-runbook-workspace/iteration-1/eval-structural-replay/with_skill/outputs/tasks/bug-501/runbook/
validator:      pass
recommended:    Adapted scaffold at tasks/bug-501/runbook/. Hypothesis pre-populated from 2026-04-12_bug-401_login-timeout-eu.md (and confirming replay 2026-04-18_bug-422_login-timeout-us.md). Dispatch validation agent to verify the minute-boundary scheduler race pattern reproduces in APAC production before applying the bug-401 continuous-timer fix.
```

## Match detail

- Module match: `auth.sso` == `auth.sso` (bug-401, bug-422)
- Symptom-keyword overlap: "kicked back to login screen", "~90 seconds after SSO redirect", "/api/me returns 401", "valid-looking token"
- Differing identifying value: country = APAC (priors: EU, US)
- Identifier overlap: none (different bug ID)
- Match criterion satisfied: 2 of 3 (module + symptom-keywords) — meets Section 2.1 threshold

## Verdict rationale (Section 3 ladder)

- Not `replay-yes`: identifying value (country) differs from both priors — APAC was not the patched region in either bug-401's original rollout or bug-422's US backport.
- `replay-structural`: same module + same failure-mode chain (minute-boundary scheduler race in session-refresh middleware) but different region. bug-422 already established the recurrence pattern (per-region config drift after partial rollout); APAC is the next region in that chain.
- Hypothesis inherited; "frame hypothesis" phase skipped per Section 4.3.
