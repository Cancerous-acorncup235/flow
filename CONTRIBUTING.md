# Contributing to FLOW

## Getting Started

```bash
git clone https://github.com/Vitalcheffe/flow.git
cd flow

# Backend
cd backend
pip install -r requirements.txt
python -m app.main

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

## Project Structure

```
backend/         Python FastAPI server
frontend/        React + TypeScript + Vite
docker/          Dockerfiles and nginx config
docs/            Documentation
examples/        Example simulations
scripts/         Build and deploy scripts
```

## Development

- Backend: Python 3.11+, FastAPI, SQLAlchemy
- Frontend: React 18, TypeScript, Tailwind CSS, Three.js
- Tests: pytest (backend), vitest (frontend)

## Commit Convention

```
feat: add new solver
fix: correct mesh generation
docs: update API reference
test: add thermal solver tests
chore: update dependencies
```

## Pull Requests

1. Fork the repo
2. Create a feature branch
3. Make changes and test
4. Open a PR with description

## License

By contributing, you agree your code will be licensed under MIT.
