# Manufacturing Interview-to-Quotation Platform

A software system that ingests interview transcripts (Traditional Chinese) and optional factory machine photos, then outputs expert-structured summaries, requirement specifications, requirement reports, and multi-option quotations in DOCX and PDF formats.

## Architecture

- **Backend**: Python FastAPI with PostgreSQL
- **Frontend**: React + TypeScript + Vite
- **Queue**: Celery + Redis (for async LLM extraction and document generation)
- **Storage**: Local filesystem or S3-compatible (MinIO)
- **LLM**: Configurable provider (OpenAI-compatible API)

## Quick Start

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis on port 6379
- Backend API on port 8000
- Celery worker
- Frontend on port 5173

### Manual Setup

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
# Set DATABASE_URL, REDIS_URL, LLM_API_KEY, etc.
alembic upgrade head
python run.py
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

#### Celery Worker

```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

### Database Migration

After setting up the database, run migrations:

```bash
cd backend
alembic upgrade head
```

## Features

- Upload interview transcripts and factory photos
- Automatic requirement extraction using LLM
- Evidence tracking for every extracted field
- Three plan options (P1/P2/P3) with pricing ranges
- Document generation (DOCX/PDF)
- Human-in-the-loop editing and versioning
- Auditability with confidence scores and evidence snippets

## Language

Traditional Chinese (Taiwan usage) - zh-TW

