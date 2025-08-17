# Coding Standards

## Core Standards

- **Languages & Runtimes:** Python 3.11.7, TypeScript 5.3.3, Node.js 20.11.0
- **Style & Linting:** Black + Ruff for Python, ESLint + Prettier for TypeScript
- **Test Organization:** Tests in `tests/` directory mirroring source structure

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Python Classes | PascalCase | `CoachService` |
| Python Functions | snake_case | `process_transcript` |
| TypeScript Classes | PascalCase | `SessionCard` |
| TypeScript Functions | camelCase | `generateSummary` |
| Database Tables | snake_case plural | `client_sessions` |
| API Endpoints | kebab-case | `/api/v1/coach-sessions` |
| Environment Variables | UPPER_SNAKE_CASE | `DATABASE_URL` |

## Critical Rules

- **No Direct Database Access:** All database operations must go through repository pattern
- **API Response Wrapper:** All API responses must use standardized ApiResponse type
- **No Hardcoded Secrets:** All secrets must come from AWS Secrets Manager
- **Async by Default:** Use async/await for all I/O operations
- **Type Everything:** No `any` types in TypeScript, use Pydantic models in Python
- **Log Correlation IDs:** Every log entry must include request correlation ID
- **Test Before Commit:** Minimum 80% code coverage for new code
