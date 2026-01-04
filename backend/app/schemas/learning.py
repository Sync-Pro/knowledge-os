from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FlashcardReviewRequest(BaseModel):
    rating: int  # 1-5 scale
    response_time_ms: Optional[int] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LearningStatsResponse(BaseModel):
    total_cards: int
    cards_reviewed_today: int
    accuracy_rate: float
    current_streak: int
    longest_streak: int
    average_response_time: float
    cards_due_tomorrow: int


class LearningScheduleResponse(BaseModel):
    schedule: List[dict]
    total_due: int
    new_cards_available: int