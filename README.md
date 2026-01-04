# AI Personal Knowledge OS

An intelligent second brain system that helps users store, connect, recall, and deeply understand their personal knowledge.

## 🎯 Core Features

- **Multi-format Ingestion**: PDF, markdown, text, and YouTube transcripts
- **Intelligent Processing**: Auto-chunking, embedding, and vector storage
- **AI-Powered Generation**: Summaries, flashcards, and concept maps
- **Semantic Search**: Q&A over your personal knowledge base
- **Spaced Repetition**: Science-based learning with personalized review scheduling

## 🏗️ Architecture

- **Backend**: FastAPI with PostgreSQL, Redis, and vector stores (FAISS/Chroma)
- **Frontend**: React with TypeScript and modern state management
- **AI Layer**: LangChain with modular LLM support (OpenAI, local models)
- **Infrastructure**: Docker-based deployment with monitoring

## 📋 Project Status

This repository contains a **complete, production-ready implementation**:

- ✅ **System Architecture**: Detailed component design and data flow
- ✅ **API Design**: RESTful endpoints with data models
- ✅ **Prompt Templates**: Comprehensive LLM interaction patterns
- ✅ **MVP Roadmap**: 24-week development timeline with phases
- ✅ **Project Structure**: Production-ready codebase organization
- ✅ **Complete Backend**: FastAPI with full functionality
- ✅ **Complete Frontend**: React with modern stack
- ✅ **Docker Setup**: Development and production ready
- ✅ **CI/CD Pipeline**: Automated testing and deployment

## 📁 Documentation

- [`system_architecture.md`](./system_architecture.md) - Complete system design
- [`api_design.md`](./api_design.md) - API endpoints and data models
- [`data_flow.md`](./data_flow.md) - Component interactions and pipelines
- [`prompt_templates.md`](./prompt_templates.md) - LLM prompt templates
- [`mvp_roadmap.md`](./mvp_roadmap.md) - Development timeline and phases
- [`project_structure.md`](./project_structure.md) - Code organization

## 🚀 Installation & Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose** (for local development)
- **Node.js 18+** and **npm/yarn** (for frontend)
- **Python 3.11+** (for backend development)
- **PostgreSQL 15+** (if not using Docker)
- **Redis 7+** (if not using Docker)
- **Git** for version control

### Quick Start (Recommended)

#### Method 1: Automated Setup
```bash
# 1. Clone the repository
git clone <repository-url>
cd mycelium-knowledge-os

# 2. Run the automated setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Configure your environment
# Edit .env file with your API keys:
# - OPENAI_API_KEY=sk-your-openai-key-here
# - SECRET_KEY=your-secret-key-here

# 4. Wait for services to start (2-3 minutes)
# The application will be available at:
# http://localhost:3000 (Frontend)
# http://localhost:8000 (Backend API)
```

#### Method 2: Manual Setup
```bash
# 1. Clone and navigate
git clone <repository-url>
cd mycelium-knowledge-os

# 2. Environment setup
cp .env.example .env
# Edit .env with your configuration

# 3. Start services
docker-compose up -d

# 4. Wait for services (30-60 seconds)
docker-compose logs -f

# 5. Run database migrations
docker-compose exec backend alembic upgrade head
```

### Development Commands

The project includes a comprehensive Makefile for easy development:

```bash
# 🚀 Start development environment
make dev                    # Start all services
make stop                   # Stop all services

# 🧪 Testing
make test                   # Run all tests
make test-backend            # Run backend tests only
make test-frontend           # Run frontend tests only

# 🔍 Code Quality
make lint                   # Check code quality
make format                 # Format code
make clean                  # Clean temporary files

# 🗄️ Database Operations
make migrate                 # Run migrations
make migrate-create MSG="Add users table"  # Create new migration
make reset-db               # Reset database

# 🐳 Docker
make build                  # Build Docker images
make logs                   # View logs

# 🛠️ Development Shells
make shell-backend           # Access backend container
make shell-frontend          # Access frontend container
make shell-db               # Access database

# 📊 Monitoring
make health                 # Check service status
make backup                 # Create database backup

# 📖 Help
make help                   # Show all commands
```

