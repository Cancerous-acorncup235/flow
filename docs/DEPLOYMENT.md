# Deployment Guide

## Docker (Recommended)

```bash
docker compose up
```

Backend: http://localhost:8000
Frontend: http://localhost:80
API Docs: http://localhost:8000/docs

## Manual Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Production

### Environment Variables

```bash
APP_ENV=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@db:5432/flow
CORS_ORIGINS=https://flow.yourdomain.com
```

### Database

For production, use PostgreSQL:

```bash
docker run -d \
  --name flow-db \
  -e POSTGRES_DB=flow \
  -e POSTGRES_USER=flow \
  -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 \
  postgres:16
```

### Reverse Proxy

Nginx config:

```nginx
server {
    listen 80;
    server_name flow.yourdomain.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
    }
}
```

### SSL

```bash
certbot --nginx -d flow.yourdomain.com
```

## GPU Support

For neural operator inference, install CUDA:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu124
```

Set in .env:
```bash
USE_GPU=true
CUDA_VISIBLE_DEVICES=0
```
