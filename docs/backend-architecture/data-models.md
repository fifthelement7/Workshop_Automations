# Data Models

## Coach

**Purpose:** Represents coaches who use the platform to manage their sessions and clients

**Key Attributes:**
- id: UUID - Unique identifier
- email: String - Coach login and notification email  
- name: String - Display name
- organization_id: UUID - Link to coaching organization
- voice_profile: JSON - Learned communication style preferences
- notification_preferences: JSON - Email timing and frequency settings
- created_at: Timestamp - Account creation date
- last_login: Timestamp - Most recent platform access

**Relationships:**
- Has many Sessions (as facilitator)
- Has many Clients (through sessions)
- Belongs to Organization
- Has many Templates

## Session

**Purpose:** Represents a coaching session (workshop, one-on-one, etc.)

**Key Attributes:**
- id: UUID - Unique identifier
- coach_id: UUID - Facilitating coach
- session_date: Date - When session occurred
- session_type: Enum - Workshop type (group, individual, etc.)
- transcript_url: String - S3 location of original transcript
- duration_minutes: Integer - Session length
- participant_count: Integer - Number of attendees
- processing_status: Enum - Current pipeline state
- metadata: JSON - Additional session context

**Relationships:**
- Belongs to Coach
- Has many ClientSessions (participants)
- Has many Summaries
- Has one ProcessingJob

## Client

**Purpose:** Individual who participates in coaching sessions

**Key Attributes:**
- id: UUID - Unique identifier
- name: String - Client full name
- email: String - Contact email (optional)
- organization_id: UUID - Company/group affiliation
- tags: Array[String] - Categorization tags
- engagement_score: Float - Calculated participation metric
- created_at: Timestamp - First session date

**Relationships:**
- Has many ClientSessions
- Has many Summaries
- Has many FollowUps
- Belongs to Organization

## ClientSession

**Purpose:** Junction table tracking client participation in specific sessions

**Key Attributes:**
- id: UUID - Unique identifier
- client_id: UUID - Participating client
- session_id: UUID - Session attended
- speaking_time_seconds: Integer - Total speaking duration
- engagement_level: Enum - High/Medium/Low/Silent
- breakthrough_detected: Boolean - Significant progress flag
- priority_score: Float - Follow-up urgency (0-1)

**Relationships:**
- Belongs to Client
- Belongs to Session
- Has one Summary

## Summary

**Purpose:** AI-generated and coach-refined session summary for a specific client

**Key Attributes:**
- id: UUID - Unique identifier
- client_session_id: UUID - Link to client's session participation
- wins: Text - Client achievements/progress
- challenges: Text - Issues and obstacles discussed
- action_items: Array[JSON] - Structured next steps
- coach_recommendations: Text - Professional guidance
- ai_version: Text - Original AI-generated content
- coach_edited_version: Text - Human-refined content
- refinement_history: JSON - Chat interaction log
- approved_at: Timestamp - Coach approval time

**Relationships:**
- Belongs to ClientSession
- Has many FollowUps
- Has RefinementHistory

## FollowUp

**Purpose:** Email communications sent to clients post-session

**Key Attributes:**
- id: UUID - Unique identifier
- summary_id: UUID - Source summary
- client_id: UUID - Recipient
- subject: String - Email subject line
- body: Text - Email content
- template_id: UUID - Source template used
- status: Enum - Draft/Scheduled/Sent/Failed
- sent_at: Timestamp - Delivery time
- scheduled_for: Timestamp - Future send time

**Relationships:**
- Belongs to Summary
- Belongs to Client
- Uses Template

## Template

**Purpose:** Reusable formats for summaries and follow-up emails

**Key Attributes:**
- id: UUID - Unique identifier
- name: String - Template name
- type: Enum - Summary/Email/Prompt
- workshop_type: String - Associated session type
- content: Text - Template with variables
- variables: Array[String] - Required placeholders
- coach_id: UUID - Owner (null for system templates)
- is_default: Boolean - Auto-selected flag

**Relationships:**
- Belongs to Coach (optional)
- Used by many FollowUps
- Used by many Summaries
