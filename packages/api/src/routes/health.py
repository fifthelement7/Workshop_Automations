"""
Health check endpoint for API monitoring and database connectivity.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import Dict, Any, cast
import logging

from ..models.database import get_db
from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=Dict[str, Any])
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Health check endpoint that verifies database connectivity and system status.

    Returns:
        Dict containing health status, database connectivity, and system info
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "version": settings.version,
        "database": {"status": "unknown", "connection": False, "error": None},
        "system": {"api_name": settings.app_name, "environment": settings.environment},
    }

    # Test database connectivity
    try:
        # Simple database connectivity test
        result = db.execute(text("SELECT 1 as test"))
        test_value = result.scalar()

        db_status = cast(Dict[str, Any], health_status["database"])
        if test_value == 1:
            db_status["status"] = "healthy"
            db_status["connection"] = True
            logger.info("Database connectivity check passed")
        else:
            db_status["status"] = "unhealthy"
            db_status["error"] = "Unexpected result"
            health_status["status"] = "degraded"
            logger.warning("Database connectivity check returned unexpected result")

    except Exception as e:
        health_status["status"] = "unhealthy"
        db_status = cast(Dict[str, Any], health_status["database"])
        db_status["status"] = "unhealthy"
        db_status["connection"] = False
        db_status["error"] = str(e)
        logger.error(f"Database connectivity check failed: {e}")

        # Return 503 Service Unavailable if database is down
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Service temporarily unavailable - database failed",
                "timestamp": datetime.utcnow().isoformat(),
                "database_error": str(e),
            },
        )

    return health_status


@router.get("/health/simple")
async def simple_health_check() -> Dict[str, str]:
    """
    Simple health check endpoint without database dependency.
    Useful for basic uptime monitoring.
    """
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
