"""
Pydantic schemas for client management.
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ClientCreate(BaseModel):
    """Schema for creating a new client."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Client's full name"
    )
    email: Optional[str] = Field(
        None,
        description="Client's email address"
    )
    organization_id: Optional[UUID] = Field(
        None,
        description="Organization the client belongs to"
    )
    tags: Optional[str] = Field(
        None,
        description="JSON string of client tags"
    )


class ClientResponse(BaseModel):
    """Schema for client data in responses."""
    
    id: UUID = Field(
        ...,
        description="Unique identifier for the client"
    )
    name: str = Field(
        ...,
        description="Client's full name"
    )
    email: Optional[str] = Field(
        None,
        description="Client's email address"
    )
    organization_id: Optional[UUID] = Field(
        None,
        description="Organization the client belongs to"
    )
    engagement_score: Optional[float] = Field(
        None,
        description="Client's engagement score"
    )
    created_at: str = Field(
        ...,
        description="Timestamp when client was created"
    )

    class Config:
        from_attributes = True


class ClientSessionCreate(BaseModel):
    """Schema for creating a client-session relationship."""
    
    client_id: UUID = Field(
        ...,
        description="Client identifier"
    )
    session_id: UUID = Field(
        ...,
        description="Session identifier"
    )
    speaking_time_seconds: Optional[int] = Field(
        None,
        ge=0,
        description="Time client spent speaking in seconds"
    )
    engagement_level: Optional[str] = Field(
        None,
        description="Client's engagement level in the session"
    )