"""
Unit tests for health check endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy.exc import DatabaseError

from src.main import app


class TestHealthEndpoints:
    """Test cases for health check endpoints."""
    
    def test_simple_health_check(self, client: TestClient):
        """Test simple health check endpoint without database dependency."""
        # Arrange & Act
        response = client.get("/health/simple")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
    
    def test_health_check_success(self, client: TestClient):
        """Test health check endpoint with successful database connection."""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"]["status"] == "healthy"
        assert data["database"]["connection"] is True
        assert data["database"]["error"] is None
        assert "timestamp" in data
        assert "environment" in data
        assert "version" in data
        assert "system" in data
    
    @patch('src.routes.health.get_db')
    def test_health_check_database_failure(self, mock_get_db, client: TestClient):
        """Test health check endpoint with database connection failure."""
        # Arrange
        mock_session = Mock()
        mock_session.execute.side_effect = DatabaseError("Connection failed", None, None)
        mock_get_db.return_value.__next__ = Mock(return_value=mock_session)
        
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 503
        data = response.json()
        assert "Service temporarily unavailable" in data["detail"]
    
    def test_health_check_response_structure(self, client: TestClient):
        """Test that health check response has correct structure."""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Verify top-level structure
        required_fields = ["status", "timestamp", "environment", "version", "database", "system"]
        for field in required_fields:
            assert field in data
        
        # Verify database structure
        db_fields = ["status", "connection", "error"]
        for field in db_fields:
            assert field in data["database"]
        
        # Verify system structure
        system_fields = ["api_name", "environment"]
        for field in system_fields:
            assert field in data["system"]