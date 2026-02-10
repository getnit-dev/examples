"""LLM: nit pick — full pipeline (scan -> run -> analyze -> fix -> report).

The most comprehensive LLM-dependent test. Asserts that the
entire pipeline completes without crashing.
"""

from __future__ import annotations

import pytest

from tests.nit_runner import NitRunner

pytestmark = [pytest.mark.llm]


@pytest.fixture(autouse=True)
def _require_ollama(ollama_available: bool) -> None:
    if not ollama_available:
        pytest.skip("Ollama not available")


class TestPick:
    """``nit pick`` should run the full pipeline without crashing."""

    def test_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        result = nit_with_ollama.pick(test_type="unit")
        assert result.exit_code in (0, 1), (
            f"pick crashed (exit={result.exit_code}):\n{result.stderr}"
        )

    def test_existing_tests_survive(self, nit_with_ollama: NitRunner) -> None:
        """After pick, existing tests should still be runnable."""
        nit_with_ollama.pick(test_type="unit")
        result = nit_with_ollama.run_tests()
        # Same tolerance as generate: existing tests shouldn't be wiped out
        if not result.success:
            data = result.json()
            assert data.get("total", 0) > 0, (
                "No tests found after pick — project may be corrupted"
            )
