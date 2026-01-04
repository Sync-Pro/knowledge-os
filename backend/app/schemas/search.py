from pydantic import BaseModel
from typing import List, Optional


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    offset: int = 0


class SearchResult(BaseModel):
    id: str
    title: str
    content: str
    score: float
    source_type: str
    metadata: dict = {}


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    query: str
    response_time_ms: int


class QnARequest(BaseModel):
    question: str
    max_context_documents: int = 5


class QnAResponse(BaseModel):
    question: str
    answer: str
    source_documents: List[str]
    llm_provider: str
    response_time_ms: int