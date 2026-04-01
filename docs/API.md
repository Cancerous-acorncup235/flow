# FLOW API Reference

Base URL: `http://localhost:8000/api/v1`

Interactive docs: http://localhost:8000/docs

---

## Health

### GET /health
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "gpu_available": false,
  "active_simulations": 0
}
```

---

## Simulations

### List Simulations
```
GET /simulations/?page=1&page_size=20&status=completed
```

Response:
```json
{
  "simulations": [...],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

### Create Simulation
```
POST /simulations/
```
```json
{
  "name": "bridge-beam",
  "description": "Structural analysis of bridge beam",
  "solver": "fea_classic",
  "parameters": {
    "length": 2.0,
    "height": 0.15
  },
  "material_properties": {
    "youngs_modulus": 200e9,
    "poissons_ratio": 0.3
  }
}
```

### Get Simulation
```
GET /simulations/{id}
```

### Update Simulation
```
PATCH /simulations/{id}
```
```json
{
  "name": "updated-name",
  "description": "Updated description"
}
```

### Delete Simulation
```
DELETE /simulations/{id}
```

### Upload Geometry
```
POST /simulations/{id}/upload
Content-Type: multipart/form-data
```
Supported formats: `.step`, `.stp`, `.iges`, `.igs`, `.stl`, `.obj`

### Run Simulation
```
POST /simulations/{id}/run
```
```json
{
  "solver_override": "thermal_classic"
}
```

### Cancel Simulation
```
POST /simulations/{id}/cancel
```

---

## Solvers

### List Solvers
```
GET /solvers/
```

### Get Solver
```
GET /solvers/{type}
```
Types: `fea_classic`, `fea_neural`, `thermal_classic`, `thermal_neural`, `fluid_classic`, `fluid_neural`

---

## Results

### Get Results
```
GET /results/{simulation_id}
```

### Get Result Fields
```
GET /results/{simulation_id}/fields
```

---

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message here"
}
```

Status codes:
- `400` Bad Request
- `404` Not Found
- `409` Conflict (e.g., simulation already running)
- `413` File too large
- `422` Validation Error
- `500` Internal Server Error
