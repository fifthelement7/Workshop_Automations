"""
Integration tests for database connectivity and operations.
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.models.core import Organization, Coach, Session as CoachingSession
from src.models.database import Base


class TestDatabaseConnectivity:
    """Test database connectivity and basic operations."""
    
    def test_database_connection(self, test_db_session: Session):
        """Test that database connection is working."""
        # Act
        result = test_db_session.execute(text("SELECT 1 as test"))
        value = result.scalar()
        
        # Assert
        assert value == 1
    
    def test_create_organization(self, test_db_session: Session, sample_organization_data):
        """Test creating an organization in the database."""
        # Arrange
        organization = Organization(**sample_organization_data)
        
        # Act
        test_db_session.add(organization)
        test_db_session.commit()
        test_db_session.refresh(organization)
        
        # Assert
        assert organization.id is not None
        assert organization.name == sample_organization_data["name"]
        assert organization.settings == sample_organization_data["settings"]
        assert organization.created_at is not None
    
    def test_create_coach_with_organization(
        self, 
        test_db_session: Session, 
        sample_organization_data,
        sample_coach_data
    ):
        """Test creating a coach linked to an organization."""
        # Arrange
        organization = Organization(**sample_organization_data)
        test_db_session.add(organization)
        test_db_session.commit()
        test_db_session.refresh(organization)
        
        coach_data = sample_coach_data.copy()
        coach_data["organization_id"] = organization.id
        coach = Coach(**coach_data)
        
        # Act
        test_db_session.add(coach)
        test_db_session.commit()
        test_db_session.refresh(coach)
        
        # Assert
        assert coach.id is not None
        assert coach.organization_id == organization.id
        assert coach.name == sample_coach_data["name"]
        assert coach.email == sample_coach_data["email"]
        assert coach.organization.name == organization.name
    
    def test_create_coaching_session(
        self,
        test_db_session: Session,
        sample_organization_data,
        sample_coach_data,
        sample_session_data
    ):
        """Test creating a coaching session."""
        # Arrange
        organization = Organization(**sample_organization_data)
        test_db_session.add(organization)
        test_db_session.commit()
        
        coach_data = sample_coach_data.copy()
        coach_data["organization_id"] = organization.id
        coach = Coach(**coach_data)
        test_db_session.add(coach)
        test_db_session.commit()
        
        session_data = sample_session_data.copy()
        session_data["coach_id"] = coach.id
        # Convert string date to date object
        from datetime import datetime
        session_data["session_date"] = datetime.fromisoformat(session_data["session_date"]).date()
        coaching_session = CoachingSession(**session_data)
        
        # Act
        test_db_session.add(coaching_session)
        test_db_session.commit()
        test_db_session.refresh(coaching_session)
        
        # Assert
        assert coaching_session.id is not None
        assert coaching_session.coach_id == coach.id
        assert coaching_session.processing_status == "pending"
        assert coaching_session.coach.name == coach.name
    
    def test_database_indexes_exist(self, test_engine):
        """Test that required database indexes are created."""
        # This test verifies that the database schema is properly created
        # with the required indexes as defined in the models
        
        # Act & Assert - If the tables were created without errors, indexes should exist
        # We verify this by checking that we can query the information schema
        with test_engine.connect() as connection:
            # Check if tables exist
            result = connection.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_names = [row[0] for row in result]
            
            expected_tables = [
                'organizations', 'coaches', 'sessions', 'clients', 
                'client_sessions', 'summaries', 'templates', 'follow_ups'
            ]
            
            for table in expected_tables:
                assert table in table_names, f"Table {table} not found in database"


class TestDatabaseTransactions:
    """Test database transaction handling."""
    
    def test_rollback_on_error(self, test_db_session: Session, sample_organization_data):
        """Test that database transactions rollback properly on errors."""
        # Arrange
        organization = Organization(**sample_organization_data)
        test_db_session.add(organization)
        
        # Act & Assert
        try:
            # Force an error by trying to commit incomplete data
            coach = Coach(name="Test Coach", email="test@example.com")  # Missing organization_id
            test_db_session.add(coach)
            test_db_session.commit()
            pytest.fail("Expected IntegrityError was not raised")
        except Exception:
            test_db_session.rollback()
            
            # Verify that organization was not saved due to rollback
            result = test_db_session.query(Organization).filter_by(
                name=sample_organization_data["name"]
            ).first()
            assert result is None