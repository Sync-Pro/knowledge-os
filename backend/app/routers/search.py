from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.database import get_db
from app.models.user import User, Query
from app.schemas.search import SearchRequest, SearchResponse, QnARequest, QnAResponse
from app.routers.auth import get_current_user
from app.services.search import SearchService

router = APIRouter()
search_service = SearchService()


@router.get("/search", response_model=SearchResponse)
async def search_documents(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search documents using semantic search."""
    try:
        results = await search_service.semantic_search(
            query=q,
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/ask", response_model=QnAResponse)
async def ask_question(
    request: QnARequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ask a question over your knowledge base."""
    try:
        result = await search_service.answer_question(
            question=request.question,
            user_id=current_user.id,
            max_context=request.max_context_documents
        )
        
        # Log the query
        query_record = Query(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            question=request.question,
            answer=result.answer,
            context_sources=result.source_documents,
            llm_provider=result.llm_provider,
            response_time_ms=result.response_time_ms
        )
        
        db.add(query_record)
        db.commit()
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Q&A failed: {str(e)}"
        )


@router.get("/suggestions")
async def get_suggestions(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user)
):
    """Get related content suggestions."""
    try:
        suggestions = await search_service.get_suggestions(
            user_id=current_user.id,
            limit=limit
        )
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get suggestions: {str(e)}"
        )