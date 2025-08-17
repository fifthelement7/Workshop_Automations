"""
Simple unit tests without database dependency for verification.
"""
import pytest
import os
from unittest.mock import Mock, patch

# Set environment before importing
os.environ["ENVIRONMENT"] = "testing"
os.environ["DATABASE_URL"] = "postgresql://test:test@test:5432/test"
os.environ["SECRET_KEY"] = "test-secret"

from src.config import get_settings


def test_config_loading():
    """Test that configuration loads properly."""
    settings = get_settings()
    assert settings.environment == "testing"
    assert settings.app_name == "Mindscribe API"
    assert settings.version == "1.0.0"


def test_config_environment_specific():
    """Test environment-specific configuration."""
    with patch.dict(os.environ, {"ENVIRONMENT": "development"}):
        dev_settings = get_settings()
        assert dev_settings.environment == "development"
        assert dev_settings.log_level == "DEBUG"
    
    with patch.dict(os.environ, {"ENVIRONMENT": "production"}):
        prod_settings = get_settings()
        assert prod_settings.environment == "production"
        assert prod_settings.log_level == "WARNING"


def test_simple_health_endpoint():
    """Test the simple health endpoint logic."""
    from src.routes.health import simple_health_check
    import asyncio
    
    async def run_test():
        response = await simple_health_check()
        assert response["status"] == "ok"
        assert "timestamp" in response
    
    asyncio.run(run_test())


def test_database_models_import():
    """Test that database models can be imported without errors."""
    from src.models.core import Organization, Coach, Session, Client
    
    # Verify classes exist
    assert Organization.__tablename__ == "organizations"
    assert Coach.__tablename__ == "coaches"
    assert Session.__tablename__ == "sessions"
    assert Client.__tablename__ == "clients"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])