# External APIs

## OpenAI GPT-4 API

- **Purpose:** Generate coaching summaries, handle natural language refinement, extract insights from transcripts
- **Documentation:** https://platform.openai.com/docs/api-reference
- **Base URL(s):** https://api.openai.com/v1
- **Authentication:** Bearer token (API key stored in AWS Secrets Manager)
- **Rate Limits:** 10,000 RPM, 2,000,000 TPM for GPT-4 Turbo

**Key Endpoints Used:**
- `POST /chat/completions` - Generate summaries and process refinements
- `POST /embeddings` - Create vector embeddings for semantic search

**Integration Notes:** Implement exponential backoff for rate limits, use streaming for long responses, maintain prompt version control

## AWS SES API

- **Purpose:** Send notification emails to coaches and follow-up emails to clients
- **Documentation:** https://docs.aws.amazon.com/ses/latest/APIReference/
- **Base URL(s):** https://email.us-east-1.amazonaws.com
- **Authentication:** AWS IAM role-based authentication
- **Rate Limits:** 14 emails/second (adjustable based on reputation)

**Key Endpoints Used:**
- `POST /` (SendEmail action) - Send individual emails
- `POST /` (SendBulkTemplatedEmail action) - Batch email operations

**Integration Notes:** Configure SPF/DKIM for deliverability, handle bounces via SNS, implement retry logic for throttling

## Pinecone Vector Database API

- **Purpose:** Store and query vector embeddings for semantic search across coaching sessions
- **Documentation:** https://docs.pinecone.io/reference
- **Base URL(s):** https://[index-name]-[project-id].svc.[environment].pinecone.io
- **Authentication:** API key authentication
- **Rate Limits:** Based on subscription tier

**Key Endpoints Used:**
- `POST /vectors/upsert` - Store coaching content embeddings
- `POST /query` - Semantic similarity search
- `POST /vectors/delete` - Remove outdated embeddings

**Integration Notes:** Batch operations for efficiency, implement local caching for frequent queries, monitor index usage
