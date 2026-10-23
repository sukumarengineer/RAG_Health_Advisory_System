# Backend/vectorstore.py
from pathlib import Path
from langchain_chroma import Chroma
from llm import get_embeddings

CHROMA_DIR = Path("chroma_db")


def create_vector_store(chunks, collection_name):
    return Chroma.from_texts(
        texts=chunks,
        embedding=get_embeddings(),
        collection_name=collection_name,
        persist_directory=str(CHROMA_DIR),
    )


def load_vector_store(collection_name):
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )