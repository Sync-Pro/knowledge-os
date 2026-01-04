.PHONY: help install dev test lint format clean build deploy

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install dependencies for all services"
	@echo "  dev         Start development environment"
	@echo "  test        Run tests for all services"
	@echo "  lint        Run linting for all services"
	@echo "  format      Format code for all services"
	@echo "  clean       Clean temporary files"
	@echo "  build       Build Docker images"
	@echo "  deploy      Deploy to production"

# Install all dependencies
install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installation complete!"

# Start development environment
dev:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Services started at:"
	@echo "  Backend API: http://localhost:8000"
	@echo "  Frontend: http://localhost:3000"
	@echo "  PostgreSQL: localhost:5432"
	@echo "  Redis: localhost:6379"
	@echo "  MinIO: http://localhost:9001"

# Stop development environment
stop:
	@echo "Stopping development environment..."
	docker-compose down

# Run all tests
test:
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v --cov=app
	@echo "Running frontend tests..."
	cd frontend && npm test -- --coverage --watchAll=false

# Run linting
lint:
	@echo "Linting backend..."
	cd backend && python -m flake8 app/ --max-line-length=88
	@echo "Linting frontend..."
	cd frontend && npm run lint

# Format code
format:
	@echo "Formatting backend..."
	cd backend && python -m black app/ && python -m isort app/
	@echo "Formatting frontend..."
	cd frontend && npm run format

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type f -name ".DS_Store" -delete
	@echo "Clean complete!"

# Build Docker images
build:
	@echo "Building Docker images..."
	docker-compose build
	@echo "Build complete!"

# Database operations
migrate:
	@echo "Running database migrations..."
	docker-compose exec backend alembic upgrade head

migrate-create:
	@echo "Creating new migration..."
	@read -p "Enter migration message: " msg; \
	docker-compose exec backend alembic revision --autogenerate -m "$$msg"

reset-db:
	@echo "Resetting database..."
	docker-compose exec backend alembic downgrade base
	docker-compose exec backend alembic upgrade head
	@echo "Database reset complete!"

# Backup operations
backup:
	@echo "Creating database backup..."
	mkdir -p backups
	docker-compose exec postgres pg_dump -U mycelium_user mycelium > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup complete!"

# Production deployment
deploy-staging:
	@echo "Deploying to staging..."
	# Add staging deployment commands here

deploy-production:
	@echo "Deploying to production..."
	# Add production deployment commands here

# Development shortcuts
logs:
	docker-compose logs -f

shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend sh

shell-db:
	docker-compose exec postgres psql -U mycelium_user -d mycelium

# Monitoring
health:
	@echo "Checking service health..."
	@echo "Backend API:"
	curl -s http://localhost:8000/api/v1/health || echo " ❌ Backend down"
	@echo "Frontend:"
	curl -s http://localhost:3000 >/dev/null && echo "  ✅ Frontend up" || echo "  ❌ Frontend down"
	@echo "Database:"
	docker-compose exec postgres pg_isready -U mycelium_user >/dev/null && echo "  ✅ Database up" || echo "  ❌ Database down"
	@echo "Redis:"
	docker-compose exec redis redis-cli ping >/dev/null && echo "  ✅ Redis up" || echo "  ❌ Redis down"