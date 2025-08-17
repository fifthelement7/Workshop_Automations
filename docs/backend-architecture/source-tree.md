# Source Tree

```plaintext
coaching-platform/
├── packages/
│   ├── api/                           # Coach Interface API
│   │   ├── src/
│   │   │   ├── auth/                  # Authentication/authorization
│   │   │   ├── routes/                # REST endpoints
│   │   │   ├── websocket/             # WebSocket handlers
│   │   │   ├── models/                # SQLAlchemy models
│   │   │   ├── schemas/               # Pydantic schemas
│   │   │   ├── repositories/          # Data access layer
│   │   │   └── main.py                # FastAPI app
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   ├── transcript-processor/           # Transcript Processing Service
│   │   ├── src/
│   │   │   ├── parsers/               # Transcript format parsers
│   │   │   ├── extractors/            # Participant extraction
│   │   │   ├── queue/                 # SQS handlers
│   │   │   └── main.py
│   │   └── tests/
│   │
│   ├── ai-analysis/                   # AI Analysis Service
│   │   ├── src/
│   │   │   ├── prompts/               # Prompt templates
│   │   │   ├── refinement/            # Iterative refinement
│   │   │   ├── voice/                 # Voice learning
│   │   │   ├── clients/               # OpenAI client
│   │   │   └── main.py
│   │   └── tests/
│   │
│   ├── search/                        # Natural Language Search Service
│   │   ├── src/
│   │   │   ├── indexers/              # Content indexing
│   │   │   ├── query/                 # Query processing
│   │   │   ├── ranking/               # Result ranking
│   │   │   └── main.py
│   │   └── tests/
│   │
│   ├── notifications/                 # Notification Service
│   │   ├── src/
│   │   │   ├── templates/             # Email templates
│   │   │   ├── scheduler/             # Send scheduling
│   │   │   ├── ses/                   # AWS SES client
│   │   │   └── main.py
│   │   └── tests/
│   │
│   ├── export/                        # Data Export Service
│   │   ├── src/
│   │   │   ├── formats/               # JSON/CSV formatters
│   │   │   ├── schemas/               # Export schemas
│   │   │   └── main.py
│   │   └── tests/
│   │
│   ├── web/                           # React/Next.js Frontend
│   │   ├── src/
│   │   │   ├── components/            # React components
│   │   │   ├── pages/                 # Next.js pages
│   │   │   ├── hooks/                 # Custom React hooks
│   │   │   ├── services/              # API clients
│   │   │   └── styles/                # CSS/styling
│   │   ├── public/
│   │   └── package.json
│   │
│   └── shared/                        # Shared utilities
│       ├── src/
│       │   ├── types/                 # Shared TypeScript types
│       │   ├── constants/             # Shared constants
│       │   └── utils/                 # Utility functions
│       └── package.json
│
├── infrastructure/                    # Infrastructure as Code
│   ├── terraform/
│   │   ├── modules/                   # Reusable Terraform modules
│   │   ├── environments/              # Environment-specific configs
│   │   └── main.tf
│   └── docker/                        # Docker configurations
│       ├── api.Dockerfile
│       └── docker-compose.yml
│
├── scripts/                           # Development and deployment scripts
│   ├── setup.sh                       # Initial setup
│   ├── deploy.sh                      # Deployment script
│   └── test.sh                        # Run all tests
│
├── docs/                              # Documentation
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
│
├── .github/                           # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── pyproject.toml                     # Python project configuration
├── package.json                       # Root package.json for monorepo
├── .env.example                       # Environment variables template
└── README.md
```
