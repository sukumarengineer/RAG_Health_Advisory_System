import sqlite3
import json
from pathlib import Path

DB_PATH = Path("health.db")
UPLOAD_DIR = Path("uploads")


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row      # read columns by name
    return conn


def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id                   INTEGER PRIMARY KEY AUTOINCREMENT,
                title                TEXT NOT NULL,
                filename             TEXT NOT NULL,
                collection_reference TEXT,
                created_at           TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS question_history (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                question           TEXT NOT NULL,
                language           TEXT NOT NULL,
                symptom_summary    TEXT NOT NULL,
                prevention_steps   TEXT NOT NULL,
                when_to_seek_care  TEXT NOT NULL,
                disclaimer         TEXT NOT NULL,
                sources            TEXT NOT NULL,
                created_at         TEXT NOT NULL
            )
        """)
    UPLOAD_DIR.mkdir(exist_ok=True)


def insert_history_entry(question, language, advice, sources, created_at):
    with connect() as conn:
        cursor = conn.execute(
            """INSERT INTO question_history
               (question, language, symptom_summary, prevention_steps, when_to_seek_care, disclaimer, sources, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                question,
                language,
                advice.symptom_summary,
                json.dumps(advice.prevention_steps),
                advice.when_to_seek_care,
                advice.disclaimer,
                json.dumps(sources),
                created_at,
            ),
        )
        return cursor.lastrowid


def get_history_entry(entry_id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM question_history WHERE id = ?", (entry_id,)).fetchone()
    if not row:
        return None
    entry = dict(row)
    entry["prevention_steps"] = json.loads(entry["prevention_steps"])
    entry["sources"] = json.loads(entry["sources"])
    return entry


def insert_document(title, filename, created_at):
    with connect() as conn:
        cursor = conn.execute(
            "INSERT INTO documents (title, filename, created_at) VALUES (?, ?, ?)",
            (title, filename, created_at),
        )
        return cursor.lastrowid


def get_document(document_id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM documents WHERE id = ?", (document_id,)).fetchone()
    return dict(row) if row else None

def list_documents():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM documents ORDER BY created_at DESC").fetchall()
    return [dict(row) for row in rows]


def delete_document(document_id):
    with connect() as conn:
        conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))

def update_collection_reference(document_id, collection_reference):
    with connect() as conn:
        conn.execute(
            "UPDATE documents SET collection_reference = ? WHERE id = ?",
            (collection_reference, document_id),
        )

def list_history():
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, question, language, symptom_summary, created_at "
            "FROM question_history ORDER BY created_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def delete_history_entry(entry_id):
    with connect() as conn:
        conn.execute("DELETE FROM question_history WHERE id = ?", (entry_id,))        