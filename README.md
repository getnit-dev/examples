# nit Example Projects

A collection of example projects spanning **7 languages and 7 test frameworks** for testing and demonstrating [nit](https://github.com/getnit/nit) — the open-source AI testing agent.

Each project ships with partial test coverage and intentionally untested code, making them ideal targets for nit to analyze, generate tests for, and improve coverage.

## Repository Overview

| Project | Language | Framework / Build | Test Framework | Directory |
|---|---|---|---|---|
| [Next.js App](#nextjs-app) | TypeScript | Next.js 16 | Vitest | [nextjs-app/](nextjs-app/) |
| [Python API](#python-api) | Python 3.11+ | FastAPI | pytest | [python-api/](python-api/) |
| [Go API](#go-api) | Go 1.21 | stdlib | go test | [go-api/](go-api/) |
| [Rust CLI](#rust-cli) | Rust 2021 | Cargo | built-in | [rust-cli/](rust-cli/) |
| [C++ CMake](#c-cmake) | C++17 | CMake | Google Test | [cpp-cmake/](cpp-cmake/) |
| [C# .NET](#c-net) | C# / .NET 9.0 | dotnet | xUnit | [csharp-dotnet/](csharp-dotnet/) |
| [Java Gradle](#java-gradle) | Java 17 | Gradle | JUnit 5 | [java-gradle/](java-gradle/) |
| [Monorepo](#monorepo) | TS + Python | pnpm + Turbo | Vitest + pytest | [monorepo/](monorepo/) |

---

## Example Projects

### Next.js App

A modern Next.js application with TypeScript strict mode and Vitest.

- **Source:** `src/utils/math.ts`, `formatting.ts`, `validation.ts`
- **Tests:** `tests/utils/math.test.ts` (partial)
- **Untested:** `formatting.ts`, `validation.ts`

```bash
cd nextjs-app && npm install
npm test
```

### Python API

A FastAPI service with type hints and pytest fixtures.

- **Source:** `src/api/services/auth.py`, `validators.py`, `utils/helpers.py`
- **Tests:** `tests/services/test_auth.py` (partial)
- **Untested:** `validators.py`, `helpers.py`

```bash
cd python-api && pip install -e ".[dev]"
pytest
```

### Go API

A Go HTTP API with handler-based routing.

- **Source:** `handlers/users.go`, `main.go`
- **Tests:** `handlers/users_test.go` (partial)

```bash
cd go-api
go test ./...
```

### Rust CLI

A Rust command-line application using Cargo.

- **Source:** `src/main.rs`, `src/lib.rs`

```bash
cd rust-cli
cargo test
```

### C++ CMake

A C++17 project using CMake and Google Test.

- **Source:** `src/math_utils.h`, `src/math_utils.cpp`
- **Tests:** `tests/test_math.cpp`

```bash
cd cpp-cmake
cmake -B build && cmake --build build
cd build && ctest
```

### C# .NET

A .NET 9.0 project with xUnit tests.

- **Source:** `src/StringProcessor.cs`
- **Tests:** `tests/StringProcessorTests.cs`

```bash
cd csharp-dotnet
dotnet test
```

### Java Gradle

A Java 17 project with JUnit 5 (Jupiter).

- **Source:** `src/main/java/com/example/Calculator.java`, `StringUtils.java`
- **Tests:** `src/test/java/com/example/CalculatorTest.java`

```bash
cd java-gradle
gradle test
```

### Monorepo

A pnpm workspace with Turborepo orchestration containing mixed-language packages.

| Package | Language | Test Framework |
|---|---|---|
| `packages/api` | TypeScript | Vitest |
| `packages/utils` | Python | pytest |

```bash
cd monorepo
pnpm install
pnpm test        # runs turbo run test across all packages
```

---

## Quick Start with nit

Pick any example project and run:

```bash
cd <project-directory>
pip install getnit
nit init
nit scan
nit generate
nit run
```

### Expected Results

After running `nit generate`, you should see:

- Automatically generated tests matching your project's existing patterns
- Tests that follow established conventions (`describe`/`it` vs `test_function` style)
- Syntactically valid, properly formatted test code
- All generated tests passing when run
- Coverage increase from ~30% to 80%+

---

## Integration Test Suite

The [tests/](tests/) directory contains a comprehensive integration test suite that validates nit's behavior across all example projects. Tests are split into two categories:

### Heuristics Tests

Fast, deterministic tests that verify nit's static analysis capabilities:

- **Config** — project configuration detection
- **Init** — initialization and setup
- **Scan** — untested code discovery
- **Run** — test execution
- **Report** — coverage reporting
- **Watch** — file watch mode
- **Docs** — documentation generation
- **Memory** — performance characteristics

### LLM Tests

Tests that exercise nit's AI-powered features (requires an Ollama instance):

- **Generate** — test generation quality
- **Analyze** — code analysis accuracy
- **Pick** — intelligent test selection
- **Debug** — failure diagnosis
- **Drift** — test drift detection
- **Docs** — AI-driven documentation

### Running the Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run heuristic tests only (fast, no LLM required)
pytest tests/heuristics/

# Run LLM tests (requires Ollama running locally)
pytest tests/llm/ --timeout=600

# Filter by project
pytest tests/heuristics/ -k "nextjs"
pytest tests/llm/ -k "python_api"
```

### Test Infrastructure

- [tests/conftest.py](tests/conftest.py) — Session-scoped fixtures, Ollama auto-discovery, pytest markers
- [tests/manifests.py](tests/manifests.py) — Data-driven project manifests defining expected languages, frameworks, untested files, and test counts
- [tests/nit_runner.py](tests/nit_runner.py) — Subprocess wrapper for invoking the nit CLI with JSON parsing
- [tests/assertions.py](tests/assertions.py) — Custom assertion helpers

---

## CI/CD

The [ci.yml](.github/workflows/ci.yml) workflow runs on every push to `main` and on pull requests. It executes two parallel job matrices across all projects:

| Job | Description | Timeout |
|---|---|---|
| **Heuristics** | Deterministic static analysis tests | Default |
| **LLM** | AI-powered tests via Ollama (tinyllama) | 30 min |

Each job sets up the appropriate toolchain for its project (Node.js, Python, Go, Rust, .NET, Java, CMake, pnpm) before running the relevant test suite.

---

## Project Structure

```
examples/
  .github/workflows/ci.yml    # CI pipeline
  nextjs-app/                  # TypeScript + Vitest
  python-api/                  # Python + pytest
  go-api/                      # Go + go test
  rust-cli/                    # Rust + cargo test
  cpp-cmake/                   # C++17 + Google Test
  csharp-dotnet/               # C# + xUnit
  java-gradle/                 # Java + JUnit 5
  monorepo/                    # pnpm + Turbo (TS + Python)
  tests/
    heuristics/                # Deterministic integration tests
    llm/                       # AI-powered integration tests
    conftest.py                # Shared fixtures
    manifests.py               # Project definitions
    nit_runner.py              # CLI wrapper
    assertions.py              # Custom assertions
  pyproject.toml               # Root test dependencies
  examples.sln                 # .NET solution file
  LICENSE                      # MIT
```

## Contributing

Found an issue or have a suggestion? Open an issue at [github.com/getnit/nit](https://github.com/getnit/nit/issues).

## License

[MIT](LICENSE) — Copyright 2026 getnit-dev
