"""Heuristics: nit watch — scheduled test execution."""

from __future__ import annotations

import pytest

from tests.nit_runner import NitRunner

pytestmark = pytest.mark.heuristics


class TestWatch:
    """``nit watch --max-runs 1`` should execute one run and exit."""

    def test_single_run(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.watch(max_runs=1, interval=1)
        assert result.exit_code in (0, 1), (
            f"watch crashed (exit={result.exit_code}):\n{result.stderr}"
        )
