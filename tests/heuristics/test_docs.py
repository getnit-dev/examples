"""Heuristics: nit docs — changelog generation (no LLM)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.assertions import assert_changelog_output
from tests.nit_runner import NitRunner

pytestmark = pytest.mark.heuristics


class TestDocsChangelog:
    """``nit docs --changelog`` with ``--no-llm`` should produce markdown."""

    def test_does_not_crash(
        self, nit: NitRunner, project_dir_with_git: Path,
    ) -> None:
        nit.init()
        result = nit.docs_changelog("v0.0.0", no_llm=True)
        assert result.exit_code in (0, 1), (
            f"changelog crashed (exit={result.exit_code}):\n{result.stderr}"
        )

    def test_produces_output(
        self, nit: NitRunner, project_dir_with_git: Path,
    ) -> None:
        nit.init()
        result = nit.docs_changelog("v0.0.0", no_llm=True)
        if result.success:
            assert len(result.stdout.strip()) > 0, "changelog produced no output"

    def test_contains_markdown(
        self, nit: NitRunner, project_dir: Path, project_dir_with_git: Path,
    ) -> None:
        nit.init()
        result = nit.docs_changelog("v0.0.0", no_llm=True)
        if result.success:
            changelog_file = project_dir / "CHANGELOG.md"
            assert changelog_file.exists(), "CHANGELOG.md was not created"
            assert_changelog_output(changelog_file.read_text())
