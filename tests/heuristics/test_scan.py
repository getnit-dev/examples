"""Heuristics: nit scan — language/framework detection tests."""

from __future__ import annotations

import pytest

from tests.assertions import (
    assert_json_parseable,
    assert_scan_detects_frameworks,
    assert_scan_detects_language,
    assert_scan_frameworks_detailed,
    assert_scan_languages_complete,
    assert_scan_structure_complete,
)
from tests.manifests import ProjectManifest
from tests.nit_runner import NitRunner

pytestmark = pytest.mark.heuristics


class TestScan:
    """``nit scan`` should detect the project stack correctly."""

    def test_json_parseable(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.scan(json_output=True, force=True)
        assert result.success, f"scan failed:\n{result.stderr}"
        assert_json_parseable(result)

    def test_detects_primary_language(
        self,
        nit: NitRunner,
        project_manifest: ProjectManifest,
    ) -> None:
        nit.init()
        result = nit.scan(json_output=True, force=True)
        data = result.json()
        assert_scan_detects_language(data, project_manifest)

    def test_detects_framework(
        self,
        nit: NitRunner,
        project_manifest: ProjectManifest,
    ) -> None:
        nit.init()
        result = nit.scan(json_output=True, force=True)
        data = result.json()
        assert_scan_detects_frameworks(data, project_manifest)

    def test_scan_structure_complete(self, nit: NitRunner) -> None:
        """Scan output has all expected top-level keys."""
        nit.init()
        result = nit.scan(json_output=True, force=True)
        data = result.json()
        assert_scan_structure_complete(data)

    def test_languages_list(
        self,
        nit: NitRunner,
        project_manifest: ProjectManifest,
    ) -> None:
        """Languages list has valid entries matching manifest."""
        nit.init()
        result = nit.scan(json_output=True, force=True)
        data = result.json()
        assert_scan_languages_complete(data, project_manifest)

    def test_frameworks_detailed(
        self,
        nit: NitRunner,
        project_manifest: ProjectManifest,
    ) -> None:
        """Framework entries have name, language, category, confidence."""
        nit.init()
        result = nit.scan(json_output=True, force=True)
        data = result.json()
        assert_scan_frameworks_detailed(data, project_manifest)

    def test_force_rescan(self, nit: NitRunner) -> None:
        """--force should re-scan even when cached."""
        nit.init()
        r1 = nit.scan(force=True)
        r2 = nit.scan(force=True)
        assert r1.success
        assert r2.success

    def test_cached_scan(self, nit: NitRunner) -> None:
        """Second scan without --force should use the cache."""
        nit.init()
        nit.scan(force=True)
        result = nit.scan(force=False)
        assert result.success
