# RAG Knowledge Assistant

A Retrieval-Augmented Generation (RAG) system for semantic document search with role-based access control and citation tracking.

## Features

- **FastAPI Backend**: Async PostgreSQL + pgvector for vector embeddings
- **JWT Authentication**: Role-based access control (admin, editor, viewer)
- **Hybrid Search**: Dense vector similarity + sparse BM25 keyword matching
- **Next.js Frontend**: App Router with TypeScript and Tailwind CSS
- **Kubernetes Deployments**: Kustomize overlays for dev/staging/prod environments
- **CI/CD Pipeline**: GitHub Actions for testing, linting, security scanning, and deployment

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Next.js Frontend │◄────│   FastAPI Backend  │◄────│  PostgreSQL/pgvector │
│       :3000      │     │       :8000         │     │    (pgvector)        │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Core Components

| Component | Description |
|-----------|-------------|
| **Document Ingestion** | Text splitting, embedding generation, storage in pgvector |
| **Hybrid Search** | Combines vector similarity (OpenAI Ada-002) with keyword matching |
| **RBAC** | Role-based access control for document management and search |
| **Citations** | Page-level citations for all generated answers |

### Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend API** | FastAPI, SQLAlchemy async, asyncpg |
| **Vector Database** | PostgreSQL 15 + pgvector extension |
| **Embeddings** | OpenAI Ada-002 (configurable) |
| **Frontend** | Next.js 14+, TypeScript, Tailwind CSS |
| **Auth** | JWT with bcrypt password hashing |
| **CI/CD** | GitHub Actions, Kustomize overlays |

## Project Structure

```
rag-knowledge-assistant/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI route handlers
│   │   ├── db/            # Database models and migrations
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   └── services/      # Business logic (search, embedding, RBAC)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/app/           # Next.js App Router pages
│   ├── package.json
│   └── Dockerfile
├── k8s-manifests/
│   ├── base/              # Base Kubernetes resources
│   ├── overlays/
│   │   ├── dev/           # Development overlay
│   │   ├── staging/       # Staging overlay
│   │   └── prod/          # Production overlay
│   └── kustomization.yaml
├── .github/workflows/     # CI/CD pipelines
│   ├── ci.yml             # Tests, linting, security scans
│   ├── cd-dev.yml         # Deploy to dev namespace
│   ├── cd-staging.yml     # Deploy to staging (PR gated)
│   └── cd-prod.yml        # Deploy to prod (manual approval)
├── .env.example           # Environment variable template
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15 with pgvector extension
- OpenAI API key (for embeddings and LLM generation)

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create .env file from example
cp ../.env.example .env
# Edit .env with your database credentials and OpenAI API key

# Run migrations (ensure pgvector extension is enabled)
python -m app.db.migrate

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp ../.env.example .env.local
# Add OPENAI_API_KEY and API_BASE_URL to .env.local

npm run dev
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string with asyncpg driver | Yes |
| `OPENAI_API_KEY` | OpenAI API key for embeddings and LLM | Yes |
| `EMBEDDING_MODEL` | OpenAI embedding model (default: text-embedding-ada-002) | No |
| `JWT_SECRET_KEY` | Secret key for JWT token signing | Yes |
| `CORS_ORIGINS` | Comma-separated list of allowed CORS origins | No |

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login (returns JWT)
- `GET /api/auth/me` - Get current user info

### Documents
- `POST /api/documents/` - Upload new document
- `GET /api/documents/` - List all documents
- `GET /api/documents/{doc_id}/chunks` - Get document chunks
- `DELETE /api/documents/{doc_id}` - Delete document

### Search
- `POST /api/search/` - Hybrid search with citations

### Health
- `GET /health` - Service health check

## Deployment

### Dev Environment

```bash
# Push to main triggers automatic dev deployment
git push origin main
```

### Staging Environment

```bash
# Create PR targeting main, staging deploys automatically after approval
# Kustomize overlay adds 2 replicas and staging namespace
kubectl apply -k k8s-manifests/overlays/staging
```

### Production Environment

```bash
# Manual workflow dispatch required for production deployment
gh workflow run cd-prod.yml --ref main

# Or deploy manually:
kubectl apply -k k8s-manifests/overlays/prod
```

## CI/CD Pipeline

The repository uses GitHub Actions for continuous integration and delivery:

### CI (ci.yml)
- **Python Linting**: ruff check on backend code
- **Python Tests**: pytest with coverage
- **Security Scanning**: safety for Python packages, npm audit for frontend
- **Docker Build Verification**: Ensures containers build successfully

### CD Pipelines
- **Dev**: Auto-deploys on every push to main
- **Staging**: Deploys after PR approval (gated)
- **Production**: Manual approval required via workflow dispatch

All deployments use Kustomize overlays to manage environment-specific configurations like replica counts, namespaces, and secret references.

## Security

- JWT authentication with bcrypt password hashing
- Role-based access control (admin, editor, viewer)
- OpenAI API key stored as Kubernetes Secret
- Database credentials in Kubernetes Secret
- CORS restrictions configured per environment
- GitHub Secrets for sensitive configuration

## License

MIT License - see LICENSE file for details.

## Author

Thomas Wire
