"""
Inline grader for task-runbook eval runs.

Reads eval_metadata.json from each eval dir, evaluates each assertion against
the run's outputs/, and writes grading.json per run dir.

Assertion check_types supported:
    - file_exists       — path relative to outputs/ must exist
    - file_not_exists   — path must NOT exist
    - file_contains     — file must exist AND contain regex pattern
    - glob_exists       — glob pattern must match ≥1 file
    - any_of            — at least one nested check passes

Usage:
    python _grade.py <iteration_dir>

Writes:
    <run_dir>/grading.json per run found.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any


def check_file_exists(outputs_dir: Path, spec: dict) -> tuple[bool, str]:
    target = outputs_dir / spec["path"]
    if target.is_file():
        return True, f"file present: {target.relative_to(outputs_dir)}"
    return False, f"file missing: {target.relative_to(outputs_dir) if target.is_relative_to(outputs_dir) else spec['path']}"


def check_file_not_exists(outputs_dir: Path, spec: dict) -> tuple[bool, str]:
    target = outputs_dir / spec["path"]
    if target.is_file():
        return False, f"file should not exist but does: {spec['path']}"
    return True, f"file correctly absent: {spec['path']}"


def check_file_contains(outputs_dir: Path, spec: dict) -> tuple[bool, str]:
    target = outputs_dir / spec["path"]
    if not target.is_file():
        return False, f"file missing: {spec['path']}"
    content = target.read_text(encoding="utf-8")
    pattern = spec["pattern"]
    if re.search(pattern, content):
        return True, f"pattern matched in {spec['path']}"
    return False, f"pattern {pattern!r} not found in {spec['path']}"


def check_glob_exists(outputs_dir: Path, spec: dict) -> tuple[bool, str]:
    pattern = spec["pattern"]
    matches = list(outputs_dir.glob(pattern))
    if matches:
        names = [m.relative_to(outputs_dir).as_posix() for m in matches]
        return True, f"glob matched {len(matches)} file(s): {names}"
    return False, f"glob {pattern!r} matched zero files"


def check_any_of(outputs_dir: Path, spec: dict) -> tuple[bool, str]:
    for sub in spec["options"]:
        ok, evidence = check_assertion(outputs_dir, sub)
        if ok:
            return True, f"any-of satisfied: {evidence}"
    return False, "no any-of option satisfied"


CHECKERS = {
    "file_exists": check_file_exists,
    "file_not_exists": check_file_not_exists,
    "file_contains": check_file_contains,
    "glob_exists": check_glob_exists,
    "any_of": check_any_of,
}


def check_assertion(outputs_dir: Path, spec: dict) -> tuple[bool, str]:
    ct = spec["check_type"]
    if ct not in CHECKERS:
        return False, f"unknown check_type: {ct}"
    return CHECKERS[ct](outputs_dir, spec)


def grade_run(run_dir: Path, eval_metadata: dict) -> dict:
    # Assertions in eval_metadata.json use paths like "outputs/finding.md" —
    # resolve relative to run_dir, not run_dir/outputs.
    base = run_dir
    expectations: list[dict[str, Any]] = []

    for assertion in eval_metadata["assertions"]:
        passed, evidence = check_assertion(base, assertion)
        expectations.append({
            "text": assertion["text"],
            "passed": passed,
            "evidence": evidence,
        })

    passed_count = sum(1 for e in expectations if e["passed"])
    total = len(expectations)

    return {
        "expectations": expectations,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": round(passed_count / total, 3) if total else 0.0,
        },
    }


def main(iteration_dir: str) -> int:
    base = Path(iteration_dir)
    if not base.is_dir():
        print(f"ERROR: iteration dir not found: {iteration_dir}", file=sys.stderr)
        return 1

    eval_dirs = sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith("eval-"))
    if not eval_dirs:
        print(f"ERROR: no eval-* dirs found under {iteration_dir}", file=sys.stderr)
        return 1

    grades_written = 0

    grading_dir = base / "_grading"

    for eval_dir in eval_dirs:
        # Two layouts supported:
        #   iter-1: <eval>/eval_metadata.json (inline, contaminates baselines)
        #   iter-2: <iter>/_grading/<eval-name>.json (isolated)
        isolated = grading_dir / f"{eval_dir.name}.json"
        inline = eval_dir / "eval_metadata.json"

        if isolated.is_file():
            metadata_path = isolated
        elif inline.is_file():
            metadata_path = inline
        else:
            print(f"SKIP: {eval_dir.name} has no metadata in either layout", file=sys.stderr)
            continue

        eval_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

        for config in ("with_skill", "without_skill"):
            run_dir = eval_dir / config
            if not run_dir.is_dir():
                continue

            grading = grade_run(run_dir, eval_metadata)
            grading_path = run_dir / "grading.json"
            grading_path.write_text(json.dumps(grading, indent=2), encoding="utf-8")
            grades_written += 1

            s = grading["summary"]
            print(f"  {eval_dir.name}/{config}  {s['passed']}/{s['total']}  ({s['pass_rate']:.0%})")

    print(f"\nWrote {grades_written} grading.json files.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
