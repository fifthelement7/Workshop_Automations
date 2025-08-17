"""
Repository for client data access operations.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, func

from ..models.core import Client, ClientSession, Organization


class ClientRepository:
    """Repository for client database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_or_create_client(
        self,
        name: str,
        organization_id: UUID,
        email: Optional[str] = None,
    ) -> tuple[Client, bool]:
        """
        Find existing client by name or create a new one.
        
        Args:
            name: Client's name
            organization_id: Organization the client belongs to
            email: Client's email (optional)
            
        Returns:
            Tuple of (client_model, was_created)
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # First, try to find existing client by exact name match
            existing_client = self._find_client_by_name(name, organization_id)
            
            if existing_client:
                return existing_client, False
            
            # Try fuzzy matching if no exact match
            fuzzy_client = self._find_client_fuzzy(name, organization_id)
            if fuzzy_client:
                return fuzzy_client, False
            
            # Create new client if no match found
            new_client = self._create_new_client(name, organization_id, email)
            return new_client, True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def _find_client_by_name(
        self,
        name: str,
        organization_id: UUID
    ) -> Optional[Client]:
        """Find client by exact name match."""
        return (
            self.db.query(Client)
            .filter(
                Client.name.ilike(name.strip()),  # Case-insensitive exact match
                Client.organization_id == organization_id
            )
            .first()
        )
    
    def _find_client_fuzzy(
        self,
        name: str,
        organization_id: UUID,
        similarity_threshold: float = 0.8
    ) -> Optional[Client]:
        """
        Find client using fuzzy matching on name.
        
        Args:
            name: Name to search for
            organization_id: Organization scope
            similarity_threshold: Minimum similarity score (0-1)
            
        Returns:
            Best matching client or None
        """
        # Normalize the search name
        normalized_search = self._normalize_name(name)
        
        # Get all clients in the organization
        clients = (
            self.db.query(Client)
            .filter(Client.organization_id == organization_id)
            .all()
        )
        
        best_match = None
        best_score = 0.0
        
        for client in clients:
            normalized_client = self._normalize_name(client.name)
            score = self._calculate_name_similarity(normalized_search, normalized_client)
            
            if score >= similarity_threshold and score > best_score:
                best_match = client
                best_score = score
        
        return best_match
    
    def _normalize_name(self, name: str) -> str:
        """Normalize name for comparison."""
        import re
        
        # Convert to lowercase, remove extra spaces
        normalized = re.sub(r'\s+', ' ', name.lower().strip())
        
        # Remove common prefixes/suffixes
        normalized = re.sub(r'^(mr|mrs|ms|dr|prof)\.?\s*', '', normalized)
        normalized = re.sub(r'\s*(jr|sr|ii|iii|iv)\.?$', '', normalized)
        
        return normalized
    
    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """
        Calculate similarity between two names using simple string matching.
        
        Returns:
            Similarity score between 0 and 1
        """
        # Simple implementation - can be enhanced with more sophisticated algorithms
        if name1 == name2:
            return 1.0
        
        # Check if one name is contained in the other
        if name1 in name2 or name2 in name1:
            return 0.9
        
        # Split into words and check overlap
        words1 = set(name1.split())
        words2 = set(name2.split())
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _create_new_client(
        self,
        name: str,
        organization_id: UUID,
        email: Optional[str] = None
    ) -> Client:
        """Create a new client record."""
        client = Client(
            name=name.strip(),
            email=email,
            organization_id=organization_id,
            engagement_score=0.0,  # Default engagement score
        )
        
        self.db.add(client)
        self.db.flush()  # Get the ID without committing
        
        return client
    
    def get_client_by_id(self, client_id: UUID) -> Optional[Client]:
        """Get client by ID."""
        return self.db.query(Client).filter(Client.id == client_id).first()
    
    def search_clients_by_name(
        self,
        name_query: str,
        organization_id: UUID,
        limit: int = 10
    ) -> List[Client]:
        """
        Search clients by name pattern.
        
        Args:
            name_query: Name search query
            organization_id: Organization scope
            limit: Maximum results to return
            
        Returns:
            List of matching clients
        """
        return (
            self.db.query(Client)
            .filter(
                Client.organization_id == organization_id,
                Client.name.ilike(f"%{name_query}%")
            )
            .limit(limit)
            .all()
        )


class ClientSessionRepository:
    """Repository for client-session relationship operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_client_session(
        self,
        client_id: UUID,
        session_id: UUID,
        speaking_time_seconds: Optional[int] = None,
        engagement_level: Optional[str] = None,
    ) -> ClientSession:
        """
        Create a client-session relationship.
        
        Args:
            client_id: Client identifier
            session_id: Session identifier
            speaking_time_seconds: Time client spoke (optional)
            engagement_level: Client's engagement level (optional)
            
        Returns:
            Created ClientSession model
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            client_session = ClientSession(
                client_id=client_id,
                session_id=session_id,
                speaking_time_seconds=speaking_time_seconds,
                engagement_level=engagement_level,
                breakthrough_detected=False,  # Default value
                priority_score=0.0,  # Default value
            )
            
            self.db.add(client_session)
            self.db.flush()
            
            return client_session
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_client_sessions_for_session(
        self,
        session_id: UUID
    ) -> List[ClientSession]:
        """Get all client sessions for a specific session."""
        return (
            self.db.query(ClientSession)
            .filter(ClientSession.session_id == session_id)
            .all()
        )
    
    def get_client_sessions_for_client(
        self,
        client_id: UUID,
        limit: int = 50
    ) -> List[ClientSession]:
        """Get all sessions for a specific client."""
        return (
            self.db.query(ClientSession)
            .filter(ClientSession.client_id == client_id)
            .limit(limit)
            .all()
        )