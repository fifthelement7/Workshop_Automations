"""
Unit tests for session upload API endpoints.
"""

import pytest
import tempfile
import os
from datetime import date
from uuid import uuid4
from unittest.mock import Mock, patch, AsyncMock

from fastapi.testclient import TestClient
from fastapi import UploadFile

from src.main import app
from src.schemas.sessions import SessionUploadResponse


client = TestClient(app)


class TestSessionUploadTextEndpoint:
    """Test cases for POST /api/v1/sessions/upload endpoint."""

    def test_upload_session_text_success(self):
        """Test successful text upload with valid data."""
        
        # Mock the SessionManagementService
        with patch('src.routes.sessions.SessionManagementService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Mock successful response
            mock_response = SessionUploadResponse(
                session_id=uuid4(),
                status="uploaded",
                participants_identified=["John Doe", "Jane Smith"],
                clients_created=["John Doe"],
                clients_matched=["Jane Smith"],
                processing_status="pending",
                next_steps="Session ready for AI analysis"
            )
            mock_service.create_session_from_upload.return_value = mock_response
            
            # Test data
            upload_data = {
                "transcript_text": "A" * 200,  # Valid length
                "session_date": "2024-01-15",
                "session_type": "individual",
                "duration_minutes": 60,
                "notes": "Test session notes"
            }
            
            # Make request
            response = client.post("/api/v1/sessions/upload", json=upload_data)
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "uploaded"
            assert "session_id" in data
            assert data["participants_identified"] == ["John Doe", "Jane Smith"]
            assert data["clients_created"] == ["John Doe"]
            assert data["clients_matched"] == ["Jane Smith"]

    def test_upload_session_text_invalid_short_transcript(self):
        """Test upload fails with transcript too short."""
        
        upload_data = {
            "transcript_text": "Short",  # Too short
            "session_date": "2024-01-15",
        }
        
        response = client.post("/api/v1/sessions/upload", json=upload_data)
        
        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

    def test_upload_session_text_missing_required_fields(self):
        """Test upload fails with missing required fields."""
        
        upload_data = {
            "transcript_text": "A" * 200,
            # Missing session_date
        }
        
        response = client.post("/api/v1/sessions/upload", json=upload_data)
        
        assert response.status_code == 422

    def test_upload_session_text_invalid_date_format(self):
        """Test upload fails with invalid date format."""
        
        upload_data = {
            "transcript_text": "A" * 200,
            "session_date": "invalid-date",
        }
        
        response = client.post("/api/v1/sessions/upload", json=upload_data)
        
        assert response.status_code == 422

    def test_upload_session_text_service_error(self):
        """Test error handling when service fails."""
        
        with patch('src.routes.sessions.SessionManagementService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Mock service error
            mock_service.create_session_from_upload.side_effect = Exception("Service error")
            
            upload_data = {
                "transcript_text": "A" * 200,
                "session_date": "2024-01-15",
            }
            
            response = client.post("/api/v1/sessions/upload", json=upload_data)
            
            assert response.status_code == 500
            assert "error" in response.json()["detail"].lower()


class TestSessionUploadFileEndpoint:
    """Test cases for POST /api/v1/sessions/upload-file endpoint."""

    def test_upload_file_success_txt(self):
        """Test successful .txt file upload."""
        
        with patch('src.routes.sessions.FileProcessingService') as mock_file_service, \
             patch('src.routes.sessions.SessionManagementService') as mock_session_service:
            
            # Mock file processing
            mock_file_service.process_uploaded_file = AsyncMock(return_value="Processed transcript text")
            
            # Mock session service
            mock_service = Mock()
            mock_session_service.return_value = mock_service
            mock_response = SessionUploadResponse(
                session_id=uuid4(),
                status="uploaded",
                participants_identified=["John Doe"],
                clients_created=["John Doe"],
                clients_matched=[],
                processing_status="pending",
                next_steps="Session ready for AI analysis"
            )
            mock_service.create_session_from_upload.return_value = mock_response
            
            # Create test file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write("Test transcript content that is long enough to pass validation")
                temp_file_path = f.name
            
            try:
                # Make request
                with open(temp_file_path, 'rb') as file:
                    response = client.post(
                        "/api/v1/sessions/upload-file",
                        files={"file": ("test.txt", file, "text/plain")},
                        data={
                            "session_date": "2024-01-15",
                            "session_type": "individual",
                            "notes": "Test notes"
                        }
                    )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "uploaded"
                assert "session_id" in data
                
            finally:
                os.unlink(temp_file_path)

    def test_upload_file_missing_file(self):
        """Test upload fails when no file is provided."""
        
        response = client.post(
            "/api/v1/sessions/upload-file",
            data={"session_date": "2024-01-15"}
        )
        
        assert response.status_code == 422

    def test_upload_file_invalid_date(self):
        """Test upload fails with invalid date format."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as file:
                response = client.post(
                    "/api/v1/sessions/upload-file",
                    files={"file": ("test.txt", file, "text/plain")},
                    data={"session_date": "invalid-date"}
                )
            
            assert response.status_code == 400
            
        finally:
            os.unlink(temp_file_path)

    def test_upload_file_processing_error(self):
        """Test error handling when file processing fails."""
        
        with patch('src.routes.sessions.FileProcessingService') as mock_file_service:
            # Mock file processing error
            mock_file_service.process_uploaded_file = AsyncMock(
                side_effect=Exception("File processing error")
            )
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write("Test content")
                temp_file_path = f.name
            
            try:
                with open(temp_file_path, 'rb') as file:
                    response = client.post(
                        "/api/v1/sessions/upload-file",
                        files={"file": ("test.txt", file, "text/plain")},
                        data={"session_date": "2024-01-15"}
                    )
                
                assert response.status_code == 500
                
            finally:
                os.unlink(temp_file_path)


class TestGetSessionEndpoint:
    """Test cases for GET /api/v1/sessions/{session_id} endpoint."""

    def test_get_session_success(self):
        """Test successful session retrieval."""
        
        with patch('src.routes.sessions.SessionManagementService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Mock session data
            session_data = {
                "session": {
                    "id": str(uuid4()),
                    "session_date": "2024-01-15",
                    "session_type": "individual",
                    "processing_status": "completed",
                    "participant_count": 2,
                    "created_at": "2024-01-15T10:00:00Z"
                },
                "participants": [
                    {"name": "John Doe", "email": "john@example.com"},
                    {"name": "Jane Smith", "email": None}
                ]
            }
            mock_service.get_session_with_participants.return_value = session_data
            
            session_id = uuid4()
            response = client.get(f"/api/v1/sessions/{session_id}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["session"]["id"] == session_data["session"]["id"]
            assert len(data["participants"]) == 2

    def test_get_session_not_found(self):
        """Test session not found scenario."""
        
        with patch('src.routes.sessions.SessionManagementService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            mock_service.get_session_with_participants.return_value = None
            
            session_id = uuid4()
            response = client.get(f"/api/v1/sessions/{session_id}")
            
            assert response.status_code == 404
            assert "not found" in response.json()["detail"].lower()

    def test_get_session_invalid_uuid(self):
        """Test invalid UUID format."""
        
        response = client.get("/api/v1/sessions/invalid-uuid")
        
        assert response.status_code == 422


class TestUpdateSessionStatusEndpoint:
    """Test cases for PATCH /api/v1/sessions/{session_id}/status endpoint."""

    def test_update_status_success(self):
        """Test successful status update."""
        
        with patch('src.routes.sessions.SessionManagementService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            mock_service.update_session_status.return_value = True
            
            session_id = uuid4()
            response = client.patch(
                f"/api/v1/sessions/{session_id}/status",
                params={"status": "completed"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["updated"] is True
            assert data["status"] == "completed"

    def test_update_status_not_found(self):
        """Test status update for non-existent session."""
        
        with patch('src.routes.sessions.SessionManagementService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            mock_service.update_session_status.return_value = False
            
            session_id = uuid4()
            response = client.patch(
                f"/api/v1/sessions/{session_id}/status",
                params={"status": "completed"}
            )
            
            assert response.status_code == 404