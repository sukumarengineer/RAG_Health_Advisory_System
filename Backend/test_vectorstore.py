# Backend/test_vectorstore.py — run this once, then delete it
from ingest import extract_text, chunk_text
from vectorstore import create_vector_store, load_vector_store

text = extract_text("FactSheet_Dengue.pdf")   # or "test.txt"
chunks = chunk_text(text)

create_vector_store(chunks, collection_name="doc_test")
print("Embedded", len(chunks), "chunks into collection 'doc_test'")

store = load_vector_store("doc_test")
results = store.similarity_search("what are the symptoms?", k=2)
for r in results:
    print("---")
    print(r.page_content[:150])
