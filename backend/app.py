"""FastAPI application exposing RAG endpoints."""

from __future__ import annotations

from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import Citation, Doc, QueryRequest, QueryResponse, UploadResponse
from rag import pipeline, storage

app = FastAPI(title="RAG MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload", response_model=UploadResponse)
async def upload(files: List[UploadFile] = File(...)) -> UploadResponse:
    """Upload PDF files and rebuild the index."""

    docs = storage.save_uploads(files)
    pipeline.rebuild_index()
    return UploadResponse(docs=[Doc(id=d["id"], title=d["title"]) for d in docs])


@app.get("/sources", response_model=UploadResponse)
async def sources() -> UploadResponse:
    """List indexed documents."""

    docs = storage.get_docs()
    return UploadResponse(docs=[Doc(id=d["id"], title=d["title"]) for d in docs])


@app.post("/query", response_model=QueryResponse)
async def query(body: QueryRequest) -> QueryResponse:
    """Answer a question with optional document filtering."""

    res = pipeline.query(body.question, body.docIds)
    citations = [Citation(**c) for c in res["citations"]]
    return QueryResponse(answer=res["answer"], citations=citations)
