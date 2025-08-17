"""
Session upload API endpoints.
"""

from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..models.database import get_db
from ..schemas.sessions import (
    SessionUploadRequest,
    SessionUploadResponse,
    FileUploadMetadata,
    ErrorResponse,
)
from ..services.session_management import SessionManagementService
from ..services.file_processing import FileProcessingService


router = APIRouter(prefix="/api/v1/sessions", tags=["Session Upload"])


# Temporary coach ID for testing - will be replaced with authentication
# TODO: Replace with proper authentication middleware
TEMP_COACH_ID = UUID("12345678-1234-5678-9abc-123456789012")  # Fixed UUID for consistency
TEMP_ORGANIZATION_ID = UUID("87654321-4321-8765-cba9-876543210987")  # Fixed UUID for consistency


@router.post(
    "/upload",
    response_model=SessionUploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        422: {"model": ErrorResponse, "description": "Processing failed"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Upload session transcript text",
    description="Upload a session transcript as text with metadata for processing.",
)
async def upload_session_text(
    upload_request: SessionUploadRequest,
    db: Annotated[Session, Depends(get_db)],
) -> SessionUploadResponse:
    """
    Upload session transcript as text content.
    
    This endpoint accepts session transcript text directly along with metadata
    such as session date, type, and optional participant information.
    """
    try:
        service = SessionManagementService(db)
        
        response = service.create_session_from_upload(
            upload_request=upload_request,
            coach_id=TEMP_COACH_ID,
            organization_id=TEMP_ORGANIZATION_ID,
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during session upload: {str(e)}"
        )


@router.post(
    "/upload-file",
    response_model=SessionUploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file or metadata"},
        413: {"model": ErrorResponse, "description": "File too large"},
        422: {"model": ErrorResponse, "description": "File processing failed"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Upload session transcript file",
    description="Upload a session transcript file (.txt or .docx) with metadata.",
)
async def upload_session_file(
    db: Annotated[Session, Depends(get_db)],
    file: Annotated[UploadFile, File(description="Transcript file (.txt or .docx, max 10MB)")],
    session_date: Annotated[str, Form(description="Session date (YYYY-MM-DD)")],
    session_type: Annotated[str, Form(description="Session type")] = None,
    notes: Annotated[str, Form(description="Additional notes")] = None,
) -> SessionUploadResponse:
    """
    Upload session transcript as a file.
    
    This endpoint accepts .txt or .docx files containing session transcripts.
    File content is extracted and processed the same way as text uploads.
    """
    try:
        # Process the uploaded file
        transcript_text = await FileProcessingService.process_uploaded_file(file)
        
        # Parse and validate the session date
        from datetime import datetime
        try:
            parsed_date = datetime.strptime(session_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD format."
            )
        
        # Create upload request object
        upload_request = SessionUploadRequest(
            transcript_text=transcript_text,
            session_date=parsed_date,
            session_type=session_type,
            notes=notes,
        )
        
        # Process through session management service
        service = SessionManagementService(db)
        
        response = service.create_session_from_upload(
            upload_request=upload_request,
            coach_id=TEMP_COACH_ID,
            organization_id=TEMP_ORGANIZATION_ID,
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during file upload: {str(e)}"
        )


@router.get(
    "/{session_id}",
    summary="Get session details",
    description="Retrieve session details with participant information.",
)
async def get_session(
    session_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):
    """Get session details by ID."""
    try:
        service = SessionManagementService(db)
        session_data = service.get_session_with_participants(session_id)
        
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )
        
        return session_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving session: {str(e)}"
        )


@router.patch(
    "/{session_id}/status",
    summary="Update session status",
    description="Update the processing status of a session.",
)
async def update_session_status(
    session_id: UUID,
    status: str,
    db: Annotated[Session, Depends(get_db)],
):
    """Update session processing status."""
    try:
        service = SessionManagementService(db)
        success = service.update_session_status(session_id, status)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Session not found or update failed"
            )
        
        return {"session_id": session_id, "status": status, "updated": True}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating session status: {str(e)}"
        )