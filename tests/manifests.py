"""Project manifests — describes each example project's expected properties.

Adding a new language stack = one new ProjectManifest here + one new directory.
All parametrized tests run against it automatically.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProjectManifest:
    """Describes an example project for data-driven integration tests."""

    name: str
    path: str
    primary_language: str
    unit_framework: str
    expected_languages: list[str]
    expected_framework_names: list[str]
    untested_source_files: list[str]
    existing_test_files: list[str]
    setup_commands: list[str] = field(default_factory=list)
    expected_test_count_min: int = 1
    expected_all_pass: bool = True


NEXTJS_APP = ProjectManifest(
    name="nextjs-app",
    path="nextjs-app",
    primary_language="typescript",
    unit_framework="vitest",
    expected_languages=["typescript", "javascript"],
    expected_framework_names=["vitest"],
    untested_source_files=[
        "src/utils/formatting.ts",
        "src/utils/validation.ts",
    ],
    existing_test_files=["tests/utils/math.test.ts"],
    setup_commands=["npm install"],
    expected_test_count_min=4,
    expected_all_pass=True,
)

PYTHON_API = ProjectManifest(
    name="python-api",
    path="python-api",
    primary_language="python",
    unit_framework="pytest",
    expected_languages=["python"],
    expected_framework_names=["pytest"],
    untested_source_files=[
        "src/api/services/validators.py",
        "src/api/utils/helpers.py",
    ],
    existing_test_files=["tests/services/test_auth.py"],
    setup_commands=["pip install -e '.[dev]'"],
    expected_test_count_min=4,
    expected_all_pass=True,
)

GO_API = ProjectManifest(
    name="go-api",
    path="go-api",
    primary_language="go",
    unit_framework="gotest",
    expected_languages=["go"],
    expected_framework_names=["gotest"],
    untested_source_files=["main.go"],
    existing_test_files=["handlers/users_test.go"],
    setup_commands=["go mod download"],
    expected_test_count_min=1,
    expected_all_pass=True,
)

CPP_CMAKE = ProjectManifest(
    name="cpp-cmake",
    path="cpp-cmake",
    primary_language="cpp",
    unit_framework="gtest",
    expected_languages=["cpp"],
    expected_framework_names=["gtest"],
    untested_source_files=["src/math_utils.cpp"],
    existing_test_files=["tests/test_math.cpp"],
    setup_commands=["mkdir -p build", "cd build && cmake .. && cmake --build ."],
    expected_test_count_min=1,
    expected_all_pass=True,
)

JAVA_GRADLE = ProjectManifest(
    name="java-gradle",
    path="java-gradle",
    primary_language="java",
    unit_framework="junit5",
    expected_languages=["java"],
    expected_framework_names=["junit5"],
    untested_source_files=["src/main/java/com/example/StringUtils.java"],
    existing_test_files=["src/test/java/com/example/CalculatorTest.java"],
    setup_commands=["gradle build"],
    expected_test_count_min=1,
    expected_all_pass=True,
)

RUST_CLI = ProjectManifest(
    name="rust-cli",
    path="rust-cli",
    primary_language="rust",
    unit_framework="cargo_test",
    expected_languages=["rust"],
    expected_framework_names=["cargo_test"],
    untested_source_files=["src/main.rs"],
    existing_test_files=["src/lib.rs"],
    setup_commands=["cargo build"],
    expected_test_count_min=1,
    expected_all_pass=True,
)

CSHARP_DOTNET = ProjectManifest(
    name="csharp-dotnet",
    path="csharp-dotnet",
    primary_language="csharp",
    unit_framework="xunit",
    expected_languages=["csharp"],
    expected_framework_names=["xunit"],
    untested_source_files=["src/StringProcessor.cs"],
    existing_test_files=["tests/StringProcessorTests.cs"],
    setup_commands=["dotnet build"],
    expected_test_count_min=1,
    expected_all_pass=True,
)

MONOREPO = ProjectManifest(
    name="monorepo",
    path="monorepo",
    primary_language="python",
    unit_framework="pytest",
    expected_languages=["typescript", "python"],
    expected_framework_names=["vitest", "pytest"],
    untested_source_files=["packages/utils/src/utils/helpers.py"],
    existing_test_files=[
        "packages/api/tests/index.test.ts",
        "packages/utils/tests/test_helpers.py",
    ],
    setup_commands=["pnpm install"],
    expected_test_count_min=1,
    expected_all_pass=True,
)

ALL_PROJECTS: list[ProjectManifest] = [
    NEXTJS_APP,
    PYTHON_API,
    GO_API,
    CPP_CMAKE,
    JAVA_GRADLE,
    RUST_CLI,
    CSHARP_DOTNET,
    MONOREPO,
]


def get_project(name: str) -> ProjectManifest:
    """Look up a manifest by project name."""
    for p in ALL_PROJECTS:
        if p.name == name:
            return p
    msg = f"No manifest for project: {name}"
    raise KeyError(msg)
