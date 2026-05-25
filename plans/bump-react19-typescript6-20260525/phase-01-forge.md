# Phase 01 — Edit package.json pins

## Owner

Forge 🔨 (Implementation Agent)

## Pre

- Active plan exists: `plans/bump-react19-typescript6-20260525/plan.md`
- Pre-coding sync gate passed: `git rev-list HEAD..origin/main --count` = 0
- Working branch created by Cipher

## Reads

- `frontend/package.json` — current dep versions

## Writes

- `frontend/package.json` — 5 version pins updated

## Steps

1. Read `frontend/package.json` (verify current content matches known state before editing)
2. Edit `dependencies.react`: `"18.3.1"` → `"19.2.6"`
3. Edit `dependencies.react-dom`: `"18.3.1"` → `"19.2.6"`
4. Edit `devDependencies.@types/react`: `"18.3.29"` → `"19.2.15"`
5. Edit `devDependencies.@types/react-dom`: `"18.3.7"` → `"19.2.3"`
6. Edit `devDependencies.typescript`: `"5.9.3"` → `"6.0.3"`
7. Verify no other package versions changed; verify all 5 new values are exact pins (no `^`, `~`, `>=`, `latest`)

## Output

- `frontend/package.json` — updated with 5 exact pins as listed in phase index table

## Gate

- Diff of `frontend/package.json` shows exactly 5 version lines changed
- All 5 new values are bare version strings (no range operators)
- No other packages added, removed, or version-changed

## Abort conditions

- Any non-target package version changed → halt, revert, report to Cipher
- Edit tool reports error → halt, report to Cipher
