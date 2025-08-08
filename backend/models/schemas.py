from __future__ import annotations

"""Pydantic models for API requests and responses."""

from typing import List, Optional
from pydantic import BaseModel


class Doc(BaseModel):
    """Metadata for a single document."""

    id: str
    title: str


class UploadResponse(BaseModel):
    """Response after uploading documents."""

    docs: List[Doc]


class QueryRequest(BaseModel):
    """Question request body."""

    question: str
    docIds: Optional[List[str]] = None


class Citation(BaseModel):
    """A snippet referenced in the answer."""

    docId: str
    page: int
    text: str


class QueryResponse(BaseModel):
    """Answer with supporting citations."""

    answer: str
    citations: List[Citation]
