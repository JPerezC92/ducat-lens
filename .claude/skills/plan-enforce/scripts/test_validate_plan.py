"""
Pytest suite for validate_plan.py (config-driven, project-agnostic).

Test classes:
    TestConfigLoading           — load plan example config, no config,
                                  malformed YAML, unsupported version
    TestHeaderValidation        — int / datetime / enum / string type checks
    TestPhaseFiles              — required-list violations, highest-present logic,
                                  glob-only mode
    TestSections                — missing ## heading, missing blockquote label,
                                  all sections present
    TestIntegrationFixtures     — end-to-end on fixtures/plan-valid with example config
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

import pytest
import yaml

# ---------------------------------------------------------------------------
# Import the module under test
# ---------------------------------------------------------------------------
import validate_plan as vp

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SCRIPTS_DIR = Path(__file__).parent
_REFERENCES_DIR = _SCRIPTS_DIR.parent / "references"
_PLAN_CONFIG = _REFERENCES_DIR / "example-config-plan.yaml"
_FIXTURES_DIR = _SCRIPTS_DIR / "fixtures"
_PLAN_FIXTURE = _FIXTURES_DIR / "plan-valid"


def _write_plan(tmp_path: Path, frontmatter: dict[str, Any], body: str = "") -> Path:
    """Write a plan.md with YAML frontmatter to tmp_path."""
    fpath = tmp_path / "plan.md"
    fm_text = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    fpath.write_text(f"---\n{fm_text}---\n\n{body}", encoding="utf-8")
    return fpath


def _write_phase(tmp_path: Path, fname: str, content: str) -> Path:
    fpath = tmp_path / fname
    fpath.write_text(content, encoding="utf-8")
    return fpath


def _full_phase_content(
    extra_sections: str = "",
) -> str:
    """Generate a phase file body with all 8 required ## sections."""
    return textwrap.dedent(
        f"""\
        # Phase NN — Test

        ## Owner

        Test agent

        ## Pre

        - Pre condition holds.

        ## Reads

        - `file.md` — reason

        ## Writes

        - `output.txt` — result

        ## Steps

        1. Do a thing.

        ## Output

        - `output.txt` — something useful

        ## Gate

        - Check passes.

        ## Abort conditions

        - Stop if bad.

        {extra_sections}
        """
    )


_VALID_PLAN_FM: dict[str, Any] = {
    "Status": "active",
    "Started": "2026-01-15 09:00",
    "Subject": "Test plan subject",
    "Layout": "subfolder pattern",
}


# ===========================================================================
# TestConfigLoading
# ===========================================================================


class TestConfigLoading:
    """Config file loading: happy paths, malformed YAML, unsupported version."""

    def test_load_plan_config(self) -> None:
        """Plan example config loads without error and has expected fields."""
        cfg = vp.load_config(_PLAN_CONFIG)
        assert cfg.version == "1.0"
        assert cfg.plan_file == "plan.md"
        assert cfg.phase_files is not None
        assert len(cfg.required_headers) == 4
        assert len(cfg.required_sections) == 8
        assert cfg.required_blockquote_labels == []

    def test_no_config_returns_none(self, tmp_path: Path) -> None:
        """resolve_config returns None when no config is found."""
        cfg = vp.resolve_config(tmp_path, explicit_config=None)
        assert cfg is None

    def test_malformed_yaml_raises_config_error(self, tmp_path: Path) -> None:
        """Malformed YAML config raises ConfigError."""
        bad = tmp_path / "plan.config.yaml"
        bad.write_text("version: [\nbroken yaml", encoding="utf-8")
        with pytest.raises(vp.ConfigError, match="Malformed YAML"):
            vp.load_config(bad)

    def test_unsupported_version_raises_config_error(self, tmp_path: Path) -> None:
        """Unsupported schema version raises ConfigError."""
        cfg_file = tmp_path / "plan.config.yaml"
        cfg_file.write_text("version: '99.0'\n", encoding="utf-8")
        with pytest.raises(vp.ConfigError, match="unsupported version"):
            vp.load_config(cfg_file)

    def test_local_config_auto_discovered(self, tmp_path: Path) -> None:
        """resolve_config discovers plan.config.yaml inside plan_dir."""
        cfg_file = tmp_path / "plan.config.yaml"
        cfg_file.write_text("version: '1.0'\n", encoding="utf-8")
        cfg = vp.resolve_config(tmp_path, explicit_config=None)
        assert cfg is not None
        assert cfg.version == "1.0"

    def test_explicit_config_overrides_local(self, tmp_path: Path) -> None:
        """Explicit --config path overrides local plan.config.yaml."""
        local = tmp_path / "plan.config.yaml"
        local.write_text("version: '1.0'\nplan_file: local.md\n", encoding="utf-8")
        explicit = tmp_path / "explicit.yaml"
        explicit.write_text("version: '1.0'\nplan_file: explicit.md\n", encoding="utf-8")
        cfg = vp.resolve_config(tmp_path, explicit_config=explicit)
        assert cfg is not None
        assert cfg.plan_file == "explicit.md"


