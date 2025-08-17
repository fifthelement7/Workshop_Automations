# Error Handling Strategy

## General Approach

- **Error Model:** Structured error responses with error codes and user-friendly messages
- **Exception Hierarchy:** Custom exceptions inheriting from base ApplicationError class
- **Error Propagation:** Errors bubble up to API layer for consistent client responses

## Logging Standards

- **Library:** structlog 24.1.0
- **Format:** JSON structured logging
- **Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Required Context:**
  - Correlation ID: UUID for request tracing
  - Service Context: service_name, version, environment
  - User Context: coach_id (never log PII)

## Error Handling Patterns

### External API Errors

- **Retry Policy:** Exponential backoff with jitter, max 3 retries
- **Circuit Breaker:** Open after 5 consecutive failures, half-open after 30s
- **Timeout Configuration:** OpenAI: 30s, AWS services: 10s
- **Error Translation:** Map external errors to internal error codes

### Business Logic Errors

- **Custom Exceptions:** ValidationError, AuthorizationError, ResourceNotFoundError
- **User-Facing Errors:** Sanitized messages without technical details
- **Error Codes:** COACH_001-999 series for consistent client handling

### Data Consistency

- **Transaction Strategy:** Database transactions with automatic rollback
- **Compensation Logic:** Saga pattern for multi-service operations
- **Idempotency:** UUID-based idempotency keys for critical operations
