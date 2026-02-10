"""Heuristics: nit config — configuration management tests."""

from __future__ import annotations

import pytest

from tests.assertions import assert_config_llm_section, assert_config_project_section
from tests.nit_runner import NitRunner

pytestmark = pytest.mark.heuristics


class TestConfigValidate:
    """``nit config validate`` should pass after init."""

    def test_validates_after_init(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.config_validate()
        assert result.success, f"config validate failed:\n{result.stderr}"


class TestConfigShow:
    """``nit config show`` should return parseable config."""

    def test_json_output(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.config_show(json_output=True)
        assert result.success, f"config show failed:\n{result.stderr}"
        data = result.json()
        assert isinstance(data, dict)

    def test_has_project_section(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.config_show(json_output=True)
        data = result.json()
        assert "project" in data

    def test_has_llm_section(self, nit: NitRunner) -> None:
        nit.init()
        result = nit.config_show(json_output=True)
        data = result.json()
        assert "llm" in data

    def test_project_section_fields(self, nit: NitRunner) -> None:
        """Project section has root and primary_language."""
        nit.init()
        result = nit.config_show(json_output=True)
        data = result.json()
        assert_config_project_section(data)

    def test_llm_section_fields(self, nit: NitRunner) -> None:
        """LLM section has mode, provider, model."""
        nit.init()
        result = nit.config_show(json_output=True)
        data = result.json()
        assert_config_llm_section(data)


class TestConfigSet:
    """``nit config set`` should update config values."""

    def test_set_and_read_back(self, nit: NitRunner) -> None:
        nit.init()
        nit.config_set("platform.mode", "disabled")
        result = nit.config_show(json_output=True)
        data = result.json()
        assert data.get("platform", {}).get("mode") == "disabled"
