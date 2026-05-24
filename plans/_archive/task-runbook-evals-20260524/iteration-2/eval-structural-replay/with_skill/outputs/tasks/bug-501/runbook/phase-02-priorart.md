# Phase 02 — Prior art (adapted — replay-structural)

> **Owner:** investigation agent
> **Pre:** Phase 01 complete; prior-art scan completed at scaffold time
> **Reads:** prior-art catalog (`.claude/skills/task-runbook-workspace/_fixtures/prior-art/`)
> **Writes:** validation evidence confirming or refuting inherited hypothesis

Verdict pre-set: **replay-structural**. Hypothesis inherited from `2026-04-12_bug-401_login-timeout-eu.md` (minute-boundary scheduler race in session-refresh middleware). The "frame hypothesis" step is skipped per skill Section 4.3 — do NOT re-frame.

Adapted from `.claude/skills/task-runbook-workspace/_fixtures/prior-art/2026-04-12_bug-401_login-timeout-eu.md` and the US replay `2026-04-18_bug-422_login-timeout-us.md`. The US case is the closest precedent: same root cause as EU, surfaced in another region because the original rollout did not patch that region's config. APAC is hypothesized to be in the same unpatched-region state.

## Steps

1. Pull session-refresh middleware config for APAC region; compare against EU/US post-fix config (continuous timer, 30s pre-expiry margin). Adapted from bug-401 fix; bug-422 confirms the gap is per-region config drift.
2. Confirm SSO token TTL in APAC is 60s (matches EU/US baseline). If different, hypothesis weakens — escalate to replay-no.
3. Reproduce: capture a session in APAC production crossing a minute boundary between token issuance and first `/api/me` call. Expect 401 if unpatched.
4. If reproduction confirms and APAC config still uses minute-boundary scheduler → apply bug-401 fix to APAC (same continuous-timer pattern bug-422 used).
5. Post-deploy validation: 0 timeout reports in 72h + APAC synthetic monitor green (mirrors bug-401 / bug-422 validation).

## Output

- Validation result: pattern confirmed (apply fix) OR pattern refuted (escalate verdict to replay-no, re-open hypothesis framing)
- Updated runbook.md finding block with APAC-specific evidence

## Gate

- Replay-candidate field set to verdict (already `structural`; downgrade to `no` if pattern refuted)
- Steps 1–3 produce evidence either way before any fix is dispatched

## Abort conditions

- APAC SSO token TTL differs from EU/US baseline (hypothesis no longer transfers)
- Reproduction does NOT trigger 401 at minute boundary → escalate to replay-no, restore hypothesis framing
- Ambiguous match between two equally strong prior cases (n/a here — bug-401 is the canonical source; bug-422 is a confirming replay)
