# FLOW Architecture

## Overview

FLOW is a web-based engineering simulation platform with three main layers:

```
┌─────────────────────────────────────────────┐
│  Frontend (React + Three.js)                │
│  - 3D geometry viewer                       │
│  - Simulation controls                      │
│  - Results visualization                    │
├─────────────────────────────────────────────┤
│  Backend API (FastAPI)                      │
│  - REST endpoints                           │
│  - File management                          │
│  - Simulation orchestration                 │
├─────────────────────────────────────────────┤
│  Solvers (Python)                           │
│  - FEA Classic (FEM)                        │
│  - Thermal Classic (FDM)                    │
│  - Neural Operator (FNO)                    │
└─────────────────────────────────────────────┘
```

## Backend

### API Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/simulations/` | GET | List simulations |
| `/api/v1/simulations/` | POST | Create simulation |
| `/api/v1/simulations/:id` | GET | Get simulation |
| `/api/v1/simulations/:id/upload` | POST | Upload geometry |
| `/api/v1/simulations/:id/run` | POST | Run simulation |
| `/api/v1/solvers/` | GET | List solvers |
| `/api/v1/results/:id` | GET | Get results |

### Solvers

**FEA Classic** — Finite Element Method for structural analysis
- Triangular elements with linear shape functions
- Plane stress formulation
- Gauss-Seidel assembly

**Thermal Classic** — Finite Difference Method for heat transfer
- 2D steady-state conduction
- Gauss-Seidel iterative solver
- Dirichlet boundary conditions

**Neural Operator (FNO)** — Fourier Neural Operator for real-time prediction
- Learns mapping from inputs to solution fields
- 100-500x faster than classical solvers
- Requires GPU for training, CPU for inference

## Frontend

### Pages

- **Dashboard** — simulation list, stats
- **New Simulation** — create and configure
- **Simulation Detail** — run, view results
- **Solvers** — available engines

### Components

- `Layout` — sidebar navigation
- `SimulationPage` — detail view with results
- `SolversPage` — solver comparison

## Database

SQLite (default) or PostgreSQL.

### Tables

- `simulations` — simulation metadata, status, parameters
- `simulation_results` — result fields and data

## Deployment

```bash
docker compose up
```

Backend on port 8000, frontend on port 80.
