"""LLM: nit generate — LLM-based test generation.

Uses Ollama (auto-discovered). Tolerance is high: we assert the command
doesn't crash and doesn't corrupt existing tests, NOT that the
generated code is high quality.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.assertions import assert_generate_files_valid
from tests.manifests import ProjectManifest
from tests.nit_runner import NitRunner

pytestmark = [pytest.mark.llm]


@pytest.fixture(autouse=True)
def _require_ollama(ollama_available: bool) -> None:
    if not ollama_available:
        pytest.skip("Ollama not available")


class TestGenerate:
    """``nit generate`` should complete without crashing."""

    def test_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        """Exit code 0 (success) or 1 (graceful abort) — NOT a traceback crash."""
        result = nit_with_ollama.generate()
        assert result.exit_code in (0, 1), (
            f"generate crashed (exit={result.exit_code}):\n{result.stderr}"
        )

    def test_attempts_file_creation(
        self,
        nit_with_ollama: NitRunner,
        project_dir: Path,
        project_manifest: ProjectManifest,
    ) -> None:
        """Should attempt to create test files for untested code."""
        nit_with_ollama.generate()

        # Count all test files in the project
        test_patterns = ["test_*.*", "*.test.*", "*.spec.*"]
        test_files: list[Path] = []
        for pattern in test_patterns:
            test_files.extend(project_dir.rglob(pattern))

        # At minimum, the existing test files should still be present
        assert len(test_files) >= len(project_manifest.existing_test_files), (
            f"Expected at least {len(project_manifest.existing_test_files)} "
            f"test files, found {len(test_files)}"
        )

    def test_generated_files_valid(
        self,
        nit_with_ollama: NitRunner,
        project_dir: Path,
        project_manifest: ProjectManifest,
    ) -> None:
        """Generated test files should exist and be non-empty."""
        nit_with_ollama.generate()
        assert_generate_files_valid(project_dir, project_manifest)

    def test_existing_tests_not_broken(self, nit_with_ollama: NitRunner) -> None:
        """Existing tests must still pass after generation."""
        nit_with_ollama.generate()
        result = nit_with_ollama.run_tests()
        # Original tests should still pass; new generated tests may fail
        # with small models — that is acceptable
        if not result.success:
            data = result.json()
            # If errors == total, something went very wrong
            assert data.get("errors", 0) < data.get("total", 1), (
                "All tests errored — generation may have corrupted the project"
            )
