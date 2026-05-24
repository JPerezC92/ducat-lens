# Hand-off finding — bug-455

- **Task ID:** bug-455
- **Module:** auth.sso
- **Country:** EU
- **Environment:** production
- **Deadline:** 2026-05-30T18:00
- **Symptom:** Users in EU production are kicked back to the login screen ~90 seconds after SSO redirect; `/api/me` returns 401 with a valid-looking token.

## Verdict: replay-yes

## Prior-art scan

Scanned `D:/projects/ducat-lens/.claude/skills/task-runbook-workspace/_fixtures/prior-art/`:

| File | Identifier | Module | Country | Match strength |
|---|---|---|---|---|
| `2026-04-12_bug-401_login-timeout-eu.md` | bug-401 | auth.sso | EU | **exact** — same module, same country, same symptom (kicked back to login ~90s after SSO redirect, `/api/me` 401 with valid-looking token) |
| `2026-04-18_bug-422_login-timeout-us.md` | bug-422 | auth.sso | US | structural — same root cause as bug-401, different region (US); confirmed replay of bug-401 |
| `2026-05-02_feature-001_cart-desktop.md` | feature-001 | commerce.cart | — | no match (unrelated module) |

## Matched prior-art: bug-401

- **Root cause (per bug-401):** SSO token TTL is 60s; backend session-refresh middleware reads token at minute boundaries (cron-style scheduler). When token issuance + first request crosses a minute boundary, the refresh fires after token expiry. Race condition affected 100% of EU traffic during peak hours due to load-balancer affinity.
- **Original fix (per bug-401):** Replace minute-boundary scheduler with a continuous timer carrying a 30s pre-expiry margin.
- **bug-422 evidence:** The same pattern recurred in US because the EU-only fix rollout did not patch US configs. Region-scoped rollout is a known regression vector for this defect.

## Recommendation: reuse prior solution — do not scaffold a fresh runbook

The symptom phrasing in bug-455 is identical to bug-401 down to the timing (90s) and the `/api/me` 401 detail. Per prior-art scan policy (exact match → replay-yes → skip scaffold), no `tasks/bug-455/runbook/` directory was created. Hand off to the owner of the auth.sso session-refresh config with this brief:

1. **Reuse the bug-401 fix** — verify the continuous-timer + 30s pre-expiry margin is in fact deployed to EU production. If the config was rolled back, re-deploy.
2. **Check for region drift** — bug-422 proved that the fix can be missing in one region while present in others. Diff EU vs US vs any other region's session-refresh config and align all regions on the continuous-timer pattern.
3. **Confirm via synthetic monitor** — bug-401 closed on 72h of zero timeout reports plus EU synthetic monitor green. Re-run the same validation.
4. **If continuous-timer IS deployed in EU and the symptom still reproduces** — escalate as a new defect (different root cause masquerading as bug-401); only then scaffold a fresh runbook.

## Why scaffold was skipped

The eval/skill contract treats `replay-yes` as a signal that the investigation runbook is unnecessary — the prior-art entry already carries the diagnosis, fix, and validation. Scaffolding a runbook would force the owner to re-derive what bug-401 already documents. The hand-off above adjusts the known prior solution for bug-455 (verify deploy state, check region drift) rather than restart investigation from triage.

## Deadline check

Deadline 2026-05-30T18:00; today 2026-05-24. Six days of runway — ample for a config-verify + region-diff + synthetic-monitor pass.
