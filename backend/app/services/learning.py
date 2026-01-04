from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import Flashcard, LearningSession
from app.schemas.learning import FlashcardReviewRequest, LearningStatsResponse, LearningScheduleResponse

logger = logging.getLogger(__name__)


class LearningService:
    """Service for spaced repetition learning system."""
    
    def __init__(self):
        self.initial_ease_factor = 2.5
        self.min_ease_factor = 1.3
    
    async def get_due_flashcards(self, user_id: str, limit: int, db: Session) -> List[Dict]:
        """Get flashcards due for review."""
        try:
            flashcards = db.query(Flashcard).filter(
                Flashcard.user_id == user_id,
                Flashcard.next_review <= datetime.utcnow()
            ).limit(limit).all()
            
            return [
                {
                    "id": card.id,
                    "front": card.front,
                    "back": card.back,
                    "difficulty": card.difficulty,
                    "review_count": card.review_count
                }
                for card in flashcards
            ]
        except Exception as e:
            logger.error(f"Error getting due flashcards: {str(e)}")
            raise e
    
    async def process_review(
        self, 
        flashcard_id: str, 
        user_id: str, 
        rating: int, 
        response_time_ms: int,
        db: Session
    ) -> None:
        """Process flashcard review using SM-2 algorithm."""
        try:
            flashcard = db.query(Flashcard).filter(
                Flashcard.id == flashcard_id,
                Flashcard.user_id == user_id
            ).first()
            
            if not flashcard:
                raise ValueError("Flashcard not found")
            
            # SM-2 algorithm implementation
            if rating >= 3:  # Correct response
                if flashcard.review_count == 0:
                    flashcard.interval_days = 1
                elif flashcard.review_count == 1:
                    flashcard.interval_days = 6
                else:
                    flashcard.interval_days = int(flashcard.interval_days * flashcard.difficulty)
                
                flashcard.difficulty = max(
                    self.min_ease_factor,
                    flashcard.difficulty + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
                )
            else:  # Incorrect response
                flashcard.interval_days = 1
                flashcard.difficulty = max(
                    self.min_ease_factor,
                    flashcard.difficulty - 0.2
                )
            
            # Update flashcard
            flashcard.next_review = datetime.utcnow() + timedelta(days=flashcard.interval_days)
            flashcard.last_review = datetime.utcnow()
            flashcard.review_count += 1
            
            # Update success rate
            total_reviews = flashcard.review_count
            successful_reviews = total_reviews * (flashcard.success_rate * 0.01) + (1 if rating >= 3 else 0)
            flashcard.success_rate = (successful_reviews / total_reviews) * 100
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error processing review: {str(e)}")
            raise e
    
    async def get_learning_stats(
        self, 
        user_id: str, 
        days: int, 
        db: Session
    ) -> LearningStatsResponse:
        """Get learning statistics for user."""
        try:
            since_date = datetime.utcnow() - timedelta(days=days)
            
            # Get total cards
            total_cards = db.query(func.count(Flashcard.id)).filter(
                Flashcard.user_id == user_id
            ).scalar() or 0
            
            # Get cards reviewed today
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            cards_reviewed_today = db.query(func.count(Flashcard.id)).filter(
                Flashcard.user_id == user_id,
                Flashcard.last_review >= today_start
            ).scalar() or 0
            
            # Get average accuracy
            avg_accuracy = db.query(func.avg(Flashcard.success_rate)).filter(
                Flashcard.user_id == user_id
            ).scalar() or 0.0
            
            # Get cards due tomorrow
            tomorrow_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            tomorrow_end = tomorrow_start + timedelta(days=1)
            cards_due_tomorrow = db.query(func.count(Flashcard.id)).filter(
                Flashcard.user_id == user_id,
                Flashcard.next_review >= tomorrow_start,
                Flashcard.next_review < tomorrow_end
            ).scalar() or 0
            
            return LearningStatsResponse(
                total_cards=total_cards,
                cards_reviewed_today=cards_reviewed_today,
                accuracy_rate=float(avg_accuracy),
                current_streak=0,  # Would need streak calculation
                longest_streak=0,  # Would need streak calculation
                average_response_time=2500.0,  # Mock value
                cards_due_tomorrow=cards_due_tomorrow
            )
            
        except Exception as e:
            logger.error(f"Error getting learning stats: {str(e)}")
            raise e
    
    async def get_learning_schedule(
        self, 
        user_id: str, 
        days: int, 
        db: Session
    ) -> LearningScheduleResponse:
        """Get learning schedule for upcoming days."""
        try:
            schedule = []
            total_due = 0
            
            for i in range(days):
                date = datetime.utcnow().date() + timedelta(days=i)
                start_datetime = datetime.combine(date, datetime.min.time())
                end_datetime = start_datetime + timedelta(days=1)
                
                due_count = db.query(func.count(Flashcard.id)).filter(
                    Flashcard.user_id == user_id,
                    Flashcard.next_review >= start_datetime,
                    Flashcard.next_review < end_datetime
                ).scalar() or 0
                
                total_due += due_count
                schedule.append({
                    "date": date.isoformat(),
                    "due_cards": due_count
                })
            
            new_cards_available = 5  # Mock value
            
            return LearningScheduleResponse(
                schedule=schedule,
                total_due=total_due,
                new_cards_available=new_cards_available
            )
            
        except Exception as e:
            logger.error(f"Error getting learning schedule: {str(e)}")
            raise e
    
    async def start_session(self, user_id: str, session_type: str, db: Session) -> LearningSession:
        """Start a new learning session."""
        try:
            session = LearningSession(
                user_id=user_id,
                session_type=session_type,
                start_time=datetime.utcnow()
            )
            
            db.add(session)
            db.commit()
            db.refresh(session)
            
            return session
            
        except Exception as e:
            logger.error(f"Error starting session: {str(e)}")
            raise e
    
    async def end_session(
        self, 
        session_id: str, 
        user_id: str, 
        cards_reviewed: int, 
        correct_answers: int,
        db: Session
    ) -> None:
        """End a learning session."""
        try:
            session = db.query(LearningSession).filter(
                LearningSession.id == session_id,
                LearningSession.user_id == user_id
            ).first()
            
            if not session:
                raise ValueError("Session not found")
            
            session.end_time = datetime.utcnow()
            session.cards_reviewed = cards_reviewed
            session.correct_answers = correct_answers
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error ending session: {str(e)}")
            raise e