# ===========================================================================
# TestHeaderValidation
# ===========================================================================


class TestHeaderValidation:
    """Header field type validation: valid and invalid samples per type."""

    def _spec(self, name: str, htype: str, **kwargs: Any) -> vp.HeaderSpec:
        return vp.HeaderSpec(name=name, type=htype, **kwargs)

    def test_int_valid(self) -> None:
        violations = vp.check_required_headers(
            {"Phase": 3}, [self._spec("Phase", "int")]
        )
        assert violations == []

    def test_int_invalid(self) -> None:
        violations = vp.check_required_headers(
            {"Phase": "not-an-int"}, [self._spec("Phase", "int")]
        )
        assert any("HEADER-TYPE" in v and "Phase" in v for v in violations)

    def test_datetime_valid(self) -> None:
        violations = vp.check_required_headers(
            {"Updated": "2026-05-24T10:30"},
            [self._spec("Updated", "datetime", format="%Y-%m-%dT%H:%M")],
        )
        assert violations == []

    def test_datetime_invalid(self) -> None:
        violations = vp.check_required_headers(
            {"Updated": "not-a-date"},
            [self._spec("Updated", "datetime", format="%Y-%m-%dT%H:%M")],
        )
        assert any("HEADER-TYPE" in v and "Updated" in v for v in violations)

    def test_datetime_placeholder_skipped(self) -> None:
        """Placeholder values (containing < or Y) skip datetime parse."""
        violations = vp.check_required_headers(
            {"Updated": "<YYYY-MM-DDTHH:MM>"},
            [self._spec("Updated", "datetime", format="%Y-%m-%dT%H:%M")],
        )
        assert violations == []

    def test_enum_valid(self) -> None:
        violations = vp.check_required_headers(
            {"Status": "active"},
            [self._spec("Status", "enum", allowed=["active", "completed", "draft"])],
        )
        assert violations == []

    def test_enum_invalid(self) -> None:
        violations = vp.check_required_headers(
            {"Status": "unknown"},
            [self._spec("Status", "enum", allowed=["active", "completed", "draft"])],
        )
        assert any("HEADER-TYPE" in v and "Status" in v for v in violations)

    def test_enum_layout_valid(self) -> None:
        """Layout enum field accepts 'subfolder pattern'."""
        violations = vp.check_required_headers(
            {"Layout": "subfolder pattern"},
            [self._spec("Layout", "enum", allowed=["single-file", "subfolder pattern"])],
        )
        assert violations == []

    def test_enum_layout_invalid(self) -> None:
        """Layout enum rejects values not in allowed list."""
        violations = vp.check_required_headers(
            {"Layout": "monolith"},
            [self._spec("Layout", "enum", allowed=["single-file", "subfolder pattern"])],
        )
        assert any("HEADER-TYPE" in v and "Layout" in v for v in violations)

    def test_missing_field_produces_header_missing(self) -> None:
        violations = vp.check_required_headers(
            {}, [self._spec("Status", "enum", allowed=["active"])]
        )
        assert any("HEADER-MISSING" in v and "Status" in v for v in violations)

    def test_string_valid(self) -> None:
        violations = vp.check_required_headers(
            {"Subject": "My plan"}, [self._spec("Subject", "string")]
        )
        assert violations == []

    def test_string_empty_invalid(self) -> None:
        violations = vp.check_required_headers(
            {"Subject": ""}, [self._spec("Subject", "string")]
        )
        assert any("HEADER-TYPE" in v and "Subject" in v for v in violations)


# ===========================================================================
# TestPhaseFiles
# ===========================================================================


