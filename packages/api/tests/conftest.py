"""
Pytest configuration and fixtures for Mindscribe API tests.
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import os

# Set test environment
os.environ["ENVIRONMENT"] = "testing"

from src.models.database import Base, get_db
from src.main import app
from src.config import settings


@pytest.fixture(scope="session") 
def test_database_url():
    """Get test database URL from environment."""
    return os.getenv("DATABASE_TEST_URL", "postgresql://postgres:password@localhost:5432/mindscribe_test")


@pytest.fixture(scope="session")
def test_engine(test_database_url):
    """Create test database engine."""
    engine = create_engine(
        test_database_url,
        pool_pre_ping=True
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db_session(test_engine):
    """Create test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def override_get_db(test_db_session):
    """Override database dependency for testing."""
    def _override_get_db():
        try:
            yield test_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client(override_get_db):
    """Create test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_organization_data():
    """Sample organization data for testing."""
    return {
        "name": "Test Coaching Organization",
        "settings": {
            "timezone": "UTC",
            "notification_enabled": True
        }
    }


@pytest.fixture
def sample_coach_data():
    """Sample coach data for testing."""
    return {
        "name": "Test Coach",
        "email": "coach@example.com",
        "voice_profile": {
            "tone": "professional",
            "style": "supportive"
        },
        "notification_preferences": {
            "email": True,
            "push": False
        }
    }


@pytest.fixture
def sample_session_data():
    """Sample session data for testing."""
    return {
        "session_date": "2024-01-15T10:00:00",
        "session_type": "group_coaching",
        "duration_minutes": 60,
        "participant_count": 5,
        "session_metadata": {
            "workshop_type": "leadership",
            "topic": "team building"
        }
    }


# For async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()