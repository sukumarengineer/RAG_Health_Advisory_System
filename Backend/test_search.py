# Backend/test_search.py — run this once, then delete it
from ingest import extract_text, chunk_text
from vectorstore import create_vector_store
from search import search_all

# use two different files — e.g. a dengue fact sheet and a malaria fact sheet
create_vector_store(chunk_text(extract_text("FactSheet_dengue.pdf")), collection_name="doc_a")
create_vector_store(chunk_text(extract_text("FactSheet_malaria.txt")), collection_name="doc_b")

fake_documents = [
    {"title": "Dengue Fact Sheet", "collection_reference": "doc_a"},
    {"title": "Malaria Fact Sheet", "collection_reference": "doc_b"},
]

results = search_all("What are the symptoms of dengue?", fake_documents)

for r in results:
    print(round(r["score"], 3), r["document_title"], "-", r["text"][:80])