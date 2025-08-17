# Database Schema

## PostgreSQL Schema

```sql
-- Core Tables
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE coaches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    voice_profile JSONB DEFAULT '{}',
    notification_preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID REFERENCES coaches(id),
    session_date DATE NOT NULL,
    session_type VARCHAR(50) NOT NULL,
    transcript_url TEXT,
    duration_minutes INTEGER,
    participant_count INTEGER,
    processing_status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sessions_coach_date (coach_id, session_date)
);

CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    organization_id UUID REFERENCES organizations(id),
    tags TEXT[],
    engagement_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_clients_org (organization_id)
);

CREATE TABLE client_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id),
    session_id UUID REFERENCES sessions(id),
    speaking_time_seconds INTEGER,
    engagement_level VARCHAR(20),
    breakthrough_detected BOOLEAN DEFAULT FALSE,
    priority_score DECIMAL(3,2),
    UNIQUE(client_id, session_id)
);

CREATE TABLE summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_session_id UUID REFERENCES client_sessions(id),
    wins TEXT,
    challenges TEXT,
    action_items JSONB,
    coach_recommendations TEXT,
    ai_version TEXT,
    coach_edited_version TEXT,
    refinement_history JSONB DEFAULT '[]',
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    workshop_type VARCHAR(100),
    content TEXT NOT NULL,
    variables TEXT[],
    coach_id UUID REFERENCES coaches(id),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE follow_ups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    summary_id UUID REFERENCES summaries(id),
    client_id UUID REFERENCES clients(id),
    subject VARCHAR(500),
    body TEXT,
    template_id UUID REFERENCES templates(id),
    status VARCHAR(50) DEFAULT 'draft',
    sent_at TIMESTAMP,
    scheduled_for TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_summaries_approved ON summaries(approved_at) WHERE approved_at IS NOT NULL;
CREATE INDEX idx_follow_ups_status ON follow_ups(status);
CREATE INDEX idx_sessions_processing ON sessions(processing_status);

-- Full text search
ALTER TABLE summaries ADD COLUMN search_vector tsvector;
CREATE INDEX idx_summaries_search ON summaries USING GIN(search_vector);

-- Trigger to update search vector
CREATE TRIGGER summaries_search_update
BEFORE INSERT OR UPDATE ON summaries
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', wins, challenges, coach_recommendations);
```

## Vector Database Schema (Pinecone)

```json
{
  "index_name": "coaching-sessions",
  "dimension": 1536,
  "metric": "cosine",
  "metadata_config": {
    "indexed": [
      "coach_id",
      "client_id",
      "session_date",
      "session_type",
      "tags"
    ]
  },
  "vector_schema": {
    "id": "summary_id",
    "values": "[1536-dimensional embedding]",
    "metadata": {
      "coach_id": "uuid",
      "client_id": "uuid",
      "session_id": "uuid",
      "session_date": "date",
      "session_type": "string",
      "content_type": "wins|challenges|actions|recommendations",
      "text_preview": "first 200 chars"
    }
  }
}
```

## Vector Database Backup & Recovery Strategy

**Backup Architecture:**
- **Dual Indexing:** Simultaneous indexing to Pinecone (primary) and Elasticsearch (backup)
- **Source of Truth:** PostgreSQL stores original text + embeddings as JSONB
- **Backup Frequency:** Real-time dual writes, daily full export to S3
- **Export Format:** Parquet files with embeddings + metadata, partitioned by date

**Backup Implementation:**
```python