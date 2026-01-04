from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User, Flashcard, LearningSession
from app.schemas.learning import FlashcardReviewRequest, LearningStatsResponse, LearningScheduleResponse
from app.routers.auth import get_current_user
from app.services.learning import LearningService

router = APIRouter()
learning_service = LearningService()


@router.get("/flashcards", response_model=List[dict])
async def get_due_flashcards(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get flashcards due for review."""
    try:
        flashcards = await learning_service.get_due_flashcards(
            user_id=current_user.id,
            limit=limit,
            db=db
        )
        return flashcards
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get flashcards: {str(e)}"
        )


@router.post("/flashcards/{flashcard_id}/review")
async def review_flashcard(
    flashcard_id: str,
    review_data: FlashcardReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record flashcard review result."""
    try:
        await learning_service.process_review(
            flashcard_id=flashcard_id,
            user_id=current_user.id,
            rating=review_data.rating,
            response_time_ms=review_data.response_time_ms,
            db=db
        )
        
        return {"message": "Review recorded successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to record review: {str(e)}"
        )


@router.get("/stats", response_model=LearningStatsResponse)
async def get_learning_stats(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get learning statistics."""
    try:
        stats = await learning_service.get_learning_stats(
            user_id=current_user.id,
            days=days,
            db=db
        )
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stats: {str(e)}"
        )


@router.get("/schedule", response_model=LearningScheduleResponse)
async def get_learning_schedule(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get learning schedule for upcoming days."""
    try:
        schedule = await learning_service.get_learning_schedule(
            user_id=current_user.id,
            days=days,
            db=db
        )
        return schedule
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get schedule: {str(e)}"
        )


@router.post("/session/start")
async def start_learning_session(
    session_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new learning session."""
    try:
        session = await learning_service.start_session(
            user_id=current_user.id,
            session_type=session_type,
            db=db
        )
        
        return {"session_id": session.id, "start_time": session.start_time}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start session: {str(e)}"
        )


@router.post("/session/{session_id}/end")
async def end_learning_session(
    session_id: str,
    cards_reviewed: int = 0,
    correct_answers: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End a learning session."""
    try:
        await learning_service.end_session(
            session_id=session_id,
            user_id=current_user.id,
            cards_reviewed=cards_reviewed,
            correct_answers=correct_answers,
            db=db
        )
        
        return {"message": "Session ended successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to end session: {str(e)}"
        )