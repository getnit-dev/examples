"""NitRunner — subprocess wrapper for the nit CLI.

Provides a typed Python interface to invoke nit commands
and parse their output.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _find_nit_binary() -> list[str]:
    """Resolve the nit command to use.

    Priority:
    1. ``NIT_BIN`` env var (explicit override)
    2. ``nit`` in the same venv as the running Python
    3. ``nit`` in the ~/nit development venv
    4. ``nit`` on PATH
    5. ``python -m nit.cli`` as fallback
    """
    env_bin = os.environ.get("NIT_BIN")
    if env_bin:
        return [env_bin]

    # Check for nit alongside the current Python interpreter
    venv_nit = Path(sys.executable).parent / "nit"
    if venv_nit.is_file():
        return [str(venv_nit)]

    # Check for nit in the development venv
    dev_nit = Path.home() / "nit" / ".venv" / "bin" / "nit"
    if dev_nit.is_file():
        return [str(dev_nit)]

    # Check PATH
    if shutil.which("nit"):
        return ["nit"]

    # Fallback: run as module
    return [sys.executable, "-m", "nit.cli"]


@dataclass
class NitResult:
    """Result of a nit CLI invocation."""

    exit_code: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        return self.exit_code == 0

    def json(self) -> Any:
        """Parse JSON from stdout.

        nit --ci may emit human-readable lines before the JSON blob.
        This method finds and parses the first JSON object in stdout.
        """
        # Try the full output first (pure JSON commands)
        try:
            return json.loads(self.stdout)
        except (json.JSONDecodeError, ValueError):
            pass

        # Find the first line that starts a JSON object
        lines = self.stdout.splitlines()
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith("{"):
                candidate = "\n".join(lines[i:])
                try:
                    return json.loads(candidate)
                except (json.JSONDecodeError, ValueError):
                    continue

        msg = f"No JSON found in stdout: {self.stdout[:200]!r}"
        raise ValueError(msg)


class NitRunner:
    """Wraps subprocess calls to the nit CLI.

    Always runs with ``--ci`` for machine-readable output and
    ``--path`` pointing to the project directory.
    """

    def __init__(self, project_dir: Path, *, timeout: int = 300) -> None:
        self.project_dir = project_dir
        self.timeout = timeout
        self._nit_cmd = _find_nit_binary()

    def run(self, *args: str, timeout: int | None = None) -> NitResult:
        """Execute ``nit --ci <args>`` in the project directory.

        The ``--ci`` flag is prepended automatically. Callers should NOT
        include ``--path`` — it is injected by the convenience methods.
        For raw invocations, pass ``--path`` explicitly if needed.
        """
        cmd = [*self._nit_cmd, "--ci", *args]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout or self.timeout,
            cwd=str(self.project_dir),
        )
        return NitResult(
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    # --- Convenience methods -------------------------------------------------

    def init(self, *, auto: bool = True) -> NitResult:
        """Run ``nit init``."""
        args = ["init", "--path", str(self.project_dir)]
        if auto:
            args.append("--auto")
        return self.run(*args)

    def scan(
        self,
        *,
        json_output: bool = True,
        force: bool = False,
    ) -> NitResult:
        """Run ``nit scan``."""
        args = ["scan", "--path", str(self.project_dir)]
        if json_output:
            args.append("--json-output")
        if force:
            args.append("--force")
        return self.run(*args)

    def run_tests(self) -> NitResult:
        """Run ``nit run`` to execute the project's test suite."""
        return self.run("run", "--path", str(self.project_dir))

    def generate(self, *, test_type: str = "unit") -> NitResult:
        """Run ``nit generate``."""
        return self.run(
            "generate",
            "--type",
            test_type,
            "--path",
            str(self.project_dir),
            timeout=600,
        )

    def analyze(self, *, json_output: bool = True) -> NitResult:
        """Run ``nit analyze``."""
        args = ["analyze", "--path", str(self.project_dir)]
        if json_output:
            args.append("--json-output")
        return self.run(*args, timeout=600)

    def pick(self, *, test_type: str = "unit") -> NitResult:
        """Run ``nit pick`` — the full pipeline."""
        return self.run(
            "pick",
            "--type",
            test_type,
            "--path",
            str(self.project_dir),
            timeout=900,
        )

    def config_validate(self) -> NitResult:
        """Run ``nit config validate``."""
        return self.run("config", "validate", "--path", str(self.project_dir))

    def config_show(self, *, json_output: bool = True) -> NitResult:
        """Run ``nit config show``."""
        args = ["config", "show", "--path", str(self.project_dir)]
        if json_output:
            args.append("--json-output")
        return self.run(*args)

    def config_set(self, key: str, value: str) -> NitResult:
        """Run ``nit config set <key> <value>``."""
        return self.run(
            "config", "set", key, value, "--path", str(self.project_dir)
        )

    def memory_show(self, *, json_output: bool = True) -> NitResult:
        """Run ``nit memory show``."""
        args = ["memory", "show", "--path", str(self.project_dir)]
        if json_output:
            args.append("--json-output")
        return self.run(*args)

    def memory_reset(self) -> NitResult:
        """Run ``nit memory reset --confirm``."""
        return self.run(
            "memory", "reset", "--confirm", "--path", str(self.project_dir)
        )

    def memory_export(self) -> NitResult:
        """Run ``nit memory export``."""
        return self.run("memory", "export", "--path", str(self.project_dir))

    # --- Docs commands -------------------------------------------------------

    def docs_generate(
        self,
        *,
        files: list[str] | None = None,
        output_dir: str | None = None,
    ) -> NitResult:
        """Run ``nit docs --all`` or ``nit docs --file <f>``."""
        args = ["docs", "--path", str(self.project_dir)]
        if files:
            for f in files:
                args.extend(["--file", f])
        else:
            args.append("--all")
        if output_dir:
            args.extend(["--output-dir", output_dir])
        return self.run(*args, timeout=600)

    def docs_readme(self) -> NitResult:
        """Run ``nit docs --readme``."""
        return self.run(
            "docs", "--readme", "--path", str(self.project_dir), timeout=600,
        )

    def docs_changelog(
        self,
        tag: str,
        *,
        no_llm: bool = False,
        output: str | None = None,
    ) -> NitResult:
        """Run ``nit docs --changelog <tag>``."""
        args = ["docs", "--changelog", tag, "--path", str(self.project_dir)]
        if no_llm:
            args.append("--no-llm")
        if output:
            args.extend(["--output", output])
        return self.run(*args, timeout=300)

    def docs_check(self) -> NitResult:
        """Run ``nit docs --check``."""
        return self.run(
            "docs", "--check", "--path", str(self.project_dir), timeout=600,
        )

    # --- Drift commands ------------------------------------------------------

    def drift(
        self,
        *,
        tests_file: str | None = None,
    ) -> NitResult:
        """Run ``nit drift``."""
        args = ["drift", "--path", str(self.project_dir)]
        if tests_file:
            args.extend(["--tests-file", tests_file])
        return self.run(*args, timeout=600)

    def drift_baseline(
        self,
        *,
        tests_file: str | None = None,
    ) -> NitResult:
        """Run ``nit drift --baseline``."""
        args = ["drift", "--baseline", "--path", str(self.project_dir)]
        if tests_file:
            args.extend(["--tests-file", tests_file])
        return self.run(*args, timeout=600)

    # --- Debug, Report, Watch ------------------------------------------------

    def debug(self, *, dry_run: bool = False) -> NitResult:
        """Run ``nit debug``."""
        args = ["debug", "--path", str(self.project_dir)]
        if dry_run:
            args.append("--dry-run")
        return self.run(*args, timeout=600)

    def report_html(self) -> NitResult:
        """Run ``nit report --html``."""
        return self.run(
            "report", "--html", "--path", str(self.project_dir), timeout=300,
        )

    def watch(self, *, max_runs: int = 1, interval: int = 10) -> NitResult:
        """Run ``nit watch --max-runs N``."""
        return self.run(
            "watch",
            "--max-runs", str(max_runs),
            "--interval", str(interval),
            "--path", str(self.project_dir),
            timeout=300,
        )