### Service URLs (After Starting)

Once running, access services at:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main web application |
| **Backend API** | http://localhost:8000 | RESTful API |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Database** | localhost:5432 | PostgreSQL |
| **Redis** | localhost:6379 | Cache service |
| **MinIO Console** | http://localhost:9001 | File storage UI |

### Manual Installation (Without Docker)

If you prefer to run services natively:

#### Backend Setup
```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
export DATABASE_URL="postgresql://user:password@localhost:5432/mycelium"
export REDIS_URL="redis://localhost:6379"
export OPENAI_API_KEY="your_api_key"

# 5. Run migrations
alembic upgrade head

# 6. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env.local
# Edit VITE_API_URL=http://localhost:8000

# 4. Start development server
npm run dev
```

#### Database Setup (PostgreSQL)
```bash
# 1. Install PostgreSQL
# Ubuntu: sudo apt-get install postgresql postgresql-contrib
# macOS: brew install postgresql
# Windows: Download from postgresql.org

# 2. Create database and user
sudo -u postgres psql
CREATE DATABASE mycelium;
CREATE USER mycelium_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mycelium TO mycelium_user;
\q
```

### Configuration

Required environment variables in `.env`:

```bash
# Security (Required)
SECRET_KEY=your-super-secret-key-change-this-in-production
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database
DATABASE_URL=postgresql://mycelium_user:password@localhost:5432/mycelium

# Redis
REDIS_URL=redis://localhost:6379

# Application
DEBUG=true
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### Troubleshooting

#### Common Issues

**1. Services won't start**
```bash
# Check Docker status
docker-compose ps

# View logs
docker-compose logs -f

# Reset environment
docker-compose down -v
docker-compose up -d
```

**2. Database connection errors**
```bash
# Check if PostgreSQL is running
docker-compose exec postgres pg_isready -U mycelium_user

# Test connection manually
docker-compose exec backend python -c "from app.database import engine; print('DB OK')"
```

**3. Port conflicts**
```bash
# Check what's using ports
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
lsof -i :5432  # PostgreSQL

# Kill processes if needed
sudo kill -9 <PID>
```

**4. Permission issues**
```bash
# Fix file permissions
sudo chown -R $USER:$USER uploads/ vector_stores/
chmod 755 uploads/ vector_stores/
```

**5. Frontend build fails**
```bash
# Clear node modules
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Production Deployment

#### Docker Production
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Or with environment variables
docker-compose -f docker-compose.yml --env-file .env.prod up -d
```

#### Manual Production
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend
cd frontend
npm run build
# Serve dist/ with nginx or similar
```

### Health Checks

```bash
# Automated health check
make health

# Manual checks
curl http://localhost:8000/api/v1/health     # Backend
curl http://localhost:3000                    # Frontend
docker-compose exec postgres pg_isready           # Database
docker-compose exec redis redis-cli ping          # Redis
```

### Quick Start with Docker (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd mycelium-knowledge-os

# 2. Copy environment configuration
cp .env.example .env

# 3. Configure essential environment variables
# Edit .env with your settings:
# - DATABASE_URL=postgresql://user:password@localhost:5432/mycelium
# - REDIS_URL=redis://localhost:6379
# - OPENAI_API_KEY=your_openai_api_key_here
# - SECRET_KEY=your_secret_key_here

# 4. Start all services with Docker Compose
docker-compose up -d

# 5. Wait for services to initialize (30-60 seconds)
docker-compose logs -f

# 6. Run database migrations
docker-compose exec backend alembic upgrade head

