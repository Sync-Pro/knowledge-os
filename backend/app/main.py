from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import engine, Base
from app.routers import auth, documents, search, learning, admin
from app.middleware import LoggingMiddleware, RateLimitMiddleware
from app.exceptions import setup_exception_handlers

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up AI Knowledge OS API...")
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Knowledge OS API...")


# Create FastAPI app
app = FastAPI(
    title="AI Personal Knowledge OS",
    description="An intelligent second brain system for knowledge management",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )

# Add custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(learning.router, prefix="/api/v1/learning", tags=["learning"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["administration"])


@app.get("/")
async def root():
    return {
        "message": "AI Personal Knowledge OS API",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "Documentation not available in production"
    }


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-knowledge-os",
        "version": "1.0.0"
    }


@app.get("/api/v1/stats")
async def get_stats():
    return {
        "total_documents": 0,  # Will be implemented with actual database queries
        "total_users": 0,
        "total_searches": 0,
        "system_status": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )