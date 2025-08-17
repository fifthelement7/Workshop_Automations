# Test Strategy and Standards

## Testing Philosophy

- **Approach:** Test-Driven Development (TDD) for critical business logic
- **Coverage Goals:** 80% overall, 90% for business logic, 70% for infrastructure
- **Test Pyramid:** 60% unit, 30% integration, 10% E2E

## Test Types and Organization

### Unit Tests

- **Framework:** pytest 8.0.0
- **File Convention:** `test_[module_name].py`
- **Location:** `tests/unit/` within each service
- **Mocking Library:** pytest-mock
- **Coverage Requirement:** 90% for business logic

**AI Agent Requirements:**
- Generate tests for all public methods
- Cover edge cases and error conditions
- Follow AAA pattern (Arrange, Act, Assert)
- Mock all external dependencies

### Integration Tests

- **Scope:** Service boundaries and database interactions
- **Location:** `tests/integration/` within each service
- **Test Infrastructure:**
  - **Database:** Testcontainers PostgreSQL
  - **Message Queue:** LocalStack SQS
  - **External APIs:** VCR.py for recording/replaying

### End-to-End Tests

- **Framework:** Playwright 1.41.0
- **Scope:** Critical user journeys (session upload, refinement, search)
- **Environment:** Staging environment with test data
- **Test Data:** Dedicated test organization with synthetic data

## Test Data Management

- **Strategy:** Factories for test data generation
- **Fixtures:** `tests/fixtures/` for static test data
- **Factories:** Factory pattern using Factory Boy
- **Cleanup:** Automatic cleanup after each test run

## Continuous Testing

- **CI Integration:** Run on every PR, block merge on failure
- **Performance Tests:** Locust for load testing critical endpoints
- **Security Tests:** Bandit for Python, npm audit for JavaScript
