"""Reusable assertion helpers for nit integration tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tests.manifests import ProjectManifest
from tests.nit_runner import NitResult


def assert_json_parseable(result: NitResult) -> dict[str, Any]:
    """Assert stdout is valid JSON and return parsed data."""
    data = result.json()
    assert isinstance(data, dict), f"Expected dict, got {type(data)}"
    return data


# ---------------------------------------------------------------------------
# Scan assertions
# ---------------------------------------------------------------------------


def assert_scan_detects_language(
    scan_data: dict[str, Any],
    manifest: ProjectManifest,
) -> None:
    """Assert scan output includes the expected primary language."""
    detected = scan_data.get("primary_language", "")
    assert detected == manifest.primary_language, (
        f"Expected primary_language={manifest.primary_language!r}, "
        f"got {detected!r}"
    )


def assert_scan_detects_frameworks(
    scan_data: dict[str, Any],
    manifest: ProjectManifest,
) -> None:
    """Assert scan output includes expected framework names."""
    frameworks = scan_data.get("frameworks", [])
    detected_names = [fw.get("name", "") for fw in frameworks]
    for expected in manifest.expected_framework_names:
        assert expected in detected_names, (
            f"Expected framework {expected!r} not found. "
            f"Detected: {detected_names}"
        )


def assert_scan_structure_complete(scan_data: dict[str, Any]) -> None:
    """Assert scan output has all expected top-level keys with valid types."""
    assert scan_data.get("root"), "scan missing or empty 'root'"
    assert scan_data.get("primary_language"), (
        "scan missing or empty 'primary_language'"
    )
    assert "workspace_tool" in scan_data, "scan missing 'workspace_tool'"
    assert isinstance(scan_data.get("languages"), list), (
        "scan 'languages' is not a list"
    )
    assert isinstance(scan_data.get("frameworks"), list), (
        "scan 'frameworks' is not a list"
    )
    assert "packages" in scan_data, "scan missing 'packages'"


def assert_scan_languages_complete(
    scan_data: dict[str, Any],
    manifest: ProjectManifest,
) -> None:
    """Assert languages list has valid entries matching the manifest."""
    languages = scan_data.get("languages", [])
    assert len(languages) > 0, "scan returned empty languages list"

    detected_lang_names: list[str] = []
    for lang in languages:
        assert "language" in lang, f"Language entry missing 'language' key: {lang}"
        assert lang.get("file_count", 0) > 0, (
            f"Language {lang.get('language')} has file_count=0"
        )
        assert lang.get("confidence", 0) > 0, (
            f"Language {lang.get('language')} has confidence=0"
        )
        detected_lang_names.append(lang["language"].lower())

    for expected in manifest.expected_languages:
        assert expected.lower() in detected_lang_names, (
            f"Expected language {expected!r} not in detected: {detected_lang_names}"
        )


def assert_scan_frameworks_detailed(
    scan_data: dict[str, Any],
    manifest: ProjectManifest,
) -> None:
    """Assert framework entries have name, language, category, and confidence."""
    frameworks = scan_data.get("frameworks", [])
    for fw in frameworks:
        assert "name" in fw, f"Framework entry missing 'name': {fw}"
        assert "language" in fw, f"Framework {fw.get('name')} missing 'language'"
        assert "category" in fw, f"Framework {fw.get('name')} missing 'category'"
        assert "confidence" in fw, f"Framework {fw.get('name')} missing 'confidence'"

    detected_names = [fw["name"] for fw in frameworks]
    for expected in manifest.expected_framework_names:
        assert expected in detected_names, (
            f"Expected framework {expected!r} not in {detected_names}"
        )


# ---------------------------------------------------------------------------
# Run assertions
# ---------------------------------------------------------------------------


def assert_run_tests_pass(
    result: NitResult,
    manifest: ProjectManifest,
) -> None:
    """Assert nit run succeeded and test counts meet expectations."""
    assert result.success, f"nit run failed: {result.stderr}"
    data = result.json()
    assert data["total"] >= manifest.expected_test_count_min, (
        f"Expected >= {manifest.expected_test_count_min} tests, "
        f"got {data['total']}"
    )
    if manifest.expected_all_pass:
        assert data["success"] is True, f"Tests failed: {data.get('failed_tests', [])}"
        assert data["failed"] == 0


def assert_run_structure_complete(run_data: dict[str, Any]) -> None:
    """Assert run output has valid structural invariants."""
    assert isinstance(run_data.get("failed_tests"), list), (
        "'failed_tests' should be a list"
    )
    assert "duration_ms" in run_data, "run output missing 'duration_ms'"
    assert run_data["duration_ms"] >= 0, (
        f"duration_ms should be >= 0, got {run_data['duration_ms']}"
    )

    total = run_data.get("total", 0)
    parts = (
        run_data.get("passed", 0)
        + run_data.get("failed", 0)
        + run_data.get("skipped", 0)
        + run_data.get("errors", 0)
    )
    assert parts == total, (
        f"passed({run_data.get('passed')}) + failed({run_data.get('failed')}) "
        f"+ skipped({run_data.get('skipped')}) + errors({run_data.get('errors')}) "
        f"= {parts}, but total = {total}"
    )


# ---------------------------------------------------------------------------
# Config assertions
# ---------------------------------------------------------------------------


def assert_config_project_section(config_data: dict[str, Any]) -> None:
    """Assert project section has required fields."""
    project = config_data.get("project", {})
    assert isinstance(project, dict), "'project' section is not a dict"
    assert "root" in project, "project section missing 'root'"


def assert_config_llm_section(config_data: dict[str, Any]) -> None:
    """Assert llm section has required fields."""
    llm = config_data.get("llm", {})
    assert isinstance(llm, dict), "'llm' section is not a dict"
    assert "mode" in llm, "llm section missing 'mode'"
    assert "provider" in llm, "llm section missing 'provider'"
    assert "model" in llm, "llm section missing 'model'"


# ---------------------------------------------------------------------------
# Analyze assertions
# ---------------------------------------------------------------------------


def assert_analyze_structure(analyze_data: dict[str, Any]) -> None:
    """Assert analyze output has valid structure when successful."""
    assert "bugs_found" in analyze_data, "analyze missing 'bugs_found'"
    assert analyze_data["bugs_found"] >= 0, (
        f"bugs_found should be >= 0, got {analyze_data['bugs_found']}"
    )

    coverage = analyze_data.get("coverage")
    if coverage is not None:
        assert isinstance(coverage, dict), "'coverage' should be a dict"
        for key in ("overall_line", "overall_function"):
            if key in coverage:
                val = coverage[key]
                assert isinstance(val, (int, float)), (
                    f"coverage.{key} should be numeric, got {type(val)}"
                )

    gap_report = analyze_data.get("gap_report")
    if gap_report is not None and isinstance(gap_report, dict):
        if "function_gaps" in gap_report:
            assert isinstance(gap_report["function_gaps"], list), (
                "gap_report.function_gaps should be a list"
            )


# ---------------------------------------------------------------------------
# Generate assertions
# ---------------------------------------------------------------------------


def assert_generate_files_valid(
    project_dir: Path,
    manifest: ProjectManifest,
) -> None:
    """Assert generated test files exist and are non-empty."""
    test_patterns = ["test_*.*", "*.test.*", "*.spec.*"]
    test_files: list[Path] = []
    for pattern in test_patterns:
        test_files.extend(project_dir.rglob(pattern))

    # At minimum, the existing test files should still be present
    assert len(test_files) >= len(manifest.existing_test_files), (
        f"Expected at least {len(manifest.existing_test_files)} "
        f"test files, found {len(test_files)}"
    )

    # Any newly created test files should be non-empty
    for f in test_files:
        if f.is_file():
            assert f.stat().st_size > 0, f"Generated test file is empty: {f}"


# ---------------------------------------------------------------------------
# Changelog assertions
# ---------------------------------------------------------------------------


def assert_changelog_output(text: str) -> None:
    """Assert changelog text is non-empty markdown with headings."""
    assert len(text.strip()) > 0, "Changelog output is empty"
    assert "#" in text, "Changelog output missing markdown headings"


# ---------------------------------------------------------------------------
# Drift assertions
# ---------------------------------------------------------------------------


def assert_drift_report_structure(drift_data: dict[str, Any]) -> None:
    """Assert drift report has expected top-level keys."""
    assert "total_tests" in drift_data, "drift report missing 'total_tests'"
    assert "passed_tests" in drift_data, "drift report missing 'passed_tests'"
    assert "drift_detected" in drift_data, "drift report missing 'drift_detected'"
    assert drift_data["total_tests"] >= 0
