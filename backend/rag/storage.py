"""Local file and index management."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Dict, List

from fastapi import UploadFile

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DOCS_DIR = DATA_DIR / "docs"
INDEX_DIR = DATA_DIR / "faiss"
METADATA_FILE = DATA_DIR / "docs.json"

CHUNK_SIZE = 800  # TODO: tune chunk size
CHUNK_OVERLAP = 200  # TODO: tune overlap


def init_storage() -> None:
    """Ensure required directories exist."""

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)


def load_metadata() -> List[Dict]:
    """Load document metadata from disk."""

    if METADATA_FILE.exists():
        return json.loads(METADATA_FILE.read_text())
    return []


def save_metadata(docs: List[Dict]) -> None:
    """Persist document metadata to disk."""

    METADATA_FILE.write_text(json.dumps(docs, indent=2))


def _unique_title(base: str, existing: List[str]) -> str:
    """Append numeric suffix until title is unique."""

    if base not in existing:
        return base
    idx = 1
    while f"{base}_{idx}" in existing:
        idx += 1
    return f"{base}_{idx}"


def save_uploads(files: List[UploadFile]) -> List[Dict]:
    """Store uploaded PDFs and update metadata.

    Returns metadata for all documents (including previous ones).
    """

    init_storage()
    docs = load_metadata()
    titles = [d["title"] for d in docs]
    batch_titles: List[str] = []

    for file in files:
        base = Path(file.filename).stem
        if base in titles:
            # Re-upload: overwrite existing file
            doc = next(d for d in docs if d["title"] == base)
        else:
            title = _unique_title(base, titles + batch_titles)
            doc = {"id": str(uuid.uuid4()), "title": title, "path": str(DOCS_DIR / f"{title}.pdf")}
            docs.append(doc)
            titles.append(title)
        with open(doc["path"], "wb") as f:
            f.write(file.file.read())
        batch_titles.append(doc["title"])

    save_metadata(docs)
    return docs


def get_docs() -> List[Dict]:
    """Return list of stored documents."""

    return load_metadata()
