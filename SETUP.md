# Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- (Optional) Docker and Docker Compose

## Environment Variables

### Backend (.env)

Create `backend/.env` from `backend/.env.example`:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/interview_quote

# Redis
REDIS_URL=redis://localhost:6379/0

# LLM Configuration
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your_api_key_here
LLM_MODEL_TEXT=gpt-4-turbo-preview
LLM_MODEL_VISION=gpt-4-vision-preview

# Storage
STORAGE_PATH=./storage
UPLOAD_PATH=./storage/uploads
DOCUMENT_PATH=./storage/documents

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Pricing
TAX_PERCENT=5
CONTINGENCY_PERCENT=10

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Database Setup

1. Create PostgreSQL database:
```bash
createdb interview_quote
```

2. Run migrations:
```bash
cd backend
alembic upgrade head
```

## Running the Application

### Option 1: Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Option 2: Manual Setup

#### Terminal 1: Backend API
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

#### Terminal 2: Celery Worker
```bash
cd backend
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

#### Terminal 3: Frontend
```bash
cd frontend
npm install
npm run dev
```

## Access

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `psql -l | grep interview_quote`

### Redis Connection Issues
- Ensure Redis is running: `redis-cli ping`
- Check REDIS_URL in .env

### LLM API Issues
- Verify LLM_API_KEY is set correctly
- Check LLM_BASE_URL matches your provider
- Test API key with a simple curl request

### File Upload Issues
- Ensure storage directories exist:
  ```bash
  mkdir -p storage/uploads storage/documents
  ```
- Check file permissions

