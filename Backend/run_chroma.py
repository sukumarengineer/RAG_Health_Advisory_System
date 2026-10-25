import os
import numpy as np
import uvicorn
from chromadb.api.rust import RustBindingsAPI

# Configure local persistence and CORS for VS Code extension
os.environ["IS_PERSISTENT"] = "TRUE"
os.environ["PERSIST_DIRECTORY"] = "./chroma_db"
os.environ["CHROMA_SERVER_CORS_ALLOW_ORIGINS"] = '["*"]'

# In-memory patch: wrap list embeddings in numpy arrays so FastAPI's .tolist() call succeeds
orig_get = RustBindingsAPI._get
def patched_get(self, *args, **kwargs):
    res = orig_get(self, *args, **kwargs)
    if res.get("embeddings") is not None:
        res["embeddings"] = [np.asarray(e) if isinstance(e, list) else e for e in res["embeddings"]]
    return res
RustBindingsAPI._get = patched_get

orig_query = RustBindingsAPI._query
def patched_query(self, *args, **kwargs):
    res = orig_query(self, *args, **kwargs)
    if res.get("embeddings") is not None:
        res["embeddings"] = [
            [np.asarray(e) if isinstance(e, list) else e for e in row]
            for row in res["embeddings"]
        ]
    return res
RustBindingsAPI._query = patched_query

if __name__ == "__main__":
    uvicorn.run("chromadb.app:app", host="127.0.0.1", port=8001)
