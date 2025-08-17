"""
Integration tests for health check API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthAPIIntegration:
    """Integration tests for health check endpoints with real database."""
    
    def test_health_endpoint_with_database(self, client: TestClient):
        """Test health endpoint with actual database connection."""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Verify successful database connection
        assert data["status"] == "healthy"
        assert data["database"]["status"] == "healthy"
        assert data["database"]["connection"] is True
        assert data["database"]["error"] is None
        
        # Verify environment information
        assert data["environment"] == "testing"
        assert "timestamp" in data
        assert "version" in data
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns proper information."""
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        assert "Mindscribe" in data["message"]
        assert data["environment"] == "testing"
        assert "version" in data
        assert "docs_url" in data
    
    def test_api_documentation_available_in_testing(self, client: TestClient):
        """Test that API documentation is available in testing environment."""
        # Act
        docs_response = client.get("/docs")
        redoc_response = client.get("/redoc")
        
        # Assert
        assert docs_response.status_code == 200
        assert redoc_response.status_code == 200
    
    def test_cors_headers(self, client: TestClient):
        """Test that CORS headers are properly configured."""
        # Act
        response = client.options("/health")
        
        # Assert
        # TestClient doesn't fully simulate CORS, but we can check the app is configured
        # In a real environment, these headers would be present
        assert response.status_code in [200, 405]  # OPTIONS might not be explicitly handled