"""
Pydantic schemas for session upload endpoints.
"""

from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class SessionUploadRequest(BaseModel):
    """Schema for text-based session upload."""
    
    transcript_text: str = Field(
        ...,
        min_length=100,
        description="Session transcript text content"
    )
    session_date: date = Field(
        ...,
        description="Date when the session occurred"
    )
    session_type: Optional[str] = Field(
        None,
        description="Type of session (e.g., 'individual', 'group', 'workshop')"
    )
    participants: Optional[List[str]] = Field(
        None,
        description="List of participant names (extracted automatically if not provided)"
    )
    duration_minutes: Optional[int] = Field(
        None,
        ge=1,
        le=480,  # 8 hours max
        description="Session duration in minutes"
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional session context or notes"
    )

    @validator('transcript_text')
    def validate_transcript_length(cls, v):
        if len(v) > 1_000_000:  # 1MB max text content
            raise ValueError('Transcript text too long (max 1MB)')
        return v


class SessionUploadResponse(BaseModel):
    """Schema for successful session upload response."""
    
    session_id: UUID = Field(
        ...,
        description="Unique identifier for the created session"
    )
    status: str = Field(
        ...,
        description="Upload status (e.g., 'uploaded')"
    )
    participants_identified: List[str] = Field(
        ...,
        description="List of participants identified in the transcript"
    )
    clients_created: List[str] = Field(
        ...,
        description="List of new clients created from participants"
    )
    clients_matched: List[str] = Field(
        ...,
        description="List of existing clients matched to participants"
    )
    processing_status: str = Field(
        ...,
        description="Current processing status of the session"
    )
    next_steps: str = Field(
        ...,
        description="Description of what happens next in the workflow"
    )


class FileUploadMetadata(BaseModel):
    """Schema for file upload metadata."""
    
    session_date: date = Field(
        ...,
        description="Date when the session occurred"
    )
    session_type: Optional[str] = Field(
        None,
        description="Type of session (e.g., 'individual', 'group', 'workshop')"
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional session context or notes"
    )


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    
    error: str = Field(
        ...,
        description="Error type or category"
    )
    detail: str = Field(
        ...,
        description="Detailed error message"
    )
    code: Optional[str] = Field(
        None,
        description="Error code for client handling"
    )