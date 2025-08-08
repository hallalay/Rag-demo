# RAG Demo

Minimal local Retrieval-Augmented Generation app.

## Architecture

- **Backend**: FastAPI service with OpenAI embeddings and FAISS index.
- **Frontend**: Next.js page for uploading PDFs and asking questions.

## Running

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set OPENAI_API_KEY
uvicorn app:app --reload
```

### Frontend

```bash
cd frontend
pnpm i
pnpm dev
```

Open <http://localhost:3000> and ensure backend at <http://localhost:8000>.