class TestPhaseFiles:
    """Phase file presence: required-list violations, highest-present logic, glob-only."""

    def _pf_spec(
        self, required: list[str] | None = None, pattern: str = "phase-*.md"
    ) -> vp.PhaseFilesSpec:
        return vp.PhaseFilesSpec(pattern=pattern, required=required)

    def test_all_required_present(self, tmp_path: Path) -> None:
        (tmp_path / "phase-01-forge.md").write_text("x", encoding="utf-8")
        (tmp_path / "phase-02-cipher.md").write_text("x", encoding="utf-8")
        spec = self._pf_spec(["phase-01-forge.md", "phase-02-cipher.md"])
        violations, warnings = vp.check_phase_files_exist(tmp_path, spec)
        assert violations == []
        assert warnings == []

    def test_gap_in_sequence_is_violation(self, tmp_path: Path) -> None:
        """Missing phase-01 while phase-02 exists is a violation (gap)."""
        (tmp_path / "phase-02-cipher.md").write_text("x", encoding="utf-8")
        spec = self._pf_spec(["phase-01-forge.md", "phase-02-cipher.md"])
        violations, warnings = vp.check_phase_files_exist(tmp_path, spec)
        assert any("MISSING-PHASE" in v and "phase-01" in v for v in violations)
        assert warnings == []

    def test_future_phase_is_warning(self, tmp_path: Path) -> None:
        """Phase with number > highest_present produces a warning, not violation."""
        (tmp_path / "phase-01-forge.md").write_text("x", encoding="utf-8")
        spec = self._pf_spec(["phase-01-forge.md", "phase-02-cipher.md"])
        violations, warnings = vp.check_phase_files_exist(tmp_path, spec)
        assert violations == []
        assert any("INCOMPLETE-PLAN" in w and "phase-02" in w for w in warnings)

    def test_no_files_all_warning(self, tmp_path: Path) -> None:
        """When no phase files exist at all, highest_present=0, all are warnings
        (not yet written — plan not started). The gap-detection violation logic
        fires only when a higher phase is present while a lower one is missing."""
        spec = self._pf_spec(["phase-01-forge.md", "phase-02-cipher.md"])
        violations, warnings = vp.check_phase_files_exist(tmp_path, spec)
        assert violations == []
        assert len(warnings) == 2

    def test_glob_only_mode_no_violations(self, tmp_path: Path) -> None:
        """When required list is absent, check_phase_files_exist returns empty lists."""
        (tmp_path / "phase-01-anything.md").write_text("x", encoding="utf-8")
        spec = self._pf_spec(required=None)
        violations, warnings = vp.check_phase_files_exist(tmp_path, spec)
        assert violations == []
        assert warnings == []


# ===========================================================================
# TestSections
# ===========================================================================


class TestSections:
    """Phase file structure: required ## headings and blockquote labels."""

    _REQUIRED_SECTIONS = [
        "Owner", "Pre", "Reads", "Writes",
        "Steps", "Output", "Gate", "Abort conditions",
    ]

    def test_all_sections_present(self, tmp_path: Path) -> None:
        content = _full_phase_content()
        _write_phase(tmp_path, "phase-01-forge.md", content)
        pf_spec = vp.PhaseFilesSpec(pattern="phase-*.md")
        findings = vp.check_phase_files_have_required_sections(
            tmp_path,
            pf_spec,
            self._REQUIRED_SECTIONS,
            [],
        )
        assert findings == []

    def test_missing_h2_section(self, tmp_path: Path) -> None:
        # Remove "## Gate" from content
        content = _full_phase_content().replace("## Gate\n\n- Check passes.\n\n", "")
        _write_phase(tmp_path, "phase-01-forge.md", content)
        pf_spec = vp.PhaseFilesSpec(pattern="phase-*.md")
        findings = vp.check_phase_files_have_required_sections(
            tmp_path,
            pf_spec,
            self._REQUIRED_SECTIONS,
            [],
        )
        assert any("Gate" in item for _, item in findings)

    def test_missing_blockquote_label(self, tmp_path: Path) -> None:
        # Phase file with blockquote labels — one is missing
        content = textwrap.dedent(
            """\
            > **Owner:** Test agent

            > **Pre:** Pre condition.

            ## Steps

            1. Do a thing.

            ## Output

            Something useful.
            """
        )
        _write_phase(tmp_path, "phase-01-forge.md", content)
        pf_spec = vp.PhaseFilesSpec(pattern="phase-*.md")
        findings = vp.check_phase_files_have_required_sections(
            tmp_path,
            pf_spec,
            [],
            ["Owner", "Pre", "Reads"],
        )
        assert any("Reads" in item for _, item in findings)

    def test_absent_file_silently_skipped(self, tmp_path: Path) -> None:
        """Files in required list that are absent do not produce section findings."""
        pf_spec = vp.PhaseFilesSpec(
            pattern="phase-*.md", required=["phase-01-forge.md"]
        )
        findings = vp.check_phase_files_have_required_sections(
            tmp_path,
            pf_spec,
            ["Steps"],
            [],
        )
        assert findings == []

    def test_empty_required_lists_no_findings(self, tmp_path: Path) -> None:
        _write_phase(tmp_path, "phase-01-forge.md", "# anything")
        pf_spec = vp.PhaseFilesSpec(pattern="phase-*.md")
        findings = vp.check_phase_files_have_required_sections(
            tmp_path, pf_spec, [], []
        )
        assert findings == []


