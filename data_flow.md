# Data Flow Architecture

## Document Ingestion Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │───▶│ API Gateway │───▶│ Auth Service│───▶│ User Store  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                    │
       │ Upload File       │                    │
       ▼                   ▼                    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ File Upload │───▶│ File Store  │    │ Document DB │
│ Validation  │    │ (Temp)      │    │ (Metadata)  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐    ┌─────────────┐
│ Processing  │───▶│ Queue System│
│ Service     │    │ (Background)│
└─────────────┘    └─────────────┘
       │
       ▼
┌─────────────┐
│ Text Parser │───┐
│ (PDF/MD/TXT)│   │
│ YouTube     │   │
│ Transcript  │   │
└─────────────┘   │
                  ▼
           ┌─────────────┐
           │ Text Content│
           │ Extraction  │
           └─────────────┘
                  │
                  ▼
           ┌─────────────┐
           │ Chunking    │───┐
           │ Service     │   │
           └─────────────┘   │
                              ▼
                       ┌─────────────┐
                       │ Content     │
                       │ Chunks      │
                       └─────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       | Embedding   │───┐
                       │ Service     │   │
                       └─────────────┘   │
                                          ▼
                                   ┌─────────────┐
                                   │ Vector      │
                                   │ Store       │
                                   │ (FAISS)      │
                                   └─────────────┘
```

## Query & Search Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │───▶│ API Gateway │───▶│ Query Engine│
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                    │
       │ User Question     │                    │
       ▼                   ▼                    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Question    │───▶│ Query        │───▶│ Vector      │
│ Embedding   │    │ Processing   │    │ Search      │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐    ┌─────────────┐
                    │ Context     │───▶│ Relevant    │
                    │ Retrieval   │    │ Chunks      │
                    └─────────────┘    └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐    ┌─────────────┐
                    │ LLM Router  │───▶│ Response    │
                    │ (RAG)       │    │ Generation  │
                    └─────────────┘    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Answer +    │
                    │ Sources     │
                    └─────────────┘
```

## Learning System Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │───▶│ API Gateway │───▶│ Learning    │
└─────────────┘    └─────────────┘    │ Engine      │
       │                   │            └─────────────┘
       │ Request Cards     │                     │
       ▼                   ▼                     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Spaced Rep  │───▶│ Flashcard   │───▶│ Due         │
│ Algorithm   │    │ Scheduler   │    │ Flashcards  │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                     │
                           ▼                     ▼
                    ┌─────────────┐    ┌─────────────┐
                    │ User        │───▶│ Performance │
                    │ Interaction │    │ Tracking    │
                    └─────────────┘    └─────────────┘
                           │                     │
                           ▼                     ▼
                    ┌─────────────┐    ┌─────────────┐
                    │ Review      │───▶│ Interval    │
                    │ Results     │    │ Update      │
                    └─────────────┘    └─────────────┘
```

## Content Generation Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Document    │───▶│ Processing  │───▶│ AI Service  │
│ Uploaded    │    │ Queue       │    │ Manager     │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                     │
                           ▼                     ▼
                    ┌─────────────┐    ┌─────────────┐
                    │ Content     │───▶│ LLM Router  │
                    │ Chunks      │    │ (Provider   │
                    └─────────────┘    │ Selection)  │
                           │            └─────────────┘
                           ▼                     │
                    ┌─────────────┐               │
                    │ Generation  │───────────────┘
                    │ Tasks       │
                    │ • Summary   │
                    │ • Flashcards│
                    │ • Concepts  │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Prompt      │
                    │ Templates   │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ LLM API     │
                    │ Call        │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Result      │
                    │ Storage     │
                    └─────────────┘
```

## Data Synchronization Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Primary DB  │───▶│ Event Bus   │───▶│ Cache       │
│ (PostgreSQL)│    │ (Redis)     │    │ Layer       │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                    │
       │ CRUD Ops          │ Pub/Sub            │
       ▼                   ▼                    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Metadata    │───▶│ Index Sync  │───▶│ Search      │
│ Updates     │    │ Service     │    │ Index       │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Vector Store│
                    │ Updates     │
                    └─────────────┘
```

## Error Handling & Recovery

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Service     │───▶│ Error       │───▶│ Retry       │
│ Failure     │    │ Detection   │    │ Queue       │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                    │
       ▼                   ▼                    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Dead Letter │    │ Monitoring  │───▶│ Circuit     │
│ Queue       │    │ Service     │    │ Breaker     │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Alerting    │
                    │ System      │
                    └─────────────┘
```

## Performance Optimization Points

### 1. Caching Strategy
- **Redis** for frequently accessed metadata
- **Local cache** for LLM responses
- **CDN** for static document files

### 2. Async Processing
- **Background workers** for document processing
- **Streaming responses** for large documents
- **Batch processing** for embeddings

### 3. Database Optimization
- **Connection pooling** for PostgreSQL
- **Sharding** for vector store at scale
- **Read replicas** for search queries

### 4. Load Balancing
- **Horizontal scaling** of API servers
- **GPU load balancing** for embedding generation
- **Queue-based work distribution**