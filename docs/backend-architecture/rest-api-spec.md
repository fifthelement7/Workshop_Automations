# REST API Spec

```yaml
openapi: 3.0.0
info:
  title: Coaching Platform API
  version: 1.0.0
  description: Backend API for the Coaching Supervision & Automation Platform
servers:
  - url: https://api.coachingplatform.com/v1
    description: Production server
  - url: http://localhost:8000/v1
    description: Development server

paths:
  /auth/login:
    post:
      summary: Authenticate coach
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        200:
          description: Successful authentication
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  refresh_token:
                    type: string
                  
  /sessions:
    get:
      summary: List coaching sessions
      parameters:
        - name: coach_id
          in: query
          schema:
            type: string
        - name: date_from
          in: query
          schema:
            type: string
            format: date
      responses:
        200:
          description: List of sessions
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Session'
    
    post:
      summary: Create new session
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                transcript:
                  type: string
                  format: binary
                session_type:
                  type: string
                session_date:
                  type: string
                  format: date
      responses:
        201:
          description: Session created
          
  /sessions/{id}/summaries:
    get:
      summary: Get session summaries
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        200:
          description: Session summaries
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Summary'
                  
  /summaries/{id}/refine:
    post:
      summary: Refine summary via chat
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                command:
                  type: string
                context:
                  type: object
      responses:
        200:
          description: Refined summary
          
  /search:
    post:
      summary: Natural language search
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                filters:
                  type: object
      responses:
        200:
          description: Search results
          
components:
  schemas:
    Session:
      type: object
      properties:
        id:
          type: string
        coach_id:
          type: string
        session_date:
          type: string
          format: date
        session_type:
          type: string
        participant_count:
          type: integer
        processing_status:
          type: string
          
    Summary:
      type: object
      properties:
        id:
          type: string
        client_name:
          type: string
        wins:
          type: string
        challenges:
          type: string
        action_items:
          type: array
          items:
            type: string
        coach_recommendations:
          type: string
```
