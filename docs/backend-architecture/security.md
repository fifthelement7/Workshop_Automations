# Security

## Input Validation

- **Validation Library:** Pydantic for Python, Zod for TypeScript
- **Validation Location:** API boundary before any processing
- **Required Rules:**
  - All external inputs MUST be validated
  - Validation at API boundary before processing
  - Whitelist approach preferred over blacklist

## Authentication & Authorization

- **Auth Method:** JWT with refresh tokens
- **Session Management:** Redis-backed sessions with 24h expiry
- **Required Patterns:**
  - Role-based access control (Coach, Coach Lead, Admin)
  - Organization-level data isolation
  - API key authentication for service-to-service

## Secrets Management

- **Development:** .env files (never committed)
- **Production:** AWS Secrets Manager
- **Code Requirements:**
  - NEVER hardcode secrets
  - Access via configuration service only
  - No secrets in logs or error messages

## API Security

- **Rate Limiting:** 100 requests/minute per coach
- **CORS Policy:** Configured for frontend domain only
- **Security Headers:** X-Frame-Options, CSP, HSTS
- **HTTPS Enforcement:** TLS 1.3 only, redirect all HTTP

## Data Protection

- **Encryption at Rest:** AWS RDS encryption, S3 server-side encryption
- **Encryption in Transit:** TLS 1.3 for all connections
- **PII Handling:** Mask client emails in logs, encrypt in database
- **Logging Restrictions:** Never log passwords, tokens, or full transcripts

## Dependency Security

- **Scanning Tool:** Snyk for vulnerability scanning
- **Update Policy:** Monthly security updates, immediate for critical
- **Approval Process:** Security review for new dependencies

## Security Testing

- **SAST Tool:** Semgrep for code analysis
- **DAST Tool:** OWASP ZAP for API testing
- **Penetration Testing:** Quarterly third-party assessment

## HIPAA Compliance (Health Coaching Context)

- **Administrative Safeguards:**
  - Business Associate Agreements (BAA) with AWS and all third-party services
  - Workforce training on PHI handling procedures
  - Access control policies with role-based permissions
  - Audit logs for all PHI access and modifications
  - Incident response plan for potential breaches

- **Physical Safeguards:**
  - AWS data center physical security (inherited)
  - Workstation security policies for coaches
  - Device encryption requirements for mobile access

- **Technical Safeguards:**
  - Access Control: Multi-factor authentication (MFA) required for all coach accounts
  - Audit Controls: CloudTrail for infrastructure, application-level audit logs for PHI access
  - Integrity Controls: Checksums for transcript storage, database transaction logs
  - Transmission Security: TLS 1.3 minimum, VPN for administrative access
  - Encryption Standards: AES-256 for data at rest, TLS 1.3 for transit

- **PHI Data Handling:**
  - Client health information classification and tagging
  - Automatic PHI detection in transcripts using NLP
  - Data retention: 7 years per HIPAA requirements
  - Data disposal: Secure deletion with audit trail
  - Minimum necessary access principle enforced

- **Breach Notification:**
  - Automated detection of unauthorized access attempts
  - 60-day breach notification compliance workflow
  - Breach risk assessment documentation system
