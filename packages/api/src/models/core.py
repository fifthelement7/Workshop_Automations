"""
Core database models for Mindscribe platform.
"""

# Type annotations for SQLAlchemy columns
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Text,
    Boolean,
    DECIMAL,
    ForeignKey,
    ARRAY,
    UniqueConstraint,
    Index,
    Date,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    settings = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    coaches = relationship("Coach", back_populates="organization")
    clients = relationship("Client", back_populates="organization")


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )
    voice_profile = Column(JSONB)
    notification_preferences = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    organization = relationship("Organization", back_populates="coaches")
    sessions = relationship("Session", back_populates="coach")
    templates = relationship("Template", back_populates="coach")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coaches.id"), nullable=False)
    session_date = Column(Date, nullable=False)
    session_type = Column(String)
    transcript_url = Column(Text)
    duration_minutes = Column(Integer)
    participant_count = Column(Integer)
    processing_status = Column(String, default="pending")
    session_metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    coach = relationship("Coach", back_populates="sessions")
    client_sessions = relationship("ClientSession", back_populates="session")

    # Indexes
    __table_args__ = (
        Index("idx_sessions_coach_date", "coach_id", "session_date"),
        Index("idx_sessions_processing", "processing_status"),
    )


class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String)
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )
    tags = Column(ARRAY(Text))  # type: ignore
    engagement_score = Column(DECIMAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="clients")
    client_sessions = relationship("ClientSession", back_populates="client")
    follow_ups = relationship("FollowUp", back_populates="client")

    # Indexes
    __table_args__ = (Index("idx_clients_org", "organization_id"),)


class ClientSession(Base):
    __tablename__ = "client_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    speaking_time_seconds = Column(Integer)
    engagement_level = Column(String)
    breakthrough_detected = Column(Boolean)
    priority_score = Column(DECIMAL)

    # Relationships
    client = relationship("Client", back_populates="client_sessions")
    session = relationship("Session", back_populates="client_sessions")
    summaries = relationship("Summary", back_populates="client_session")

    # Constraints
    __table_args__ = (UniqueConstraint("client_id", "session_id"),)


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_session_id = Column(
        UUID(as_uuid=True), ForeignKey("client_sessions.id"), nullable=False
    )
    wins = Column(Text)
    challenges = Column(Text)
    action_items = Column(JSONB)
    coach_recommendations = Column(Text)
    ai_version = Column(Text)
    coach_edited_version = Column(Text)
    refinement_history = Column(JSONB)
    approved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    search_vector = Column(Text)  # For full-text search

    # Relationships
    client_session = relationship("ClientSession", back_populates="summaries")
    follow_ups = relationship("FollowUp", back_populates="summary")

    # Indexes
    __table_args__ = (
        Index(
            "idx_summaries_approved",
            "approved_at",
            postgresql_where="approved_at IS NOT NULL",
        ),
        Index("idx_summaries_search", "search_vector", postgresql_using="gin"),
    )


class Template(Base):
    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String)
    workshop_type = Column(String)
    content = Column(Text)
    variables = Column(ARRAY(Text))  # type: ignore
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coaches.id"), nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    coach = relationship("Coach", back_populates="templates")
    follow_ups = relationship("FollowUp", back_populates="template")


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summary_id = Column(UUID(as_uuid=True), ForeignKey("summaries.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    subject = Column(String)
    body = Column(Text)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"))
    status = Column(String, default="draft")
    sent_at = Column(DateTime(timezone=True))
    scheduled_for = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    summary = relationship("Summary", back_populates="follow_ups")
    client = relationship("Client", back_populates="follow_ups")
    template = relationship("Template", back_populates="follow_ups")

    # Indexes
    __table_args__ = (Index("idx_follow_ups_status", "status"),)
