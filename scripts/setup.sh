#!/bin/bash

# Setup script for AI Personal Knowledge OS

set -e

echo "🚀 Setting up AI Personal Knowledge OS..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads vector_stores backups

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing."
    echo "   Required: SECRET_KEY, OPENAI_API_KEY"
fi

# Install dependencies
echo "📦 Installing dependencies..."
make install

# Build and start services
echo "🐳 Building and starting services..."
make build
make dev

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run database migrations
echo "🗄️ Running database migrations..."
make migrate

# Create admin user (optional)
echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Services are available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   MinIO Console: http://localhost:9001"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env file with your API keys"
echo "   2. Register a new user at http://localhost:3000/login"
echo "   3. Upload your first document to start building your knowledge base"
echo ""
echo "🔧 Useful commands:"
echo "   make dev         - Start development environment"
echo "   make test        - Run tests"
echo "   make logs        - View logs"
echo "   make clean       - Clean temporary files"
echo "   make health      - Check service health"