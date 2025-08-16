# Epic 1: Foundation & Basic Summary Analysis

**Epic Goal:** Establish foundational project infrastructure including database schema, manual transcript loading capability, and basic AI summary generation, delivering a functional transcript → client summary workflow that coaches can immediately test and validate for accuracy and usefulness.

## Story 1.1: Project Setup and Database Schema

**As a** development team,
**I want** a properly configured project structure with database schema,
**so that** we can store coaching sessions, client data, and generated summaries in a structured, queryable format.

### Acceptance Criteria
1. Monorepo project structure created with separate services for API, processing, and frontend
2. PostgreSQL database schema designed for coaches, sessions, clients, summaries, and notes
3. Database migrations and connection management configured
4. Environment configuration for development, testing, and production
5. Basic health-check endpoint responding with database connectivity status
6. Git repository initialized with branching strategy and CI/CD pipeline foundation

## Story 1.2: Manual Transcript Upload Interface

**As a** coach,
**I want** to manually upload session transcripts through a web interface,
**so that** I can begin testing the AI summary generation with my actual coaching sessions.

### Acceptance Criteria
1. Simple web form for transcript text upload with session metadata (date, participants)
2. File upload capability supporting .txt and .docx transcript formats
3. Basic validation for transcript content and required session information
4. Participant name extraction and matching to create client records if needed
5. Successful upload confirmation with assigned session ID for tracking
6. Error handling for invalid files or missing required information

## Story 1.3: Basic AI Summary Generation

**As a** coach,
**I want** AI-generated summaries created from uploaded transcripts,
**so that** I can evaluate the quality and accuracy of automated session analysis.

### Acceptance Criteria
1. OpenAI GPT-4 integration configured for transcript analysis and summary generation
2. Prompt templates developed for extracting client wins, challenges, action items, and coach recommendations
3. Structured summary format using narrative + bullet points as specified in requirements
4. Individual client summary generation for each participant identified in transcript
5. Summary storage in database with linkage to original session and client records
6. Basic error handling for API failures with graceful degradation and retry logic

## Story 1.4: Summary Review and Display

**As a** coach,
**I want** to view generated summaries in a clean, readable format,
**so that** I can assess the AI's understanding of my coaching session and client needs.

### Acceptance Criteria
1. Web interface displaying session summaries with clear client-by-client organization
2. Summary presentation using narrative + bullet format optimized for coach review
3. Session metadata display including date, duration, and participant count
4. Individual client summary views with wins, challenges, action items, and recommendations
5. Basic navigation between different sessions and client summaries
6. Responsive design supporting both desktop and mobile review workflows

## Story 1.5: Manual Summary Editing

**As a** coach,
**I want** to manually edit and correct generated summaries,
**so that** I can refine the AI output and validate that the system captures my coaching insights accurately.

### Acceptance Criteria
1. Inline editing capability for all summary sections (wins, challenges, actions, recommendations)
2. Edit history tracking showing original AI version and coach modifications
3. Save functionality preserving both original AI output and coach-edited versions
4. Character limits and formatting validation ensuring summary structure consistency
5. Auto-save functionality preventing loss of coach edits during long review sessions
6. Clear visual indicators distinguishing AI-generated content from coach modifications
