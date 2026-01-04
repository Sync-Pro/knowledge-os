# API Design & Data Models

## API Endpoints

### Authentication
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
DELETE /api/v1/auth/logout
```

### Document Management
```
GET    /api/v1/documents                    # List user documents
POST   /api/v1/documents/upload            # Upload new document
GET    /api/v1/documents/{doc_id}          # Get document details
PUT    /api/v1/documents/{doc_id}          # Update document metadata
DELETE /api/v1/documents/{doc_id}          # Delete document
GET    /api/v1/documents/{doc_id}/content  # Get processed content
```

### Knowledge Processing
```
POST   /api/v1/documents/{doc_id}/process   # Trigger document processing
GET    /api/v1/documents/{doc_id}/summary   # Get AI-generated summary
GET    /api/v1/documents/{doc_id}/flashcards # Get generated flashcards
GET    /api/v1/documents/{doc_id}/concepts  # Get concept map
```

### Search & Query
```
GET    /api/v1/search                      # Semantic search
POST   /api/v1/ask                         # Q&A over knowledge base
GET    /api/v1/suggestions                 # Get related content
```

### Learning System
```
GET    /api/v1/flashcards                  # Get due flashcards
POST   /api/v1/flashcards/{card_id}/review # Record review result
GET    /api/v1/learning/stats              # Get learning statistics
GET    /api/v1/learning/schedule           # Get learning schedule
```

### System Management
```
GET    /api/v1/health                      # System health check
GET    /api/v1/stats                       # Usage statistics
POST   /api/v1/llm/switch                  # Switch LLM provider
```

## Data Models

### User Model
```python
class User:
    id: UUID
    email: str
    username: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
    preferences: dict  # LLM preferences, learning settings
```

### Document Model
```python
class Document:
    id: UUID
    user_id: UUID
    title: str
    source_type: str  # pdf, youtube, markdown, text
    source_url: Optional[str]
    file_path: Optional[str]
    status: str  # uploaded, processing, completed, failed
    created_at: datetime
    updated_at: datetime
    metadata: dict  # file size, duration, language, etc.
```

### Content Chunk Model
```python
class ContentChunk:
    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    chunk_type: str  # text, code, image_caption
    embedding: List[float]  # Vector representation
    metadata: dict  # page number, timestamp, etc.
    created_at: datetime
```

### Summary Model
```python
class Summary:
    id: UUID
    document_id: UUID
    summary_type: str  # brief, detailed, bullet_points
    content: str
    llm_provider: str
    created_at: datetime
    updated_at: datetime
```

### Flashcard Model
```python
class Flashcard:
    id: UUID
    document_id: UUID
    front: str
    back: str
    difficulty: float  # 0-1, updated by learning algorithm
    interval_days: int
    next_review: datetime
    last_review: Optional[datetime]
    review_count: int
    success_rate: float
    created_at: datetime
```

### Concept Map Model
```python
class Concept:
    id: UUID
    document_id: UUID
    name: str
    definition: str
    confidence: float
    embedding: List[float]
    created_at: datetime

class ConceptRelationship:
    id: UUID
    source_concept_id: UUID
    target_concept_id: UUID
    relationship_type: str  # prerequisite, related, example, contrast
    confidence: float
    created_at: datetime
```

### Query Model
```python
class Query:
    id: UUID
    user_id: UUID
    question: str
    answer: str
    context_sources: List[UUID]  # Referenced document/chunk IDs
    llm_provider: str
    response_time_ms: int
    user_rating: Optional[int]  # 1-5 stars
    created_at: datetime
```

### Learning Session Model
```python
class LearningSession:
    id: UUID
    user_id: UUID
    session_type: str  # flashcards, reading, review
    start_time: datetime
    end_time: Optional[datetime]
    cards_reviewed: int
    correct_answers: int
    created_at: datetime
```

## API Response Formats

### Standard Response
```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully",
  "timestamp": "2024-01-01T00:00:00Z",
  "request_id": "uuid"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {}
  },
  "timestamp": "2024-01-01T00:00:00Z",
  "request_id": "uuid"
}
```

### Paginated Response
```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 100,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

## Request Validation

### Document Upload
- Max file size: 50MB
- Supported formats: PDF, MD, TXT
- YouTube URL validation
- Content type verification

### Search Parameters
- Query string length: 1-500 characters
- Max results: 50 per page
- Filters: date range, document types, tags

### Rate Limiting
- Authenticated users: 100 requests/minute
- Search endpoints: 30 requests/minute
- Processing endpoints: 10 requests/minute