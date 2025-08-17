"""
File processing service for handling uploaded transcript files.
"""

import os
import tempfile
from typing import Dict, Any
from pathlib import Path

import chardet
from docx import Document
from fastapi import UploadFile, HTTPException


class FileProcessingService:
    """Service for processing uploaded transcript files."""
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_TEXT_SIZE = 1 * 1024 * 1024   # 1MB text content
    SUPPORTED_EXTENSIONS = {'.txt', '.docx'}
    
    @classmethod
    async def process_uploaded_file(cls, file: UploadFile) -> str:
        """
        Process an uploaded file and extract text content.
        
        Args:
            file: FastAPI UploadFile object
            
        Returns:
            Extracted text content
            
        Raises:
            HTTPException: If file processing fails
        """
        # Validate file size
        await cls._validate_file_size(file)
        
        # Validate file extension
        file_extension = cls._get_file_extension(file.filename)
        cls._validate_file_extension(file_extension)
        
        # Process file based on type
        content = await cls._extract_text_content(file, file_extension)
        
        # Validate content size and format
        cls._validate_content(content)
        
        return content
    
    @classmethod
    async def _validate_file_size(cls, file: UploadFile) -> None:
        """Validate uploaded file size."""
        # Read file to check size
        content = await file.read()
        file_size = len(content)
        
        if file_size > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {cls.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Reset file pointer for further processing
        await file.seek(0)
    
    @classmethod
    def _get_file_extension(cls, filename: str) -> str:
        """Extract file extension from filename."""
        if not filename:
            raise HTTPException(
                status_code=400,
                detail="No filename provided"
            )
        
        return Path(filename).suffix.lower()
    
    @classmethod
    def _validate_file_extension(cls, extension: str) -> None:
        """Validate file extension is supported."""
        if extension not in cls.SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported formats: {', '.join(cls.SUPPORTED_EXTENSIONS)}"
            )
    
    @classmethod
    async def _extract_text_content(cls, file: UploadFile, extension: str) -> str:
        """Extract text content based on file type."""
        try:
            if extension == '.txt':
                return await cls._process_txt_file(file)
            elif extension == '.docx':
                return await cls._process_docx_file(file)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file extension: {extension}"
                )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=422,
                detail=f"Failed to process file: {str(e)}"
            )
    
    @classmethod
    async def _process_txt_file(cls, file: UploadFile) -> str:
        """Process .txt file with encoding detection."""
        content_bytes = await file.read()
        
        # Detect encoding
        detected = chardet.detect(content_bytes)
        encoding = detected.get('encoding', 'utf-8')
        
        try:
            content = content_bytes.decode(encoding)
        except UnicodeDecodeError:
            # Fallback to utf-8 with error handling
            content = content_bytes.decode('utf-8', errors='replace')
        
        return content.strip()
    
    @classmethod
    async def _process_docx_file(cls, file: UploadFile) -> str:
        """Process .docx file using python-docx."""
        content_bytes = await file.read()
        
        # Save to temporary file for processing
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_file.write(content_bytes)
            temp_file_path = temp_file.name
        
        try:
            # Read document
            doc = Document(temp_file_path)
            
            # Extract text from all paragraphs
            paragraphs = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text.strip())
            
            content = '\n'.join(paragraphs)
            return content
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass  # File already deleted or inaccessible
    
    @classmethod
    def _validate_content(cls, content: str) -> None:
        """Validate extracted content."""
        if not content or len(content.strip()) < 100:
            raise HTTPException(
                status_code=400,
                detail="Transcript content too short. Minimum 100 characters required."
            )
        
        if len(content) > cls.MAX_TEXT_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Text content too large. Maximum size is {cls.MAX_TEXT_SIZE // (1024*1024)}MB"
            )
        
        # Basic content validation - check for suspicious patterns
        cls._scan_for_malicious_content(content)
    
    @classmethod
    def _scan_for_malicious_content(cls, content: str) -> None:
        """Basic scan for potentially malicious content patterns."""
        # Check for suspicious patterns that might indicate malicious content
        suspicious_patterns = [
            '<script',
            'javascript:',
            'eval(',
            'document.cookie',
            'window.location',
        ]
        
        content_lower = content.lower()
        for pattern in suspicious_patterns:
            if pattern in content_lower:
                raise HTTPException(
                    status_code=400,
                    detail="File contains potentially malicious content"
                )