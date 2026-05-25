"""
Validate a plan directory: header fields, phase files, and required sections.

Usage:
    python validate_plan.py <plan_dir>                              # full validation
    python validate_plan.py <plan_dir> --config <path>              # explicit config
    python validate_plan.py <plan_dir> --phase NN                   # single-phase check

Config loading order:
    1. ``--config <path>`` if provided
    2. ``<plan_dir>/plan.config.yaml`` if present
    3. None — only checks plan file exists and parses as YAML frontmatter

Full validation:
    - Validates the plan header fields per ``required_headers`` config.
    - Checks that phase files exist and contain required sections.
    - Emits a phase-by-phase status table to stdout on success.

Single-phase validation (``--phase NN``):
    - Validates the plan header as above.
    - Checks ONLY the specified phase file for required sections.

Exit codes:
    0 — all checks pass (warnings do not affect exit code)
    1 — one or more violations found
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml

# ---------------------------------------------------------------------------
# Schema version
# ---------------------------------------------------------------------------
_SUPPORTED_VERSIONS: frozenset[str] = frozenset({"1.0"})


# ---------------------------------------------------------------------------
# Config dataclasses
# ---------------------------------------------------------------------------


@dataclass
class HeaderSpec:
    name: str
    type: str  # string | int | datetime | enum
    format: Optional[str] = None  # strftime format for datetime
    allowed: Optional[list[str]] = None  # enum allowed values
    regex: Optional[str] = None  # optional additional pattern


@dataclass
class PhaseFilesSpec:
    pattern: str
    number_extract_regex: str = r"^phase-(\d+)-"
    required: Optional[list[str]] = None


@dataclass
class PlanConfig:
    version: str
    plan_file: str = "plan.md"
    phase_files: Optional[PhaseFilesSpec] = None
    required_headers: list[HeaderSpec] = field(default_factory=list)
    required_sections: list[str] = field(default_factory=list)
    required_blockquote_labels: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------


class ConfigError(Exception):
    """Raised when the config file cannot be parsed or has an unsupported version."""


def _load_raw_config(config_path: Path) -> dict[str, Any]:
    """Read and parse a YAML config file.

    Raises ``ConfigError`` on IO or parse failure.
    """
    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"Cannot read config file {config_path}: {exc}") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ConfigError(f"Malformed YAML in {config_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"Config file {config_path} must be a YAML mapping")
    return data


def _build_config(data: dict[str, Any], config_path: Path) -> PlanConfig:
    """Validate top-level version and construct a ``PlanConfig`` from raw dict.

    Raises ``ConfigError`` on unsupported version or structural errors.
    """
    version = str(data.get("version", "")).strip()
    if not version:
        raise ConfigError(f"Config {config_path} is missing required 'version' field")
    if version not in _SUPPORTED_VERSIONS:
        supported = ", ".join(sorted(_SUPPORTED_VERSIONS))
        raise ConfigError(
            f"Config {config_path} has unsupported version {version!r}. "
            f"Supported: {supported}"
        )

    cfg = PlanConfig(version=version)
    cfg.plan_file = str(data.get("plan_file", "plan.md"))

    # phase_files
    pf_raw = data.get("phase_files")
    if pf_raw is not None:
        if not isinstance(pf_raw, dict):
            raise ConfigError(f"Config {config_path}: 'phase_files' must be a mapping")
        if "pattern" not in pf_raw:
            raise ConfigError(
                f"Config {config_path}: 'phase_files.pattern' is required"
            )
        cfg.phase_files = PhaseFilesSpec(
            pattern=str(pf_raw["pattern"]),
            number_extract_regex=str(
                pf_raw.get("number_extract_regex", r"^phase-(\d+)-")
            ),
            required=pf_raw.get("required"),
        )

    # required_headers
    rh_raw = data.get("required_headers")
    if rh_raw is not None:
        if not isinstance(rh_raw, list):
            raise ConfigError(
                f"Config {config_path}: 'required_headers' must be a list"
            )
        for idx, item in enumerate(rh_raw):
            if not isinstance(item, dict):
                raise ConfigError(
                    f"Config {config_path}: 'required_headers[{idx}]' must be a mapping"
                )
            if "name" not in item or "type" not in item:
                raise ConfigError(
                    f"Config {config_path}: 'required_headers[{idx}]' "
                    f"missing 'name' or 'type'"
                )
            cfg.required_headers.append(
                HeaderSpec(
                    name=str(item["name"]),
                    type=str(item["type"]),
                    format=item.get("format"),
                    allowed=item.get("allowed"),
                    regex=item.get("regex"),
                )
            )

    # required_sections
    rs_raw = data.get("required_sections")
    if rs_raw is not None:
        if not isinstance(rs_raw, list):
            raise ConfigError(
                f"Config {config_path}: 'required_sections' must be a list"
            )
        cfg.required_sections = [str(s) for s in rs_raw]

    # required_blockquote_labels
    rbl_raw = data.get("required_blockquote_labels")
    if rbl_raw is not None:
        if not isinstance(rbl_raw, list):
            raise ConfigError(
                f"Config {config_path}: 'required_blockquote_labels' must be a list"
            )
        cfg.required_blockquote_labels = [str(s) for s in rbl_raw]

    return cfg


def load_config(config_path: Path) -> PlanConfig:
    """Load and validate a plan config file.

    Raises ``ConfigError`` on any error.
    """
    data = _load_raw_config(config_path)
    return _build_config(data, config_path)


def resolve_config(
    plan_dir: Path, explicit_config: Optional[Path]
) -> Optional[PlanConfig]:
    """Resolve config using loading-order rules.

    Order:
    1. ``explicit_config`` if provided
    2. ``<plan_dir>/plan.config.yaml`` if present
    3. ``None`` — no config, minimal mode

    Raises ``ConfigError`` on parse/version errors.
    """
    if explicit_config is not None:
        return load_config(explicit_config)
    local_config = plan_dir / "plan.config.yaml"
    if local_config.is_file():
        return load_config(local_config)
    return None


# ---------------------------------------------------------------------------
# Pure-logic helpers
# ---------------------------------------------------------------------------


def _is_placeholder(value: str) -> bool:
    """Return True when a string looks like an unfilled template placeholder.

    Placeholder heuristics: contains ``<`` or ``Y`` characters (e.g.
    ``<YYYY-MM-DDTHH:MM>``, ``<fill>``).
    """
    s = str(value).strip()
    return "<" in s or "Y" in s


def _parse_iso_datetime(value: str, fmt: str = "%Y-%m-%dT%H:%M") -> Optional[datetime]:
    """Parse a datetime string per ``fmt``.

    Returns ``None`` when the value is a placeholder or cannot be parsed.
    """
    s = str(value).strip()
    if _is_placeholder(s):
        return None
    try:
        return datetime.strptime(s, fmt)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Header parsing (config-driven)
# ---------------------------------------------------------------------------


def parse_plan_frontmatter(path: Path) -> dict[str, Any]:
    """Read a plan file and return its YAML frontmatter as a dict.

    Raises ``ValueError`` when the file cannot be parsed (no frontmatter,
    unclosed block, not a mapping).  Does NOT enforce required fields — that
    is config-driven.
    """
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    if not lines or lines[0].rstrip("\r\n") != "---":
        raise ValueError(f"No YAML frontmatter block found in {path}")

    closing: Optional[int] = None
    for i, line in enumerate(lines[1:], start=1):
        if line.rstrip("\r\n") == "---":
            closing = i
            break

    if closing is None:
        raise ValueError(f"Unclosed frontmatter in {path}")

    frontmatter_text = "".join(lines[1:closing])
    data = yaml.safe_load(frontmatter_text)

    if not isinstance(data, dict):
        raise ValueError(f"Frontmatter is not a YAML mapping in {path}")

    return data


def _validate_header_value(
    field_name: str, value: Any, spec: HeaderSpec
) -> Optional[str]:
    """Validate a single header field value against its spec.

    Returns a violation string on failure, ``None`` on success.
    """
    raw = str(value).strip() if value is not None else ""

    if spec.type == "string":
        if not raw:
            return f"HEADER-TYPE: {field_name} expected non-empty string, got {value!r}"

    elif spec.type == "int":
        try:
            int(raw.lstrip("0") or "0")
        except ValueError:
            return f"HEADER-TYPE: {field_name} expected int, got {value!r}"

    elif spec.type == "datetime":
        fmt = spec.format or "%Y-%m-%dT%H:%M"
        if not _is_placeholder(raw):
            try:
                datetime.strptime(raw, fmt)
            except ValueError:
                return (
                    f"HEADER-TYPE: {field_name} expected datetime ({fmt}), "
                    f"got {value!r}"
                )

    elif spec.type == "enum":
        allowed = spec.allowed or []
        if raw not in allowed:
            allowed_str = ", ".join(str(a) for a in allowed)
            return (
                f"HEADER-TYPE: {field_name} expected enum ({allowed_str}), "
                f"got {value!r}"
            )

    else:
        # Unknown type — treat as string present check
        if not raw:
            return f"HEADER-TYPE: {field_name} expected non-empty value, got {value!r}"

    # Optional regex check
    if spec.regex and raw:
        if not re.search(spec.regex, raw):
            return (
                f"HEADER-TYPE: {field_name} value {value!r} "
                f"does not match pattern {spec.regex!r}"
            )

    return None


def check_required_headers(
    data: dict[str, Any], specs: list[HeaderSpec]
) -> list[str]:
    """Validate plan frontmatter against all header specs.

    Returns a list of violation strings.
    """
    violations: list[str] = []
    for spec in specs:
        if spec.name not in data:
            violations.append(f"HEADER-MISSING: {spec.name}")
            continue
        violation = _validate_header_value(spec.name, data[spec.name], spec)
        if violation:
            violations.append(violation)
    return violations


# ---------------------------------------------------------------------------
# Phase file helpers
# ---------------------------------------------------------------------------


def _phase_number_from_fname(fname: str, pattern: str = r"^phase-(\d+)-") -> int:
    """Extract phase number from a filename using ``pattern``.

    Returns 99 for filenames that do not match (treated as always-required).
    """
    m = re.match(pattern, fname)
    return int(m.group(1)) if m else 99


def _glob_phase_files(plan_dir: Path, pf_spec: PhaseFilesSpec) -> list[str]:
    """Return filenames of all phase files in ``plan_dir`` matching the glob.

    Returns sorted list of filenames (not full paths).
    """
    return sorted(p.name for p in plan_dir.glob(pf_spec.pattern))


def check_phase_files_exist(
    plan_dir: Path,
    pf_spec: PhaseFilesSpec,
) -> tuple[list[str], list[str]]:
    """Verify required phase files exist in ``plan_dir``.

    Uses file presence to distinguish violations from warnings:
    - Highest-present phase determines the boundary.
    - Absent phases with number <= highest_present → violation (gap).
    - Absent phases with number > highest_present → warning (in-progress).
    - When no required list is configured, returns empty lists (glob-only mode).

    Returns:
        (violations, warnings)
    """
    if not pf_spec.required:
        return [], []

    regex = pf_spec.number_extract_regex

    presence: dict[int, bool] = {}
    for fname in pf_spec.required:
        phase_num = _phase_number_from_fname(fname, regex)
        presence[phase_num] = (plan_dir / fname).is_file()

    highest_present = max(
        (n for n, exists in presence.items() if exists), default=0
    )

    violations: list[str] = []
    warnings: list[str] = []

    for fname in pf_spec.required:
        phase_num = _phase_number_from_fname(fname, regex)
        if presence[phase_num]:
            continue
        if phase_num <= highest_present:
            violations.append(
                f"MISSING-PHASE: {fname} not found in {plan_dir}"
            )
        else:
            warnings.append(
                f"INCOMPLETE-PLAN: {fname} not yet written "
                f"(highest written phase: {highest_present:02d})"
            )

    return violations, warnings


def _check_phase_file_sections(
    fpath: Path,
    fname: str,
    required_sections: list[str],
    required_blockquote_labels: list[str],
) -> list[tuple[str, str]]:
    """Check a single phase file for required headings and blockquote labels.

    Returns a list of ``(filename, missing_item)`` tuples.
    """
    findings: list[tuple[str, str]] = []
    h2_re = re.compile(r"^##\s+(.+)$")
    blockquote_label_re = re.compile(r"^>\s+\*\*(\w[\w\s-]*):\*\*")

    content = fpath.read_text(encoding="utf-8")
    lines = content.splitlines()

    h2_present: set[str] = set()
    labels_present: set[str] = set()

    for line in lines:
        h2_match = h2_re.match(line)
        if h2_match:
            h2_present.add(h2_match.group(1).strip())

        bq_match = blockquote_label_re.match(line)
        if bq_match:
            labels_present.add(bq_match.group(1).strip())

    for section in required_sections:
        if section not in h2_present:
            findings.append((fname, f"## {section}"))

    for label in required_blockquote_labels:
        if label not in labels_present:
            findings.append((fname, f"**{label}:**"))

    return findings


def check_phase_files_have_required_sections(
    plan_dir: Path,
    pf_spec: PhaseFilesSpec,
    required_sections: list[str],
    required_blockquote_labels: list[str],
) -> list[tuple[str, str]]:
    """Verify each present phase file has the required headings and blockquote labels.

    Iterates files matched by ``pf_spec.pattern``. Missing files are silently
    skipped (absence is handled by ``check_phase_files_exist``).

    Returns a list of ``(filename, missing_section)`` tuples.
    """
    if not required_sections and not required_blockquote_labels:
        return []

    findings: list[tuple[str, str]] = []
    matched_files = _glob_phase_files(plan_dir, pf_spec)

    for fname in matched_files:
        fpath = plan_dir / fname
        if not fpath.is_file():
            continue
        findings.extend(
            _check_phase_file_sections(
                fpath, fname, required_sections, required_blockquote_labels
            )
        )

    return findings


def check_single_phase_file_exists(
    plan_dir: Path,
    phase_num: int,
    pf_spec: PhaseFilesSpec,
) -> Optional[str]:
    """Return the filename for phase ``phase_num`` in ``plan_dir``.

    Searches matched files via glob + number extraction regex.
    Returns the matched filename string, or ``None`` when not found.
    """
    regex = pf_spec.number_extract_regex
    for fname in _glob_phase_files(plan_dir, pf_spec):
        if _phase_number_from_fname(fname, regex) == phase_num:
            if (plan_dir / fname).is_file():
                return fname

    # Also check required list for expected name (for clearer error messages)
    if pf_spec.required:
        for fname in pf_spec.required:
            if _phase_number_from_fname(fname, regex) == phase_num:
                if (plan_dir / fname).is_file():
                    return fname

    return None


def _expected_phase_filename(
    phase_num: int, pf_spec: PhaseFilesSpec
) -> str:
    """Return the expected filename for a phase number, for error messages."""
    regex = pf_spec.number_extract_regex
    if pf_spec.required:
        for fname in pf_spec.required:
            if _phase_number_from_fname(fname, regex) == phase_num:
                return fname
    return f"phase-{phase_num:02d}-*.md"


# ---------------------------------------------------------------------------
# Full validation orchestration
# ---------------------------------------------------------------------------


def validate(plan_dir: str, config: Optional[PlanConfig]) -> int:
    """Run all checks on ``plan_dir`` (full-plan mode).

    Prints violations to stderr and warnings to stderr with ``WARN:`` prefix.
    Emits a phase-by-phase status table to stdout on success.
    Returns 0 if all checks pass, 1 if violations found.
    """
    violations: list[str] = []
    warnings: list[str] = []

    base = Path(plan_dir)
    plan_file = config.plan_file if config else "plan.md"
    plan_path = base / plan_file

    # -- Parse frontmatter ------------------------------------------------------
    try:
        data = parse_plan_frontmatter(plan_path)
    except (OSError, ValueError) as exc:
        print(f"HEADER-ERROR: {exc}", file=sys.stderr)
        return 1

    if config is None:
        # Minimal mode: only check the file exists and parses
        print(f"ok  {plan_path} (no config — frontmatter only check)")
        return 0

    # -- Required headers -------------------------------------------------------
    if config.required_headers:
        violations.extend(check_required_headers(data, config.required_headers))

    # -- Phase files exist ------------------------------------------------------
    if config.phase_files is not None:
        phase_violations, phase_warnings = check_phase_files_exist(
            base, config.phase_files
        )
        violations.extend(phase_violations)
        warnings.extend(phase_warnings)

        # -- Phase file sections ------------------------------------------------
        section_findings = check_phase_files_have_required_sections(
            base,
            config.phase_files,
            config.required_sections,
            config.required_blockquote_labels,
        )
        for fname, section in section_findings:
            violations.append(f"MISSING-SECTION: {fname} is missing {section}")

    # -- Report -----------------------------------------------------------------
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)

    if violations:
        for v in violations:
            print(v, file=sys.stderr)
        return 1

    # -- Phase status table (on success) ----------------------------------------
    print(f"\nPlan: {plan_dir}  Status: {data.get('Status', '?')}\n")
    if config.phase_files is not None:
        matched = _glob_phase_files(base, config.phase_files)
        required_set = set(config.phase_files.required or [])
        all_files = sorted(
            set(matched) | required_set,
            key=lambda f: _phase_number_from_fname(
                f, config.phase_files.number_extract_regex
            ),
        )
        print(f"{'Phase file':<35} {'Status'}")
        print("-" * 45)
        for fname in all_files:
            status = "ok" if (base / fname).is_file() else "absent (not yet written)"
            print(f"  {fname:<33} {status}")
        print()

    return 0


def validate_phase(
    plan_dir: str, phase_num: int, config: Optional[PlanConfig]
) -> int:
    """Validate a single phase file in ``plan_dir``.

    Checks:
    - Plan header file can be parsed.
    - The phase file for ``phase_num`` exists.
    - The phase file has all required sections and blockquote labels.

    Returns 0 if all checks pass, 1 if violations found.
    """
    violations: list[str] = []

    base = Path(plan_dir)
    plan_file = config.plan_file if config else "plan.md"
    plan_path = base / plan_file

    # -- Parse frontmatter ------------------------------------------------------
    try:
        data = parse_plan_frontmatter(plan_path)
    except (OSError, ValueError) as exc:
        print(f"HEADER-ERROR: {exc}", file=sys.stderr)
        return 1

    if config is None:
        # Minimal mode: only check frontmatter
        print(f"ok  {plan_path} (no config — frontmatter only check)")
        return 0

    # -- Required headers -------------------------------------------------------
    if config.required_headers:
        violations.extend(check_required_headers(data, config.required_headers))

    # -- Single phase file exists? ----------------------------------------------
    if config.phase_files is not None:
        fname = check_single_phase_file_exists(base, phase_num, config.phase_files)
        if fname is None:
            expected = _expected_phase_filename(phase_num, config.phase_files)
            print(
                f"PHASE-NOT-WRITTEN: phase {phase_num:02d} ({expected}) "
                f"not yet written in {plan_dir}",
                file=sys.stderr,
            )
            return 1

        # -- Phase file sections ------------------------------------------------
        section_findings = _check_phase_file_sections(
            base / fname,
            fname,
            config.required_sections,
            config.required_blockquote_labels,
        )
        for _fname, section in section_findings:
            violations.append(f"MISSING-SECTION: {_fname} is missing {section}")

    # -- Report -----------------------------------------------------------------
    if violations:
        for v in violations:
            print(v, file=sys.stderr)
        return 1

    phase_fname = (
        check_single_phase_file_exists(base, phase_num, config.phase_files)
        if config.phase_files
        else f"phase-{phase_num:02d}-*.md"
    )
    print(f"ok  phase {phase_num:02d} ({phase_fname})  [plan: {plan_dir}]")
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a plan directory against a config-driven schema.\n\n"
            "Default: full validation (all present phases + header checks).\n"
            "With --phase NN: single-phase check (only that phase file + header).\n\n"
            "Config loading order:\n"
            "  1. --config <path> if provided\n"
            "  2. <plan_dir>/plan.config.yaml if present\n"
            "  3. None — only checks plan file exists and parses as YAML frontmatter"
        ),
        epilog="Exit code 0 = pass, 1 = fail.  Warnings do not affect exit code.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "plan_dir",
        help="Path to the plan directory (contains plan.md + phase-NN-*.md files)",
    )
    parser.add_argument(
        "--config",
        metavar="PATH",
        default=None,
        help=(
            "Path to plan.config.yaml. If omitted, looks for "
            "<plan_dir>/plan.config.yaml. If still absent, minimal mode."
        ),
    )
    parser.add_argument(
        "--phase",
        metavar="NN",
        type=int,
        default=None,
        help=(
            "Validate only the specified phase file (e.g. --phase 03 checks "
            "phase-03-*.md + plan header). Exits 1 if the phase file "
            "does not yet exist."
        ),
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Entry point — parses args and dispatches to validate() or validate_phase()."""
    args = _build_parser().parse_args(argv)

    plan_dir = Path(args.plan_dir)
    explicit_config = Path(args.config) if args.config else None

    try:
        config = resolve_config(plan_dir, explicit_config)
    except ConfigError as exc:
        print(f"CONFIG-ERROR: {exc}", file=sys.stderr)
        return 1

    if args.phase is not None:
        return validate_phase(str(plan_dir), args.phase, config)
    else:
        return validate(str(plan_dir), config)


if __name__ == "__main__":
    sys.exit(main())