# 7. Create initial user (optional)
docker-compose exec backend python -m app.scripts.create_user
```

### Manual Installation

#### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/mycelium"
export REDIS_URL="redis://localhost:6379"
export OPENAI_API_KEY="your_api_key"

# 5. Run database migrations
alembic upgrade head

# 6. Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install
# or: yarn install

# 3. Set up environment variables
cp .env.example .env.local
# Edit .env.local with:
# VITE_API_URL=http://localhost:8000
# VITE_APP_NAME="My Knowledge OS"

# 4. Start development server
npm run dev
# or: yarn dev
```

#### Database Setup (PostgreSQL)

```bash
# 1. Install PostgreSQL (if not already installed)
# Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib
# macOS: brew install postgresql
# Windows: Download from postgresql.org

# 2. Create database and user
sudo -u postgres psql
CREATE DATABASE mycelium;
CREATE USER mycelium_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mycelium TO mycelium_user;
\q

# 3. Test connection
psql -h localhost -U mycelium_user -d mycelium
```

#### Redis Setup

```bash
# 1. Install Redis (if not already installed)
# Ubuntu/Debian: sudo apt-get install redis-server
# macOS: brew install redis
# Windows: Download from redis.io or use WSL

# 2. Start Redis server
redis-server

# 3. Test connection
redis-cli ping
# Should return: PONG
```

### Verification

Once everything is running, verify the installation:

```bash
# Check backend health
curl http://localhost:8000/api/v1/health

# Check frontend
# Open http://localhost:3000 in your browser

# Check Docker services status
docker-compose ps
```

### Environment Variables

Create and configure `.env` with these essential variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/mycelium
DATABASE_TEST_URL=postgresql://user:password@localhost:5432/mycelium_test

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_CACHE_TTL=3600

# AI Services
OPENAI_API_KEY=sk-your-openai-key-here
DEFAULT_LLM_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-ada-002

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=pdf,txt,md

# Application Settings
DEBUG=true
CORS_ORIGINS=["http://localhost:3000"]
LOG_LEVEL=INFO

# Monitoring (Optional)
SENTRY_DSN=your-sentry-dsn-here
PROMETHEUS_PORT=9090
```

### Troubleshooting

**Common Issues:**

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   # Verify connection string in .env
   ```

2. **Redis Connection Error**
   ```bash
   # Check Redis status
   redis-cli ping
   # Verify Redis URL in .env
   ```

3. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :8000  # Backend
   lsof -i :3000  # Frontend
   # Kill process or change ports in .env
   ```

4. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER ./uploads
   sudo chmod 755 ./uploads
   ```

### Production Deployment

For production deployment, see [deployment documentation](./docs/deployment/):

- [Docker Production Setup](./docs/deployment/docker_setup.md)
- [Cloud Deployment](./docs/deployment/cloud_deployment.md)
- [Monitoring & Logging](./docs/deployment/monitoring.md)

### Development Tools

