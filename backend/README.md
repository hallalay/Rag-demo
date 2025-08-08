# Backend

Simple FastAPI service for PDF question answering.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set OPENAI_API_KEY=...
```

## Running

```bash
uvicorn app:app --reload
```

## Seeding sample data

```bash
make seed
```

## Endpoints

### `POST /upload`
Upload one or more PDFs.

```bash
curl -F "files=@path/to/file.pdf" http://localhost:8000/upload
```

### `GET /sources`
List indexed documents.

```bash
curl http://localhost:8000/sources
```

### `POST /query`
Ask a question.

```bash
curl -H 'Content-Type: application/json' \
  -d '{"question": "What is in the PDF?", "docIds": ["<doc_id>"]}' \
  http://localhost:8000/query
```
