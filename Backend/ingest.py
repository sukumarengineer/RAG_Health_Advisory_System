# Backend/ingest.py
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)


def extract_text(path):
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        pages = PyPDFLoader(str(path)).load()
    else:
        pages = TextLoader(str(path), encoding="utf-8").load()
    return "\n\n".join(page.page_content for page in pages)


def chunk_text(text):
    return splitter.split_text(text)