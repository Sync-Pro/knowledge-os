# AI Personal Knowledge OS - Project Structure

```
mycelium-knowledge-os/
├── README.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── Makefile
├── requirements.txt
├── pyproject.toml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy.yml
│       └── security.yml
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── middleware.py
│   │   ├── exceptions.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   ├── search.py
│   │   │   ├── learning.py
│   │   │   └── admin.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   ├── content.py
│   │   │   ├── learning.py
│   │   │   └── analytics.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   ├── search.py
│   │   │   ├── learning.py
│   │   │   └── common.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── document_processing.py
│   │   │   ├── search.py
│   │   │   ├── learning.py
│   │   │   ├── ai_services.py
│   │   │   └── file_storage.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── llm_router.py
│   │   │   ├── prompt_manager.py
│   │   │   ├── vector_store.py
│   │   │   └── cache.py
│   │   ├── workers/
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   ├── document_processor.py
│   │   │   └── content_generator.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── text_processing.py
│   │       ├── file_utils.py
│   │       ├── embeddings.py
│   │       └── validators.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_documents.py
│   │   ├── test_search.py
│   │   └── test_learning.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic.ini
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Loading.tsx
│   │   │   │   └── ErrorBoundary.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── documents/
│   │   │   │   ├── DocumentUpload.tsx
│   │   │   │   ├── DocumentList.tsx
│   │   │   │   ├── DocumentView.tsx
│   │   │   │   └── DocumentCard.tsx
│   │   │   ├── search/
│   │   │   │   ├── SearchBar.tsx
│   │   │   │   ├── SearchResults.tsx
│   │   │   │   └── QnAInterface.tsx
│   │   │   └── learning/
│   │   │       ├── Dashboard.tsx
│   │   │       ├── FlashcardReview.tsx
│   │   │       ├── ProgressChart.tsx
│   │   │       └── LearningStats.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Documents.tsx
│   │   │   ├── Search.tsx
│   │   │   ├── Learning.tsx
│   │   │   └── Settings.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useDocuments.ts
│   │   │   ├── useSearch.ts
│   │   │   └── useLearning.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   ├── documents.ts
│   │   │   ├── search.ts
│   │   │   └── learning.ts
│   │   ├── store/
│   │   │   ├── index.ts
│   │   │   ├── authSlice.ts
│   │   │   ├── documentsSlice.ts
│   │   │   ├── searchSlice.ts
│   │   │   └── learningSlice.ts
│   │   ├── types/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   ├── document.ts
│   │   │   ├── search.ts
│   │   │   └── learning.ts
│   │   ├── utils/
│   │   │   ├── constants.ts
│   │   │   ├── helpers.ts
│   │   │   ├── validators.ts
│   │   │   └── formatters.ts
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   ├── components.css
│   │   │   └── variables.css
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── setupTests.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── shared/
│   ├── types/
│   │   ├── user.ts
│   │   ├── document.ts
│   │   ├── search.ts
│   │   └── learning.ts
│   ├── utils/
│   │   ├── validation.ts
│   │   └── constants.ts
│   └── package.json
├── docs/
│   ├── api/
│   │   ├── openapi.yaml
│   │   └── postman_collection.json
│   ├── architecture/
│   │   ├── system_design.md
│   │   ├── database_schema.md
│   │   └── api_design.md
│   ├── deployment/
│   │   ├── docker_setup.md
│   │   ├── cloud_deployment.md
│   │   └── monitoring.md
│   └── user/
│       ├── user_guide.md
│       ├── api_reference.md
│       └── troubleshooting.md
├── scripts/
│   ├── setup.sh
│   ├── migrate.sh
│   ├── backup.sh
│   └── deploy.sh
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── rules/
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   └── logs/
│       └── logstash.conf
└── infrastructure/
    ├── terraform/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── ansible/
    │   ├── playbooks/
    │   └── roles/
    └── kubernetes/
        ├── deployments/
        ├── services/
        └── ingress/
```

## Core Files Overview

### Backend Core Files
- `main.py`: FastAPI application entry point
- `config.py`: Configuration management and environment variables
- `database.py`: Database connection and session management
- `dependencies.py`: FastAPI dependency injection
- `middleware.py`: Custom middleware for authentication, CORS, etc.

### Service Layer
- `auth.py`: Authentication and authorization logic
- `document_processing.py`: Document ingestion and processing
- `search.py`: Semantic search and Q&A functionality
- `learning.py`: Spaced repetition and learning algorithms
- `ai_services.py`: LLM integration and prompt management

### Frontend Core Files
- `App.tsx`: Main React application component
- `api.ts`: HTTP client and API integration
- `index.ts`: Application entry point
- `store/`: Redux/Zustand state management
- `hooks/`: Custom React hooks for API calls

### Configuration Files
- `docker-compose.yml`: Development environment setup
- `pyproject.toml`: Python project configuration
- `package.json`: Node.js dependencies and scripts
- `alembic.ini`: Database migration configuration