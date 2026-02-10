"""Heuristics: nit run — test execution tests."""

from __future__ import annotations

import pytest

from tests.assertions import assert_run_structure_complete, assert_run_tests_pass
from tests.manifests import ProjectManifest
from tests.nit_runner import NitRunner

pytestmark = pytest.mark.heuristics


class TestRun:
    """``nit run`` should execute the project's test suite via the adapter."""

    def test_exits_zero(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.run_tests()
        assert result.success, f"nit run failed:\n{result.stderr}"

    def test_json_structure(self, nit: NitRunner) -> None:
        """CI-mode JSON output has the expected keys."""
        nit.init()
        result = nit.run_tests()
        data = result.json()
        for key in ("success", "total", "passed", "failed", "skipped", "errors", "duration_ms"):
            assert key in data, f"Missing key {key!r} in run output"

    def test_run_structure_complete(self, nit: NitRunner) -> None:
        """Run output has valid structural invariants."""
        nit.init()
        result = nit.run_tests()
        data = result.json()
        assert_run_structure_complete(data)

    def test_all_existing_tests_pass(
        self,
        nit: NitRunner,
        project_manifest: ProjectManifest,
    ) -> None:
        nit.init()
        result = nit.run_tests()
        assert_run_tests_pass(result, project_manifest)

    def test_test_count_meets_minimum(
        self,
        nit: NitRunner,
        project_manifest: ProjectManifest,
    ) -> None:
        nit.init()
        result = nit.run_tests()
        data = result.json()
        assert data["total"] >= project_manifest.expected_test_count_min