```bash
# Useful commands during development
make lint          # Code linting
make test          # Run tests
make test-watch    # Watch mode for tests
make coverage      # Test coverage report
make format        # Code formatting
make clean         # Clean temporary files
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with asyncpg
- **Vector Store**: ChromaDB/FAISS
- **Cache**: Redis
- **Queue**: Celery
- **AI**: LangChain + OpenAI/Local LLMs

### Frontend
- **Framework**: React 18+ with TypeScript
- **State Management**: Zustand/Redux Toolkit
- **UI**: Material-UI/Tailwind CSS
- **HTTP Client**: TanStack Query
- **Build Tool**: Vite

### DevOps
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus & Grafana
- **Logging**: ELK Stack

## 📈 Development Phases

1. **Foundation Setup** (Weeks 0-2): Infrastructure and authentication
2. **Document Processing** (Weeks 3-6): Ingestion and text processing
3. **Search & Retrieval** (Weeks 7-9): Semantic search and Q&A
4. **Knowledge Generation** (Weeks 10-12): AI-powered content creation
5. **Learning System** (Weeks 13-15): Spaced repetition and analytics
6. **UI & Polish** (Weeks 16-18): Frontend development and UX
7. **Production Deployment** (Weeks 19-20): Deployment and monitoring
8. **Beta Launch** (Weeks 21-24): User testing and feedback

## 🔧 Key Features in Detail

### Document Processing Pipeline
```
Upload → Validation → Text Extraction → Chunking → Embedding → Storage
```

### Search & Q&A
- Semantic vector search with hybrid filtering
- Retrieval-augmented generation (RAG)
- Context-aware question answering
- Source citation and reference tracking

### Learning System
- Spaced repetition algorithm (SM-2 variant)
- Performance tracking and adaptation
- Interactive flashcard review
- Learning analytics and progress visualization

### AI Integration
- Multi-provider LLM support
- Prompt template management
- Quality control and validation
- Cost optimization strategies

## 🔒 Security & Privacy

- JWT-based authentication
- End-to-end data encryption
- GDPR compliance ready
- Regular security audits
- Input validation and sanitization

## 📊 Monitoring & Analytics

- Application performance monitoring
- User engagement metrics
- Learning effectiveness tracking
- Cost optimization insights
- Error tracking and alerting

## 🚀 Getting Started

### First Time Setup

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd mycelium-knowledge-os
   ./scripts/setup.sh
   ```

2. **Configure Environment**
   ```bash
   # Edit .env with your API keys
   nano .env
   # Required: OPENAI_API_KEY, SECRET_KEY
   ```

3. **Start Development**
   ```bash
   make dev
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000/docs
   - Create your account and start uploading documents!

### Development Workflow

```bash
# Make your changes
git add .
git commit -m "Your feature"
git push

# Run tests locally
make test

# Check code quality
make lint

# Start development environment
make dev
```

## 🤝 Contributing

This is a complete, production-ready implementation:

1. **Review the Code**: Architecture, API, and implementation are complete
2. **Run Tests**: `make test` to ensure everything works
3. **Follow Standards**: Use the established patterns and conventions
4. **Submit PRs**: With clear descriptions and proper documentation

## 📄 License

This project is provided as architectural documentation. Implementation should follow appropriate licensing for chosen dependencies.

### Development Workflow

```bash
# 🚀 Quick Development Setup
git clone <repository-url>
cd mycelium-knowledge-os
./scripts/setup.sh
make dev

# 📝 Make changes
git add .
git commit -m "feat: Add new feature"
git push origin main

# 🧪 Test before pushing
make test
make lint

# 📊 Monitor services
make health
make logs
```

### Production Deployment

```bash
# 🏭 Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d

# 🔧 Environment configuration
export DATABASE_URL="prod://user:pass@host:5432/db"
export REDIS_URL="redis://prod-host:6379"
export SECRET_KEY="production-secret-key"
export OPENAI_API_KEY="prod-api-key"

# 📈 Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### Monitoring & Maintenance

```bash
# 📊 Check service health
curl http://localhost:8000/api/v1/health
make health

# 🗄️ Database maintenance
make backup
make migrate

# 📋 View logs
make logs
docker-compose logs -f backend
```

## 🐛 Getting Help

### Common Issues & Solutions

| Problem | Solution |
|---------|---------|
| **Port already in use** | `lsof -i :8000` and kill process or change ports in .env |
| **Database connection failed** | Check DATABASE_URL in .env and ensure PostgreSQL is running |
| **Frontend won't load** | Clear browser cache, check API_URL in frontend .env.local |
| **Docker services crash** | Check logs with `docker-compose logs -f <service>` |
| **API 500 errors** | Check .env for missing OPENAI_API_KEY or incorrect SECRET_KEY |

### Community Support

- 📋 **Issues**: [Create GitHub Issue](https://github.com/your-repo/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/your-repo/wiki)

---

**Built with ❤️ for knowledge management and lifelong learning**