# ===========================================================================
# TestIntegrationFixtures
# ===========================================================================


class TestIntegrationFixtures:
    """End-to-end integration: run validator subprocess on fixture directories."""

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        script = str(_SCRIPTS_DIR / "validate_plan.py")
        return subprocess.run(
            [sys.executable, script] + args,
            capture_output=True,
            text=True,
            cwd=str(_SCRIPTS_DIR),
        )

    def test_plan_fixture_exits_zero(self) -> None:
        """plan-valid fixture passes with plan config."""
        result = self._run(
            [
                str(_PLAN_FIXTURE),
                "--config",
                str(_PLAN_CONFIG),
            ]
        )
        assert result.returncode == 0, (
            f"Expected exit 0 but got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )

    def test_no_config_exits_zero(self, tmp_path: Path) -> None:
        """No config mode: plan.md exists and parses → exit 0."""
        _write_plan(tmp_path, {"Status": "active", "Subject": "test"})
        result = self._run([str(tmp_path)])
        assert result.returncode == 0, (
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )

    def test_missing_plan_exits_one(self, tmp_path: Path) -> None:
        """No plan.md in dir → exit 1 with HEADER-ERROR."""
        result = self._run([str(tmp_path)])
        assert result.returncode == 1
        assert "HEADER-ERROR" in result.stderr

    def test_missing_header_exits_one(self, tmp_path: Path) -> None:
        """Plan missing required header field exits 1 with HEADER-MISSING."""
        fm = dict(_VALID_PLAN_FM)
        del fm["Status"]
        _write_plan(tmp_path, fm)
        result = self._run(
            [str(tmp_path), "--config", str(_PLAN_CONFIG)]
        )
        assert result.returncode == 1
        assert "HEADER-MISSING" in result.stderr

    def test_invalid_status_enum_exits_one(self, tmp_path: Path) -> None:
        """Plan with Status not in allowed enum exits 1 with HEADER-TYPE."""
        fm = dict(_VALID_PLAN_FM)
        fm["Status"] = "running"
        _write_plan(tmp_path, fm)
        result = self._run(
            [str(tmp_path), "--config", str(_PLAN_CONFIG)]
        )
        assert result.returncode == 1
        assert "HEADER-TYPE" in result.stderr

    def test_config_error_exits_one(self, tmp_path: Path) -> None:
        """Malformed config file exits 1 with CONFIG-ERROR."""
        bad_config = tmp_path / "bad.yaml"
        bad_config.write_text("version: [\nbroken", encoding="utf-8")
        _write_plan(tmp_path, {"Status": "active", "Subject": "test"})
        result = self._run([str(tmp_path), "--config", str(bad_config)])
        assert result.returncode == 1
        assert "CONFIG-ERROR" in result.stderr

    def test_phase_flag_valid_phase_exits_zero(self, tmp_path: Path) -> None:
        """--phase 01 on a directory with a valid phase-01 file exits 0."""
        _write_plan(tmp_path, _VALID_PLAN_FM)
        _write_phase(tmp_path, "phase-01-forge.md", _full_phase_content())
        result = self._run(
            [str(tmp_path), "--config", str(_PLAN_CONFIG), "--phase", "1"]
        )
        assert result.returncode == 0, (
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )

    def test_phase_flag_missing_phase_exits_one(self, tmp_path: Path) -> None:
        """--phase 05 when phase-05 file is absent exits 1 with PHASE-NOT-WRITTEN."""
        _write_plan(tmp_path, _VALID_PLAN_FM)
        result = self._run(
            [str(tmp_path), "--config", str(_PLAN_CONFIG), "--phase", "5"]
        )
        assert result.returncode == 1
        assert "PHASE-NOT-WRITTEN" in result.stderr
