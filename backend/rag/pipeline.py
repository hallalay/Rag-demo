"""Chunking, embedding, index build/load, and querying."""

from __future__ import annotations

from typing import List, Optional

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pypdf import PdfReader

from . import storage


def _pdf_to_documents(path: str, doc_id: str, title: str) -> List[Document]:
    """Load a PDF and split into LangChain Documents."""

    reader = PdfReader(path)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=storage.CHUNK_SIZE, chunk_overlap=storage.CHUNK_OVERLAP
    )
    docs: List[Document] = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for chunk in splitter.split_text(text):
            docs.append(
                Document(page_content=chunk, metadata={"doc_id": doc_id, "title": title, "page": page_num})
            )
    return docs


def rebuild_index() -> None:
    """Recreate the FAISS index from all stored PDFs."""

    docs_meta = storage.get_docs()
    all_docs: List[Document] = []
    for meta in docs_meta:
        all_docs.extend(_pdf_to_documents(meta["path"], meta["id"], meta["title"]))
    if not all_docs:
        return
    embeddings = OpenAIEmbeddings()  # TODO: switch to OSS embeddings
    index = FAISS.from_documents(all_docs, embeddings)
    index.save_local(str(storage.INDEX_DIR))


def _get_retriever(doc_ids: Optional[List[str]] = None):
    """Create a retriever that optionally filters by doc IDs."""

    embeddings = OpenAIEmbeddings()
    index = FAISS.load_local(str(storage.INDEX_DIR), embeddings, allow_dangerous_deserialization=True)

    def _filter_docs(query: str) -> List[Document]:
        docs = index.similarity_search(query, k=5)
        if doc_ids:
            docs = [d for d in docs if d.metadata.get("doc_id") in doc_ids]
        return docs

    class _Retriever:
        def get_relevant_documents(self, query: str) -> List[Document]:
            return _filter_docs(query)

    return _Retriever()


def query(question: str, doc_ids: Optional[List[str]] = None) -> dict:
    """Run retrieval QA and return answer plus citations."""

    if not storage.INDEX_DIR.exists():
        return {"answer": "No documents indexed.", "citations": []}

    retriever = _get_retriever(doc_ids)
    llm = ChatOpenAI()
    from langchain.chains import RetrievalQA

    qa = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, return_source_documents=True
    )
    res = qa.invoke({"query": question})
    sources: List[Document] = res.get("source_documents", [])
    citations = [
        {"docId": d.metadata["doc_id"], "page": d.metadata["page"], "text": d.page_content}
        for d in sources
    ]
    answer = res.get("result", "")
    if not answer:
        answer = "No relevant information found."
    if not citations:
        answer = "No relevant information found."
    return {"answer": answer, "citations": citations}
