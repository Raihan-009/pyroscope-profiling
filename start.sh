#!/bin/bash

# Quick start script for FastAPI Pyroscope Profiling Demo

echo "🚀 Starting FastAPI + PostgreSQL + Pyroscope Profiling Demo"
echo "============================================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose is not installed."
    exit 1
fi

echo "📦 Building and starting containers..."
docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check service health
echo ""
echo "🔍 Checking service health..."

# Check FastAPI
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ FastAPI is running at http://localhost:8000"
else
    echo "⚠️  FastAPI is starting up (this may take a moment)..."
fi

# Check Pyroscope
if curl -s http://localhost:4040/health > /dev/null; then
    echo "✅ Pyroscope is running at http://localhost:4040"
else
    echo "⚠️  Pyroscope is starting up (this may take a moment)..."
fi

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
else
    echo "⚠️  PostgreSQL is starting up (this may take a moment)..."
fi

echo ""
echo "============================================================"
echo "🎉 Services are starting up!"
echo ""
echo "📍 Access points:"
echo "   • FastAPI:      http://localhost:8000"
echo "   • API Docs:     http://localhost:8000/docs"
echo "   • Pyroscope:    http://localhost:4040"
echo "   • Health Check: http://localhost:8000/health"
echo ""
echo "📊 Next steps:"
echo "   1. Wait a few seconds for all services to be fully ready"
echo "   2. Open Pyroscope UI: http://localhost:4040"
echo "   3. Generate some load: python test_load.py"
echo "   4. Explore the API: http://localhost:8000/docs"
echo ""
echo "📝 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
echo "============================================================"

