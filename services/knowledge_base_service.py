"""
knowledge_base_service.py
A simple scaffold for a knowledge base service with file upload/link ingestion, embedding, and retrieval.
This version uses ChromaDB (local vector DB) and OpenAI embeddings (can be swapped for Gemini or others).
"""
import os
from typing import List, Optional
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import tempfile

# Initialize ChromaDB client
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
client = chromadb.Client(Settings(persist_directory=CHROMA_PATH))

# Create or get collection
COLLECTION_NAME = "knowledge_base"
collection = client.get_or_create_collection(COLLECTION_NAME)

# Use Gemini embedding function if OpenAI key is not set
EMBEDDING_API_KEY = os.getenv("OPENAI_API_KEY")
if EMBEDDING_API_KEY:
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=EMBEDDING_API_KEY)
else:
    # Use Gemini embedding (placeholder, replace with actual Gemini embedding function if available)
    def embedding_fn(texts):
        raise RuntimeError("Gemini embedding function is not implemented. Please provide a Gemini embedding function.")

# --- Document Ingestion ---
def add_document(text: str, metadata: Optional[dict] = None):
    """Add a text chunk to the knowledge base."""
    doc_id = f"doc_{collection.count() + 1}"
    collection.add(
        documents=[text],
        metadatas=[metadata or {}],
        ids=[doc_id]
    )
    return doc_id

def add_file(file_path: str, metadata: Optional[dict] = None):
    """Read a file and add its content to the knowledge base."""
    # Try to read as text, fallback to PDF if needed
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        # Try PDF extraction
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            raise RuntimeError(f"Failed to read file as text or PDF: {e}")
    return add_document(text, metadata)

# --- Retrieval ---
def query_knowledge_base(query: str, top_k: int = 3) -> List[dict]:
    """Retrieve the most relevant chunks for a query."""
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        embedding_function=embedding_fn
    )
    # Format results
    docs = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        docs.append({"text": doc, "metadata": meta})
    return docs

# --- (Optional) Web Link Ingestion ---
def add_url(url: str, metadata: Optional[dict] = None):
    import requests
    from bs4 import BeautifulSoup
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text()
    return add_document(text, metadata)

# FastAPI router
router = APIRouter()

@router.post("/knowledge/upload")
def upload_knowledge_file(file: UploadFile = File(...)):
    """Endpoint to upload a file and add its content to the knowledge base."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name
    try:
        doc_id = add_file(tmp_path, {"filename": file.filename})
        return {"status": "success", "doc_id": doc_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

@router.post("/knowledge/url")
def upload_knowledge_url(url: str = Form(...)):
    """Endpoint to add a web page to the knowledge base by URL."""
    try:
        doc_id = add_url(url, {"source": url})
        return {"status": "success", "doc_id": doc_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

@router.post("/knowledge/query")
def query_knowledge(query: str = Form(...)):
    """Endpoint to query the knowledge base."""
    try:
        docs = query_knowledge_base(query)
        return {"status": "success", "results": docs}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

@router.get("/knowledge/test-fetch")
def test_fetch_knowledge():
    """Test endpoint to fetch all documents in the knowledge base for debugging."""
    try:
        results = collection.get()
        docs = []
        for doc, meta in zip(results["documents"], results["metadatas"]):
            docs.append({"text": doc, "metadata": meta})
        return {"status": "success", "results": docs}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

# Example usage:
# add_file("./docs/yourfile.txt", {"source": "yourfile.txt"})
# add_url("https://example.com", {"source": "example.com"})
# docs = query_knowledge_base("What is X?")
