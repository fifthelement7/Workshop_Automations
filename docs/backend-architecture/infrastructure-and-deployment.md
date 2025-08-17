# Infrastructure and Deployment

## Infrastructure as Code

- **Tool:** Terraform 1.7.0
- **Location:** `infrastructure/terraform/`
- **Approach:** Modular Terraform with separate modules for each AWS service, environment-specific variables

## Deployment Strategy

- **Strategy:** Blue-Green deployment with automated rollback
- **CI/CD Platform:** GitHub Actions
- **Pipeline Configuration:** `.github/workflows/deploy.yml`

## Environments

- **Development:** Local Docker Compose environment for rapid iteration - Uses LocalStack for AWS services
- **Staging:** AWS ECS on Fargate with reduced capacity - Full integration with external services
- **Production:** AWS ECS on Fargate with auto-scaling - Multi-AZ deployment for high availability

## Environment Promotion Flow

```text
Local Development
    ↓ (git push)
CI/CD Pipeline
    ↓ (automated tests pass)
Staging Environment
    ↓ (manual approval + smoke tests)
Production Environment
    ↓ (canary deployment 10%)
Full Production Rollout
```

## Rollback Strategy

- **Primary Method:** Automated rollback on health check failures
- **Trigger Conditions:** 5XX error rate > 1%, P95 latency > 3s, Failed health checks
- **Recovery Time Objective:** < 5 minutes for automated rollback
