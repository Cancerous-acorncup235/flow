#!/bin/bash
# FLOW Development Setup Script

set -e

echo "🔧 FLOW Development Setup"
echo "========================="

# Check prerequisites
echo "Checking prerequisites..."
python3 --version || { echo "Python 3.11+ required"; exit 1; }
node --version || { echo "Node.js 20+ required"; exit 1; }

# Backend setup
echo ""
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
echo "  ✓ Backend ready"

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd ../frontend
npm install
echo "  ✓ Frontend ready"

# Create directories
cd ..
mkdir -p backend/uploads backend/results backend/models
touch backend/uploads/.gitkeep backend/results/.gitkeep

echo ""
echo "✅ Setup complete!"
echo ""
echo "Start development servers:"
echo "  Backend:  cd backend && source venv/bin/activate && python -m app.main"
echo "  Frontend: cd frontend && npm run dev"
echo ""
echo "Visit http://localhost:5173"
