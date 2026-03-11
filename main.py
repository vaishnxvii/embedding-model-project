from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List, Union
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Text Embedding API",
    description="Generates semantic embeddings using all-MiniLM-L6-v2",
    version="1.0.0"
)

# Load model once at startup
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# API Key auth
API_KEY = os.getenv("API_KEY", "test-key-123")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return key


class EmbedRequest(BaseModel):
    text: Union[str, List[str]]

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]
    model: str
    dimensions: int


@app.get("/")
def root():
    return {"status": "ok", "message": "Text Embedding API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/embed", response_model=EmbedResponse)
def embed(request: EmbedRequest, api_key: str = Security(verify_api_key)):
    texts = request.text if isinstance(request.text, list) else [request.text]

    if not texts or any(t.strip() == "" for t in texts):
        raise HTTPException(status_code=400, detail="Text input cannot be empty")

    embeddings = model.encode(texts, convert_to_numpy=True).tolist()

    return EmbedResponse(
        embeddings=embeddings,
        model="sentence-transformers/all-MiniLM-L6-v2",
        dimensions=len(embeddings[0])
    )
