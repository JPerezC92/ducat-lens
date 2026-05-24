# Audit Report — AI Attribution Contamination Sweep

**Date:** 2026-05-24  
**Executor:** Sentinel (Quality Guardian)  
**Scope:** Tracked file set (Phase 2, Plan: scrub-ai-attribution-20260524)

---

## Grep Results Summary

| Pattern | Hits | Files with hits |
|---------|------|-----------------|
| `Co-Authored-By:.*noreply@anthropic\.com` | 6 | All in allowlist |
| `Co-Authored-By:.*bot@` | 7 | All in allowlist |
| `Co-Authored-By:.*\.bot\b` | 0 | — |
| `Generated with \[Claude Code\]` | 4 | All in allowlist |
| `🤖` | 10 | All in allowlist |
| `claude\.com/claude-code` | 4 | All in allowlist |
| `openai\.com\|cursor\.sh\|copilot\.github\.com` | 4 | All in allowlist |
| `anthropic\.com` | 11 | All in allowlist |

**Total hits: 46**  
**Hits outside allowlist: 0**

---

## Hit Locations (all within allowlist)

### Pattern: `Co-Authored-By:.*noreply@anthropic\.com` (6 hits)
- `.claude/agents/herald.md:109` (allowlist: HARD RULE statement)
- `.claude/skills/git-commit/SKILL.md:78` (allowlist: HARD RULE statement)
- `.claude/skills/git-pr/SKILL.md:87` (allowlist: HARD RULE statement)
- `CLAUDE.md:185` (allowlist: Operational gates section)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:32` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/plan.md:32` (allowlist: plan file)

### Pattern: `Co-Authored-By:.*bot@` (7 hits)
- `.claude/agents/herald.md:109` (allowlist: HARD RULE statement)
- `.claude/skills/git-commit/SKILL.md:78` (allowlist: HARD RULE statement)
- `.claude/skills/git-pr/SKILL.md:87` (allowlist: HARD RULE statement)
- `CLAUDE.md:185` (allowlist: Operational gates section)
- `plans/scrub-ai-attribution-20260524/phase-02-sentinel-audit.md:26` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:32` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/plan.md:32` (allowlist: plan file)

### Pattern: `Co-Authored-By:.*\.bot\b` (0 hits)
- None found.

### Pattern: `Generated with \[Claude Code\]` (4 hits)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:16` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:24` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:34` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/plan.md:12` (allowlist: plan file)

### Pattern: `🤖` (10 hits)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:16` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:24` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:34` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/plan.md:12` (allowlist: plan file)
- `.claude/agents/herald.md:109` (allowlist: HARD RULE statement)
- `.claude/skills/git-commit/SKILL.md:78` (allowlist: HARD RULE statement)
- `.claude/skills/git-pr/SKILL.md:87` (allowlist: HARD RULE statement)
- `CLAUDE.md:185` (allowlist: Operational gates section)
- `agents/herald/profile.md:40` (allowlist: persona CV)
- `plans/scrub-ai-attribution-20260524/phase-02-sentinel-audit.md:29` (allowlist: plan file)

### Pattern: `claude\.com/claude-code` (4 hits)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:24` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:34` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/plan.md:35` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-03-herald-initial-push.md:70` (allowlist: plan file)

### Pattern: `openai\.com|cursor\.sh|copilot\.github\.com` (4 hits)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:25` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/plan.md:35` (allowlist: plan file)
- `agents/herald/profile.md:40` (allowlist: persona CV)
- `plans/scrub-ai-attribution-20260524/phase-03-herald-initial-push.md:70` (allowlist: plan file)

### Pattern: `anthropic\.com` (11 hits)
- `.claude/agents/herald.md:109` (allowlist: HARD RULE statement)
- `.claude/skills/git-commit/SKILL.md:78` (allowlist: HARD RULE statement)
- `.claude/skills/git-pr/SKILL.md:87` (allowlist: HARD RULE statement)
- `CLAUDE.md:185` (allowlist: Operational gates section)
- `agents/herald/profile.md:40` (allowlist: persona CV)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:25` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md:32` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/plan.md:32` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/plan.md:35` (allowlist: plan file)
- `plans/scrub-ai-attribution-20260524/phase-03-herald-initial-push.md:70` (allowlist: plan file)

---

## Allowlist Verification

All 46 hits land within the allowlist:

- `plans/scrub-ai-attribution-20260524/plan.md` ✓
- `plans/scrub-ai-attribution-20260524/phase-01-marshal-template-scrub.md` ✓
- `plans/scrub-ai-attribution-20260524/phase-02-sentinel-audit.md` ✓
- `plans/scrub-ai-attribution-20260524/phase-03-herald-initial-push.md` ✓
- `.claude/skills/git-commit/SKILL.md` ✓
- `.claude/skills/git-pr/SKILL.md` ✓
- `.claude/agents/herald.md` ✓
- `agents/herald/profile.md` ✓
- `CLAUDE.md` ✓

---

## Conclusion

No AI-attribution contamination detected outside the allowlist. All pattern hits are legitimate references to the rule statement itself (as documented in Phase 1 edits).

**Phase 1 verification (abort condition check):**
- `.claude/skills/git-commit/SKILL.md` contains `agent-agnostic` ✓
- `.claude/skills/git-pr/SKILL.md` contains `agent-agnostic` ✓
- `.claude/agents/herald.md` contains `agent-agnostic` ✓
- `agents/herald/profile.md` contains `agent-agnostic` ✓
- `CLAUDE.md` contains `agent-agnostic` ✓

All 5 Phase-1-edited files verified as containing the rule statement.

VERDICT: PASS
