"""Seed the vector index with the sample PDF."""

from pathlib import Path
from fastapi import UploadFile

from rag import pipeline, storage


def main() -> None:
    path = Path("sample_data/sample.pdf")
    with path.open("rb") as f:
        upload = UploadFile(filename=path.name, file=f)
        storage.save_uploads([upload])
    pipeline.rebuild_index()
    print("Indexed sample.pdf")


if __name__ == "__main__":
    main()
