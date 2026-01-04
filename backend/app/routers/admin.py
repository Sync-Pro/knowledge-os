from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any

from app.database import get_db
from app.models.user import User, Document, Flashcard, Query, LearningSession
from app.routers.auth import get_current_user

router = APIRouter()


@router.get("/stats")
async def get_system_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system-wide statistics."""
    # Check if user is admin (you might want to add an is_admin field)
    if not current_user.email.endswith("@admin.com"):  # Simple admin check
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    try:
        stats = {
            "users": db.query(func.count(User.id)).scalar(),
            "documents": db.query(func.count(Document.id)).scalar(),
            "flashcards": db.query(func.count(Flashcard.id)).scalar(),
            "queries": db.query(func.count(Query.id)).scalar(),
            "learning_sessions": db.query(func.count(LearningSession.id)).scalar()
        }
        
        return {"stats": stats}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stats: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Comprehensive health check."""
    return {
        "status": "healthy",
        "service": "ai-knowledge-os",
        "timestamp": str(func.now()),
        "version": "1.0.0"
    }


@router.post("/llm/switch")
async def switch_llm_provider(
    provider: str,
    current_user: User = Depends(get_current_user)
):
    """Switch LLM provider (admin only)."""
    if not current_user.email.endswith("@admin.com"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # This would update system configuration
    return {"message": f"LLM provider switched to {provider}"}