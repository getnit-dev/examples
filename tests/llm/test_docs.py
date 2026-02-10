"""LLM: nit docs — docstring generation, README, and check.

Uses Ollama (auto-discovered). Tolerance is high: we assert the commands
don't crash and produce output, NOT that the content is high quality.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.manifests import ProjectManifest
from tests.nit_runner import NitRunner

pytestmark = [pytest.mark.llm]


@pytest.fixture(autouse=True)
def _require_ollama(ollama_available: bool) -> None:
    if not ollama_available:
        pytest.skip("Ollama not available")


class TestDocsGenerate:
    """``nit docs --all`` should generate docstrings without crashing."""

    def test_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        result = nit_with_ollama.docs_generate()
        assert result.exit_code in (0, 1), (
            f"docs --all crashed (exit={result.exit_code}):\n{result.stderr}"
        )

    def test_produces_output(self, nit_with_ollama: NitRunner) -> None:
        result = nit_with_ollama.docs_generate()
        if result.success:
            assert len(result.stdout.strip()) > 0, "docs --all produced no output"

    def test_output_dir(
        self,
        nit_with_ollama: NitRunner,
        project_dir: Path,
    ) -> None:
        """``--output-dir`` should create markdown files."""
        out = project_dir / "_docs_output"
        result = nit_with_ollama.docs_generate(output_dir=str(out))
        if result.success and out.exists():
            md_files = list(out.rglob("*.md"))
            assert len(md_files) > 0, "No .md files generated in output dir"

    def test_specific_file(
        self,
        nit_with_ollama: NitRunner,
        project_manifest: ProjectManifest,
    ) -> None:
        """``--file`` should target a single source file."""
        if not project_manifest.untested_source_files:
            pytest.skip("No untested source files in manifest")
        target = project_manifest.untested_source_files[0]
        result = nit_with_ollama.docs_generate(files=[target])
        assert result.exit_code in (0, 1), (
            f"docs --file crashed (exit={result.exit_code}):\n{result.stderr}"
        )


class TestDocsReadme:
    """``nit docs --readme`` should produce README content."""

    def test_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        result = nit_with_ollama.docs_readme()
        assert result.exit_code in (0, 1), (
            f"docs --readme crashed (exit={result.exit_code}):\n{result.stderr}"
        )

    def test_produces_output(self, nit_with_ollama: NitRunner) -> None:
        result = nit_with_ollama.docs_readme()
        if result.success:
            assert len(result.stdout.strip()) > 0, "docs --readme produced no output"


class TestDocsCheck:
    """``nit docs --check`` should report doc status."""

    def test_does_not_crash(self, nit_with_ollama: NitRunner) -> None:
        result = nit_with_ollama.docs_check()
        assert result.exit_code in (0, 1), (
            f"docs --check crashed (exit={result.exit_code}):\n{result.stderr}"
        )
