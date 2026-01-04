from fastapi import UploadFile
import os
import aiofiles
from pathlib import Path
from typing import Optional

from app.config import settings


class FileStorageService:
    """Service for handling file storage operations."""
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self.max_file_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024  # Convert to bytes
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
    
    async def save_file(self, file: UploadFile, user_id: str) -> str:
        """Save uploaded file to storage."""
        # Validate file
        if file.size > self.max_file_size:
            raise ValueError(f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB")
        
        # Get file extension
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in self.allowed_extensions:
            raise ValueError(f"File type not allowed. Allowed: {self.allowed_extensions}")
        
        # Create user directory
        user_dir = self.upload_dir / user_id
        user_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        filename = f"{file.filename}"
        file_path = user_dir / filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(await file.read())
        
        return str(file_path)
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False
    
    def get_file_path(self, user_id: str, filename: str) -> str:
        """Get file path for user file."""
        return str(self.upload_dir / user_id / filename)