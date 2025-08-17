"""
Session management service for orchestrating upload workflow.
"""

from datetime import date
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from ..schemas.sessions import SessionUploadRequest, SessionUploadResponse
from ..repositories.sessions import SessionRepository
from ..repositories.clients import ClientRepository, ClientSessionRepository
from ..services.participant_extraction import ParticipantExtractor, ParticipantInfo
from ..models.core import Session as SessionModel, Client


class SessionManagementService:
    """Service for managing session upload and processing workflow."""
    
    def __init__(self, db: Session):
        self.db = db
        self.session_repo = SessionRepository(db)
        self.client_repo = ClientRepository(db)
        self.client_session_repo = ClientSessionRepository(db)
        self.participant_extractor = ParticipantExtractor()
    
    def create_session_from_upload(
        self,
        upload_request: SessionUploadRequest,
        coach_id: UUID,
        organization_id: UUID,
    ) -> SessionUploadResponse:
        """
        Create a session from upload request with full workflow.
        
        Args:
            upload_request: Session upload data
            coach_id: ID of the coach creating the session
            organization_id: Organization context
            
        Returns:
            SessionUploadResponse with session details
            
        Raises:
            HTTPException: If workflow fails
        """
        try:
            # Extract participants from transcript first (validation step)
            participants = self._extract_participants(upload_request)
            
            # Create the session record
            session = self._create_session_record(
                upload_request, coach_id, len(participants)
            )
            
            # Process participants and create client relationships
            client_results = self._process_participants(
                participants, session.id, organization_id
            )
            
            # Commit the transaction
            self.db.commit()
            
            # Build response
            response = SessionUploadResponse(
                session_id=session.id,
                status="uploaded",
                participants_identified=[p.name for p in participants],
                clients_created=client_results["created"],
                clients_matched=client_results["matched"],
                processing_status="pending",
                next_steps="Session ready for AI analysis"
            )
            
            return response
                
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error during session creation: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Failed to process session upload: {str(e)}"
            )
    
    def _extract_participants(
        self,
        upload_request: SessionUploadRequest
    ) -> List[ParticipantInfo]:
        """Extract participants from transcript or use provided list."""
        if upload_request.participants:
            # Use explicitly provided participants
            participants = []
            for name in upload_request.participants:
                participants.append(ParticipantInfo(name=name.strip()))
            return participants
        else:
            # Extract from transcript text
            return self.participant_extractor.extract_participants(
                upload_request.transcript_text
            )
    
    def _create_session_record(
        self,
        upload_request: SessionUploadRequest,
        coach_id: UUID,
        participant_count: int,
    ) -> SessionModel:
        """Create the main session database record."""
        return self.session_repo.create_session(
            coach_id=coach_id,
            transcript_text=upload_request.transcript_text,
            session_date=upload_request.session_date,
            session_type=upload_request.session_type,
            duration_minutes=upload_request.duration_minutes,
            participant_count=participant_count,
            notes=upload_request.notes,
        )
    
    def _process_participants(
        self,
        participants: List[ParticipantInfo],
        session_id: UUID,
        organization_id: UUID,
    ) -> Dict[str, List[str]]:
        """
        Process participants to create or match clients.
        
        Returns:
            Dictionary with 'created' and 'matched' client name lists
        """
        created_clients = []
        matched_clients = []
        
        for participant in participants:
            # Skip if this looks like the coach (basic heuristic)
            if participant.role == "coach":
                continue
            
            try:
                # Find or create client
                client, was_created = self.client_repo.find_or_create_client(
                    name=participant.name,
                    organization_id=organization_id,
                )
                
                # Create client-session relationship
                self.client_session_repo.create_client_session(
                    client_id=client.id,
                    session_id=session_id,
                    engagement_level="unknown",  # Default, will be analyzed later
                )
                
                # Track results
                if was_created:
                    created_clients.append(participant.name)
                else:
                    matched_clients.append(participant.name)
                    
            except Exception as e:
                # Log error but continue with other participants
                import logging
                logging.warning(f"Failed to process participant {participant.name}: {e}")
                continue
        
        return {
            "created": created_clients,
            "matched": matched_clients,
        }
    
    def get_session_with_participants(
        self,
        session_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """
        Get session details with participant information.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with session and participant details
        """
        session = self.session_repo.get_session_by_id(session_id)
        if not session:
            return None
        
        # Get client sessions
        client_sessions = self.client_session_repo.get_client_sessions_for_session(session_id)
        
        # Build participant list
        participants = []
        for cs in client_sessions:
            client = self.client_repo.get_client_by_id(cs.client_id)
            if client:
                participants.append({
                    "name": client.name,
                    "email": client.email,
                    "engagement_level": cs.engagement_level,
                    "speaking_time_seconds": cs.speaking_time_seconds,
                })
        
        return {
            "session": {
                "id": session.id,
                "session_date": session.session_date.isoformat(),
                "session_type": session.session_type,
                "duration_minutes": session.duration_minutes,
                "processing_status": session.processing_status,
                "participant_count": session.participant_count,
                "created_at": session.created_at.isoformat(),
            },
            "participants": participants,
        }
    
    def update_session_status(
        self,
        session_id: UUID,
        status: str
    ) -> bool:
        """Update session processing status."""
        return self.session_repo.update_processing_status(session_id, status)