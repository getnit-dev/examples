"""LLM: nit analyze — LLM-based analysis.

Asserts that the analyze command produces structured output
without crashing. Does NOT assert on analysis quality.
"""

from __future__ import annotations

import pytest

from tests.assertions import assert_analyze_structure
from tests.nit_runner import NitRunner

pytestmark = [pytest.mark.llm]


@pytest.fixture(autouse=True)
def _require_ollama(ollama_available: bool) -> None:
    if not ollama_available:
        pytest.skip("Ollama not available")


class TestAnalyze:
    """``nit analyze`` should produce structured JSON output."""

    def test_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        result = nit_with_ollama.analyze(json_output=True)
        assert result.exit_code in (0, 1), (
            f"analyze crashed (exit={result.exit_code}):\n{result.stderr}"
        )

    def test_json_structure(self, nit_with_ollama: NitRunner) -> None:
        """JSON output should have expected top-level keys."""
        result = nit_with_ollama.analyze(json_output=True)
        if result.success:
            data = result.json()
            assert isinstance(data, dict)
            # At minimum, should have test run info
            expected_keys = {"bugs_found", "tests_run", "tests_passed"}
            present = expected_keys & set(data.keys())
            assert len(present) > 0, (
                f"None of {expected_keys} found in analyze output. "
                f"Keys: {list(data.keys())}"
            )
            assert_analyze_structure(data)
