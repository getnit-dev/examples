# Python API Example

Example Python + FastAPI + pytest project for testing nit.

## Structure

- `src/api/services/auth.py` - Authentication functions (partially tested)
- `src/api/services/validators.py` - Validation functions (untested)
- `src/api/utils/helpers.py` - Helper utilities (untested)
- `tests/services/test_auth.py` - Example tests showing project patterns
- `tests/conftest.py` - pytest fixtures

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

## Run Tests

```bash
pytest
pytest --cov=src --cov-report=html
```

## Testing with nit

```bash
# Initialize nit
nit init

# Scan for untested code
nit scan

# Generate tests
nit generate

# Run all tests
nit run
```

Expected outcome:
- nit detects Python and pytest
- nit generates tests for untested functions in `auth.py`, `validators.py`, and `helpers.py`
- Generated tests follow the function-based, assert-style pattern from `test_auth.py`
- Generated tests use pytest fixtures from `conftest.py`
- Coverage increases from ~30% to 80%+
