"""Heuristics: nit init — project initialization tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.nit_runner import NitRunner

pytestmark = pytest.mark.heuristics


class TestInitAuto:
    """``nit init --auto`` should detect the stack and create config files."""

    def test_creates_profile(self, nit: NitRunner, project_dir: Path) -> None:
        result = nit.init(auto=True)
        assert result.success, f"init --auto failed:\n{result.stderr}"
        assert (project_dir / ".nit" / "profile.json").is_file()

    def test_creates_nit_yml(self, nit: NitRunner, project_dir: Path) -> None:
        nit.init(auto=True)
        assert (project_dir / ".nit.yml").is_file()

    def test_exit_code_zero(self, nit: NitRunner) -> None:
        result = nit.init(auto=True)
        assert result.exit_code == 0


class TestInitQuick:
    """``nit init --quick`` should also produce valid config."""

    def test_creates_profile(self, nit: NitRunner, project_dir: Path) -> None:
        result = nit.run("init", "--quick", "--path", str(project_dir))
        assert result.success, f"init --quick failed:\n{result.stderr}"
        assert (project_dir / ".nit" / "profile.json").is_file()
