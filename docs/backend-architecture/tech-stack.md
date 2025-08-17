# Tech Stack

This is the DEFINITIVE technology selection for the entire platform. All components must use these specific versions and technologies.

## Cloud Infrastructure

- **Provider:** AWS
- **Key Services:** Lambda, API Gateway, RDS, S3, SQS/SNS, SES, CloudWatch, Secrets Manager
- **Deployment Regions:** us-east-1 (primary), us-west-2 (DR)

## Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-----------|
| **Language - Backend** | Python | 3.11.7 | Primary backend development | Excellent AI/ML ecosystem, FastAPI support, team expertise |
| **Language - Frontend** | TypeScript | 5.3.3 | Frontend development | Type safety, excellent tooling, React ecosystem |
| **Runtime - Backend** | Python | 3.11.7 | Backend runtime environment | Stable, performant, wide library support |
| **Runtime - Frontend** | Node.js | 20.11.0 | Frontend build and SSR | LTS version, Next.js compatibility |
| **Framework - Backend** | FastAPI | 0.109.0 | REST API and WebSocket server | High performance, automatic OpenAPI docs, WebSocket support |
| **Framework - Frontend** | Next.js | 14.1.0 | React framework with SSR | SEO optimization, excellent DX, built-in optimization |
| **UI Library** | React | 18.2.0 | User interface components | Component model, vast ecosystem, team familiarity |
| **Database - Primary** | PostgreSQL | 16.1 | Structured coaching data | JSONB support, full-text search, reliability |
| **Database - Vector** | Pinecone | - | Semantic search embeddings | Purpose-built for vector search, managed service |
| **Database - Cache** | Redis | 7.2.4 | Session cache and real-time data | WebSocket state, API response caching |
| **Message Queue** | AWS SQS | - | Asynchronous job processing | Managed service, reliable delivery, dead letter queues |
| **Event Bus** | AWS SNS | - | Service event distribution | Fan-out pattern, service decoupling |
| **Object Storage** | AWS S3 | - | Transcript and document storage | Unlimited scale, lifecycle policies, cost-effective |
| **AI/LLM Provider** | OpenAI GPT-4 | gpt-4-turbo | Transcript analysis and NL processing | Best accuracy, function calling, long context |
| **Email Service** | AWS SES | - | Coach notifications and client emails | Cost-effective, high deliverability, AWS integration |
| **Search Engine** | Elasticsearch | 8.11.3 | Full-text and tag-based search | Powerful query DSL, aggregations, faceting |
| **API Documentation** | OpenAPI/Swagger | 3.0.0 | API specification and docs | Industry standard, code generation, testing |
| **Testing - Python** | pytest | 8.0.0 | Python unit and integration tests | Powerful fixtures, excellent reporting |
| **Testing - JavaScript** | Jest | 29.7.0 | JavaScript/React testing | Snapshot testing, good React support |
| **Testing - E2E** | Playwright | 1.41.0 | End-to-end browser testing | Cross-browser support, reliable automation |
| **Monitoring** | Datadog | - | APM and infrastructure monitoring | Comprehensive observability, AI insights |
| **IaC** | Terraform | 1.7.0 | Infrastructure as code | Multi-cloud support, state management |
| **Container** | Docker | 25.0.0 | Containerization for services | Development parity, easy deployment |
| **Orchestration** | AWS ECS | - | Container orchestration | Managed service, AWS integration, Fargate support |
