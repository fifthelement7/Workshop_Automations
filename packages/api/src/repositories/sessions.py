"""
Repository for session data access operations.
"""

from datetime import date
from typing import Optional, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.core import Session as SessionModel
from ..schemas.sessions import SessionUploadRequest


class SessionRepository:
    """Repository for session database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_session(
        self,
        coach_id: UUID,
        transcript_text: str,
        session_date: date,
        session_type: Optional[str] = None,
        duration_minutes: Optional[int] = None,
        participant_count: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> SessionModel:
        """
        Create a new session record.
        
        Args:
            coach_id: ID of the coach conducting the session
            transcript_text: Full transcript text
            session_date: Date the session occurred
            session_type: Type of session (optional)
            duration_minutes: Session duration (optional)
            participant_count: Number of participants (optional)
            notes: Additional notes (optional)
            
        Returns:
            Created session model
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # Prepare metadata
            metadata = {}
            if notes:
                metadata['notes'] = notes
            if transcript_text:
                metadata['transcript_text'] = transcript_text
            
            # Create session model
            session = SessionModel(
                coach_id=coach_id,
                session_date=session_date,
                session_type=session_type,
                duration_minutes=duration_minutes,
                participant_count=participant_count,
                processing_status="uploaded",
                session_metadata=metadata,
            )
            
            self.db.add(session)
            self.db.flush()  # Get the ID without committing
            
            return session
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_session_by_id(self, session_id: UUID) -> Optional[SessionModel]:
        """
        Retrieve a session by its ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session model or None if not found
        """
        return self.db.query(SessionModel).filter(
            SessionModel.id == session_id
        ).first()
    
    def update_processing_status(
        self,
        session_id: UUID,
        status: str
    ) -> bool:
        """
        Update the processing status of a session.
        
        Args:
            session_id: Session identifier
            status: New processing status
            
        Returns:
            True if update succeeded, False otherwise
        """
        try:
            result = self.db.query(SessionModel).filter(
                SessionModel.id == session_id
            ).update({"processing_status": status})
            
            return result > 0
            
        except SQLAlchemyError:
            self.db.rollback()
            return False
    
    def get_sessions_by_coach(
        self,
        coach_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> list[SessionModel]:
        """
        Get sessions for a specific coach.
        
        Args:
            coach_id: Coach identifier
            limit: Maximum number of sessions to return
            offset: Number of sessions to skip
            
        Returns:
            List of session models
        """
        return (
            self.db.query(SessionModel)
            .filter(SessionModel.coach_id == coach_id)
            .order_by(SessionModel.session_date.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )