"""Heuristics: nit report — HTML dashboard generation."""

from __future__ import annotations

import pytest

from tests.nit_runner import NitRunner

pytestmark = pytest.mark.heuristics


class TestReport:
    """``nit report --html`` should generate a dashboard without crashing."""

    def test_report_html_does_not_crash(self, nit: NitRunner) -> None:
        nit.init()
        nit.run_tests()
        result = nit.report_html()
        assert result.exit_code in (0, 1), (
            f"report --html crashed (exit={result.exit_code}):\n{result.stderr}"
        )
