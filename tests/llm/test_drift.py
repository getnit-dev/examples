"""LLM: nit drift — LLM output drift monitoring.

Uses Ollama (auto-discovered). Asserts that drift commands complete
without crashing, NOT that drift detection is accurate.
"""

from __future__ import annotations

import pytest

from tests.nit_runner import NitRunner

pytestmark = [pytest.mark.llm]


@pytest.fixture(autouse=True)
def _require_ollama(ollama_available: bool) -> None:
    if not ollama_available:
        pytest.skip("Ollama not available")


class TestDrift:
    """``nit drift`` should run drift tests without crashing."""

    def test_baseline_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        """Creating a baseline should not crash (even with no drift tests)."""
        result = nit_with_ollama.drift_baseline()
        assert result.exit_code in (0, 1), (
            f"drift --baseline crashed (exit={result.exit_code}):\n{result.stderr}"
        )

    def test_drift_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        """Running drift tests should not crash."""
        # Create baseline first, then run drift check
        nit_with_ollama.drift_baseline()
        result = nit_with_ollama.drift()
        assert result.exit_code in (0, 1), (
            f"drift crashed (exit={result.exit_code}):\n{result.stderr}"
        )
