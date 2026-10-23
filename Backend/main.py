 # Backend/main.py
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import os
import database
import chromadb
from vectorstore import CHROMA_DIR
from ingest import extract_text, chunk_text
from vectorstore import create_vector_store

from datetime import datetime, timezone
from pydantic import BaseModel
from search import search_all
from rag import generate_answer

database.init_db()

app = FastAPI(title="Native Language Health Advisory")

ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/documents")
def list_documents():
    return database.list_documents()


@app.get("/api/documents/{document_id}")
def get_document(document_id: int):
    document = database.get_document(document_id)
    if not document:
        raise HTTPException(404, "Document not found")
    return document


@app.delete("/api/documents/{document_id}")
def delete_document(document_id: int):
    document = database.get_document(document_id)
    if not document:
        raise HTTPException(404, "Document not found")

    file_path = database.UPLOAD_DIR / document["filename"]
    file_path.unlink(missing_ok=True)

    if document["collection_reference"]:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        try:
            client.delete_collection(document["collection_reference"])
        except Exception:
            pass  # already gone — nothing left to clean up

    database.delete_document(document_id)
    return {"deleted": True}

ALLOWED_EXTENSIONS = (".pdf", ".txt", ".md")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/documents")
async def upload_document(title: str = Form(...), file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Only .pdf, .txt, and .md files are supported")

    filename = str(uuid.uuid4()) + suffix
    file_path = database.UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    created_at = datetime.now(timezone.utc).isoformat()
    document_id = database.insert_document(title, filename, created_at)

    collection_name = "doc_" + str(document_id)
    try:
        text = extract_text(file_path)
        chunks = chunk_text(text)
        create_vector_store(chunks, collection_name)
        database.update_collection_reference(document_id, collection_name)
    except Exception as e:
        print("Embedding failed for document", document_id, ":", str(e))

    return database.get_document(document_id)

class AskRequest(BaseModel):
    question: str
    language: str = "English"


@app.post("/api/ask")
def ask_question(request: AskRequest):
    documents = database.list_documents()
    chunks = search_all(request.question, documents)
    advice, sources = generate_answer(request.question, chunks, language=request.language)

    created_at = datetime.now(timezone.utc).isoformat()
    entry_id = database.insert_history_entry(
        request.question, request.language, advice, sources, created_at
    )

    return database.get_history_entry(entry_id)

@app.get("/api/history")
def history_list():
    return database.list_history()


@app.get("/api/history/{entry_id}")
def history_detail(entry_id: int):
    entry = database.get_history_entry(entry_id)
    if not entry:
        raise HTTPException(404, "History entry not found")
    return entry


@app.delete("/api/history/{entry_id}")
def history_delete(entry_id: int):
    if not database.get_history_entry(entry_id):
        raise HTTPException(404, "History entry not found")
    database.delete_history_entry(entry_id)
    return {"deleted": True}