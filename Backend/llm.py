# Backend/llm.py
from click import clear
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set — add it to Backend/.env")


def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", google_api_key=API_KEY, temperature=0.2)


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=API_KEY)