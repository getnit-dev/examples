# Next.js App Example

Example Next.js + TypeScript + Vitest project for testing nit.

## Structure

- `src/utils/formatting.ts` - Text formatting utilities (untested)
- `src/utils/validation.ts` - Validation utilities (untested)
- `src/utils/math.ts` - Math utilities (partially tested)
- `tests/utils/math.test.ts` - Example tests showing project patterns

## Setup

```bash
npm install
```

## Run Tests

```bash
npm test
npm run test:coverage
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
- nit detects TypeScript and Vitest
- nit generates tests for `formatting.ts` and `validation.ts`
- Generated tests follow the describe/it/expect pattern from `math.test.ts`
- Coverage increases from ~30% to 80%+
