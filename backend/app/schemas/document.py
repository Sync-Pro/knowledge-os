from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


class DocumentCreate(BaseModel):
    title: str
    source_type: str
    source_url: Optional[str] = None
    
    @validator('source_type')
    def validate_source_type(cls, v):
        allowed_types = ['pdf', 'youtube', 'markdown', 'text']
        if v not in allowed_types:
            raise ValueError(f'source_type must be one of {allowed_types}')
        return v


class DocumentResponse(BaseModel):
    id: str
    user_id: str
    title: str
    source_type: str
    source_url: Optional[str]
    status: str
    file_size: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    id: str
    title: str
    source_type: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True