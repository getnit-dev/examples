"""Heuristics: nit memory — memory management tests."""

from __future__ import annotations

import pytest

from tests.nit_runner import NitRunner

pytestmark = pytest.mark.heuristics


class TestMemoryShow:
    """``nit memory show`` should return memory contents."""

    def test_json_output(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.memory_show(json_output=True)
        assert result.success, f"memory show failed:\n{result.stderr}"
        data = result.json()
        assert isinstance(data, dict)


class TestMemoryReset:
    """``nit memory reset`` should clear memory."""

    def test_reset_succeeds(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.memory_reset()
        assert result.success, f"memory reset failed:\n{result.stderr}"


class TestMemoryExport:
    """``nit memory export`` should output markdown."""

    def test_export_produces_output(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.memory_export()
        assert result.success, f"memory export failed:\n{result.stderr}"
        # Export should produce some text output
        assert len(result.stdout.strip()) > 0
