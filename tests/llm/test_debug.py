"""LLM: nit debug — bug fix generation.

Uses Ollama (auto-discovered). Asserts that debug commands complete
without crashing, NOT that fixes are correct.
"""

from __future__ import annotations

import pytest

from tests.nit_runner import NitRunner

pytestmark = [pytest.mark.llm]


@pytest.fixture(autouse=True)
def _require_ollama(ollama_available: bool) -> None:
    if not ollama_available:
        pytest.skip("Ollama not available")


class TestDebug:
    """``nit debug`` should attempt to fix bugs without crashing."""

    def test_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        result = nit_with_ollama.debug(dry_run=True)
        assert result.exit_code in (0, 1), (
            f"debug --dry-run crashed (exit={result.exit_code}):\n{result.stderr}"
        )
