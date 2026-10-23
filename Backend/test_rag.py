# Backend/test_rag.py — run this once, then delete it
from ingest import extract_text, chunk_text
from vectorstore import create_vector_store
from search import search_all
from rag import generate_answer

chunks = chunk_text(extract_text("factsheet_dengue.pdf"))
create_vector_store(chunks, collection_name="doc_1")

documents = [{"title": "Dengue Fact Sheet", "collection_reference": "doc_1"}]
question = "What are the symptoms of dengue and how can I prevent it?"
results = search_all(question, documents)

for language in ["English", "Hindi"]:
    advice, sources = generate_answer(question, results, language=language)
    print("=" * 20, language, "=" * 20)
    print("Summary:", advice.symptom_summary)
    print("Prevention:", advice.prevention_steps)
    print("Seek care:", advice.when_to_seek_care)
    print("Disclaimer:", advice.disclaimer)
    print("Sources:", sources)