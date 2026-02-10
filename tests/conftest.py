"""Root conftest — shared fixtures for nit integration tests."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

from tests.manifests import ALL_PROJECTS, ProjectManifest, get_project
from tests.nit_runner import NitRunner

EXAMPLES_ROOT = Path(__file__).resolve().parent.parent


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "heuristics: No LLM needed — fast, deterministic")
    config.addinivalue_line("markers", "llm: Requires Ollama LLM — slow, tolerant")


# ---------------------------------------------------------------------------
# Ollama auto-discovery
# ---------------------------------------------------------------------------

_MODEL_PREFERENCES = [
    "qwen2.5-coder",
    "llama3.1",
    "llama3",
    "mistral",
    "codellama",
]


@dataclass(frozen=True)
class OllamaInfo:
    """Result of Ollama auto-discovery."""

    available: bool
    host: str
    model: str


def _discover_ollama() -> OllamaInfo:
    """Probe Ollama once and return host + best available model.

    Checks ``OLLAMA_HOST`` env var (default ``http://localhost:11434``).
    Picks a model using a preference list, falling back to the first
    model returned by the API.
    """
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    if not host.startswith(("http://", "https://")):
        host = f"http://{host}"

    try:
        import httpx

        resp = httpx.get(f"{host}/api/tags", timeout=3)
        if resp.status_code != 200:
            return OllamaInfo(available=False, host=host, model="")

        data = resp.json()
        models = data.get("models", [])
        if not models:
            return OllamaInfo(available=False, host=host, model="")

        model_names = [m["name"] for m in models if m.get("name")]
        if not model_names:
            return OllamaInfo(available=False, host=host, model="")

        # Pick the best model by preference
        best = model_names[0]
        for pref in _MODEL_PREFERENCES:
            for name in model_names:
                if pref in name:
                    best = name
                    break
            else:
                continue
            break

        return OllamaInfo(available=True, host=host, model=best)
    except Exception:
        return OllamaInfo(available=False, host=host, model="")


# ---------------------------------------------------------------------------
# Session-scoped helpers
# ---------------------------------------------------------------------------


def _resolve_examples_root() -> Path:
    """Resolve the examples repo root, allowing env var override."""
    env = os.environ.get("EXAMPLES_DIR")
    if env:
        return Path(env).resolve()
    return EXAMPLES_ROOT


def _configure_ollama_for_project(
    nit: NitRunner,
    info: OllamaInfo,
) -> None:
    """Force Ollama config onto a project via ``nit config set``."""
    nit.config_set("llm.mode", "ollama")
    nit.config_set("llm.provider", "ollama")
    nit.config_set("llm.model", info.model)
    nit.config_set("llm.base_url", info.host)
    nit.config_set("platform.mode", "disabled")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def examples_root() -> Path:
    """Root directory of the examples repository."""
    return _resolve_examples_root()


@pytest.fixture(scope="session")
def ollama_info() -> OllamaInfo:
    """Ollama discovery result — host, model, availability."""
    return _discover_ollama()


@pytest.fixture(scope="session")
def ollama_available(ollama_info: OllamaInfo) -> bool:
    """Whether Ollama is running and has a model pulled."""
    return ollama_info.available


@pytest.fixture(
    params=[p.name for p in ALL_PROJECTS],
    scope="session",
)
def project_manifest(request: pytest.FixtureRequest) -> ProjectManifest:
    """Parametrized fixture — yields each project manifest in turn."""
    return get_project(request.param)


# Directories that should be symlinked instead of copied (too large or
# contain absolute paths that break when relocated).
_SYMLINK_DIRS = {
    "node_modules",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "target",       # Rust (cargo)
    "build",        # C++ (cmake), Java (gradle)
    ".gradle",      # Java (gradle cache)
    "bin",          # C# (dotnet)
    "obj",          # C# (dotnet)
}


@pytest.fixture(scope="session")
def project_dir(
    examples_root: Path,
    project_manifest: ProjectManifest,
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Working copy of the project in a temp directory.

    Copies the project so that nit commands (init, generate, etc.)
    do not pollute the original source tree. Heavy directories
    (node_modules, .venv) are symlinked to avoid slow copies and
    broken paths.
    """
    src = examples_root / project_manifest.path
    assert src.is_dir(), f"Project not found: {src}"

    dst = tmp_path_factory.mktemp(project_manifest.name)

    def _ignore(directory: str, entries: list[str]) -> set[str]:
        return {e for e in entries if e in _SYMLINK_DIRS}

    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=_ignore)

    # Symlink heavy dirs from original so they work without reinstall.
    # Walk the entire source tree to catch nested occurrences too
    # (e.g. pnpm workspace per-package node_modules/).
    for root, dirs, _files in os.walk(src):
        for dirname in list(dirs):
            if dirname in _SYMLINK_DIRS:
                original = Path(root) / dirname
                relative = original.relative_to(src)
                link = dst / relative
                # copytree's _ignore already excluded it, so just symlink
                if not link.exists() and not link.is_symlink():
                    link.symlink_to(original)
                # Don't descend into symlinked dirs
                dirs.remove(dirname)

    return dst


@pytest.fixture()
def nit(project_dir: Path) -> NitRunner:
    """NitRunner bound to the current project copy."""
    return NitRunner(project_dir)


@pytest.fixture()
def nit_with_ollama(
    nit: NitRunner,
    ollama_info: OllamaInfo,
) -> NitRunner:
    """NitRunner that has been init'd and configured with discovered Ollama.

    Calls ``nit init --auto``, then overrides LLM config with the
    Ollama host and model found during session-scoped discovery.
    """
    nit.init(auto=True)
    _configure_ollama_for_project(nit, ollama_info)
    return nit


# ---------------------------------------------------------------------------
# Git-enabled project fixture (for changelog tests)
# ---------------------------------------------------------------------------


def _init_git_repo(path: Path) -> None:
    """Initialize a git repo with an initial commit + v0.0.0 tag + second commit."""
    env = {**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "t@t.com",
           "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "t@t.com"}
    run = lambda *args: subprocess.run(  # noqa: E731
        args, cwd=str(path), capture_output=True, env=env, check=True,
    )
    run("git", "init")
    run("git", "add", "-A")
    run("git", "commit", "-m", "feat: initial commit")
    run("git", "tag", "v0.0.0")
    # Add a second commit so changelog has something to report
    marker = path / ".nit-changelog-marker"
    marker.write_text("test\n")
    run("git", "add", "-A")
    run("git", "commit", "-m", "fix: add changelog marker for testing")


@pytest.fixture(scope="session")
def project_dir_with_git(project_dir: Path) -> Path:
    """Project copy with git history (initial commit + tag + second commit)."""
    if not (project_dir / ".git").exists():
        _init_git_repo(project_dir)
    return project_dir
