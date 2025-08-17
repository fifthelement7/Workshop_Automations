"""
Integration tests for complete upload workflow.
"""

import pytest
import tempfile
import os
from datetime import date
from uuid import UUID
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.database import Base, get_db
from src.models.core import Coach, Organization, Session as SessionModel, Client


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Create test database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_organization(test_db):
    """Create a sample organization for testing."""
    db = TestingSessionLocal()
    try:
        org = Organization(name="Test Organization")
        db.add(org)
        db.commit()
        db.refresh(org)
        return org
    finally:
        db.close()


@pytest.fixture
def sample_coach(test_db, sample_organization):
    """Create a sample coach for testing."""
    db = TestingSessionLocal()
    try:
        coach = Coach(
            email="test.coach@example.com",
            name="Test Coach",
            organization_id=sample_organization.id
        )
        db.add(coach)
        db.commit()
        db.refresh(coach)
        return coach
    finally:
        db.close()


class TestCompleteUploadWorkflow:
    """Integration tests for the complete upload workflow."""

    def test_text_upload_complete_workflow(self, test_db, sample_coach, sample_organization):
        """Test complete workflow for text upload with database integration."""
        
        # Mock the temporary coach/org IDs in routes
        with patch('src.routes.sessions.TEMP_COACH_ID', sample_coach.id), \
             patch('src.routes.sessions.TEMP_ORGANIZATION_ID', sample_organization.id):
            
            # Prepare test data
            transcript_text = """
            Coach Jennifer: Welcome to today's session, Sarah. How are you feeling?
            
            Sarah Thompson: I'm doing well, thank you. I've been reflecting on our last conversation.
            
            Coach Jennifer: That's wonderful to hear. What insights came up for you?
            
            Sarah Thompson: I realized I need to be more assertive in my communication at work.
            
            Coach Jennifer: That's a powerful realization. Can you give me a specific example?
            
            Sarah Thompson: Yes, in team meetings I often hold back my ideas because I worry about criticism.
            
            Coach Jennifer: What would it look like if you shared your ideas more freely?
            """
            
            upload_data = {
                "transcript_text": transcript_text,
                "session_date": "2024-01-15",
                "session_type": "individual",
                "duration_minutes": 60,
                "notes": "Initial coaching session focused on communication skills"
            }
            
            # Make the upload request
            response = client.post("/api/v1/sessions/upload", json=upload_data)
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            
            assert "session_id" in data
            assert data["status"] == "uploaded"
            assert data["processing_status"] == "pending"
            assert "Jennifer" in data["participants_identified"]
            assert "Sarah Thompson" in data["participants_identified"]
            
            # Verify database records were created
            db = TestingSessionLocal()
            try:
                # Check session was created
                session = db.query(SessionModel).filter(
                    SessionModel.id == data["session_id"]
                ).first()
                
                assert session is not None
                assert session.coach_id == sample_coach.id
                assert session.session_date == date(2024, 1, 15)
                assert session.session_type == "individual"
                assert session.duration_minutes == 60
                assert session.processing_status == "uploaded"
                assert "notes" in session.session_metadata
                
                # Check client was created
                clients = db.query(Client).filter(
                    Client.organization_id == sample_organization.id
                ).all()
                
                assert len(clients) >= 1
                client_names = [c.name for c in clients]
                assert "Sarah Thompson" in client_names
                
            finally:
                db.close()

    def test_file_upload_complete_workflow(self, test_db, sample_coach, sample_organization):
        """Test complete workflow for file upload with database integration."""
        
        # Create test transcript file
        transcript_content = """
        Coach Maria: Good morning, Alex. How has your week been?
        
        Alex Johnson: Morning, Maria. It's been quite eventful actually.
        
        Coach Maria: I'd love to hear about that. What made it eventful?
        
        Alex Johnson: I had a presentation at work and I applied some of the techniques we discussed.
        
        Coach Maria: That's fantastic! How did it go?
        
        Alex Johnson: Better than expected. I felt more confident and prepared.
        
        Coach Maria: What specifically helped you feel more confident?
        
        Alex Johnson: The visualization exercise we practiced and the preparation framework.
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(transcript_content)
            temp_file_path = f.name
        
        try:
            # Mock the temporary coach/org IDs
            with patch('src.routes.sessions.TEMP_COACH_ID', sample_coach.id), \
                 patch('src.routes.sessions.TEMP_ORGANIZATION_ID', sample_organization.id):
                
                # Make the file upload request
                with open(temp_file_path, 'rb') as file:
                    response = client.post(
                        "/api/v1/sessions/upload-file",
                        files={"file": ("session_transcript.txt", file, "text/plain")},
                        data={
                            "session_date": "2024-01-20",
                            "session_type": "individual",
                            "notes": "Follow-up session on presentation skills"
                        }
                    )
                
                # Verify response
                assert response.status_code == 200
                data = response.json()
                
                assert "session_id" in data
                assert data["status"] == "uploaded"
                assert "Maria" in data["participants_identified"]
                assert "Alex Johnson" in data["participants_identified"]
                
                # Verify database state
                db = TestingSessionLocal()
                try:
                    session = db.query(SessionModel).filter(
                        SessionModel.id == data["session_id"]
                    ).first()
                    
                    assert session is not None
                    assert session.session_date == date(2024, 1, 20)
                    assert "transcript_text" in session.session_metadata
                    
                    # Verify client creation
                    alex_client = db.query(Client).filter(
                        Client.name == "Alex Johnson"
                    ).first()
                    
                    assert alex_client is not None
                    assert alex_client.organization_id == sample_organization.id
                    
                finally:
                    db.close()
        
        finally:
            os.unlink(temp_file_path)

    def test_duplicate_client_handling(self, test_db, sample_coach, sample_organization):
        """Test that duplicate clients are handled correctly."""
        
        # First, create a client manually
        db = TestingSessionLocal()
        try:
            existing_client = Client(
                name="John Smith",
                organization_id=sample_organization.id,
                email="john.smith@example.com"
            )
            db.add(existing_client)
            db.commit()
            existing_client_id = existing_client.id
        finally:
            db.close()
        
        # Now upload a session with the same client
        transcript_text = """
        Coach Lisa: Hello John, ready for today's session?
        
        John Smith: Yes, I'm excited to continue our work on leadership.
        
        Coach Lisa: Great! Let's pick up where we left off last week.
        """
        
        with patch('src.routes.sessions.TEMP_COACH_ID', sample_coach.id), \
             patch('src.routes.sessions.TEMP_ORGANIZATION_ID', sample_organization.id):
            
            upload_data = {
                "transcript_text": transcript_text,
                "session_date": "2024-01-25",
                "session_type": "individual"
            }
            
            response = client.post("/api/v1/sessions/upload", json=upload_data)
            
            assert response.status_code == 200
            data = response.json()
            
            # Should match existing client, not create new one
            assert "John Smith" in data["clients_matched"]
            assert "John Smith" not in data["clients_created"]
            
            # Verify only one John Smith exists in database
            db = TestingSessionLocal()
            try:
                john_clients = db.query(Client).filter(
                    Client.name == "John Smith"
                ).all()
                
                assert len(john_clients) == 1
                assert john_clients[0].id == existing_client_id
                
            finally:
                db.close()

    def test_session_retrieval_after_upload(self, test_db, sample_coach, sample_organization):
        """Test that uploaded session can be retrieved correctly."""
        
        transcript_text = """
        Coach Emma: How are you progressing with your goals, David?
        
        David Wilson: I've made some good progress on the time management front.
        
        Coach Emma: That's excellent. Can you share some specifics?
        """
        
        with patch('src.routes.sessions.TEMP_COACH_ID', sample_coach.id), \
             patch('src.routes.sessions.TEMP_ORGANIZATION_ID', sample_organization.id):
            
            # Upload session
            upload_data = {
                "transcript_text": transcript_text,
                "session_date": "2024-02-01",
                "session_type": "individual",
                "duration_minutes": 45
            }
            
            upload_response = client.post("/api/v1/sessions/upload", json=upload_data)
            assert upload_response.status_code == 200
            
            session_id = upload_response.json()["session_id"]
            
            # Retrieve session
            get_response = client.get(f"/api/v1/sessions/{session_id}")
            assert get_response.status_code == 200
            
            session_data = get_response.json()
            
            # Verify session details
            assert session_data["session"]["id"] == session_id
            assert session_data["session"]["session_type"] == "individual"
            assert session_data["session"]["duration_minutes"] == 45
            
            # Verify participants
            participant_names = [p["name"] for p in session_data["participants"]]
            assert "David Wilson" in participant_names

    def test_error_handling_invalid_data(self, test_db):
        """Test error handling with invalid upload data."""
        
        # Test with transcript too short
        upload_data = {
            "transcript_text": "Too short",
            "session_date": "2024-01-15"
        }
        
        response = client.post("/api/v1/sessions/upload", json=upload_data)
        assert response.status_code == 422

    def test_error_handling_invalid_file(self, test_db):
        """Test error handling with invalid file upload."""
        
        # Create invalid file content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Short")  # Too short content
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as file:
                response = client.post(
                    "/api/v1/sessions/upload-file",
                    files={"file": ("short.txt", file, "text/plain")},
                    data={"session_date": "2024-01-15"}
                )
            
            assert response.status_code == 400
            
        finally:
            os.unlink(temp_file_path)