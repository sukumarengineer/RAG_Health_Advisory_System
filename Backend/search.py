# Backend/search.py
from vectorstore import load_vector_store


def search_all(question, documents, k_per_doc=3, top_n=6):
    results = []

    for doc in documents:
        if not doc.get("collection_reference"):
            continue

        store = load_vector_store(doc["collection_reference"])
        matches = store.similarity_search_with_relevance_scores(question, k=k_per_doc)

        for chunk, score in matches:
            results.append({
                "text": chunk.page_content,
                "score": score,
                "document_title": doc["title"],
            })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_n]