# Text Embedding API

A publicly accessible REST API that generates semantic text embeddings using [`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

---

## Overview

This service wraps the `all-MiniLM-L6-v2` model in a FastAPI application. It accepts raw text (single string or a batch) and returns 384-dimensional embedding vectors. The API is secured via an API key passed in the request header.

**Use cases:** semantic search, similarity scoring, retrieval-augmented generation (RAG), recommendation systems.

---

## Project Structure

```
embedding-api/
├── main.py            # FastAPI application
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container build instructions
├── render.yaml        # Render.com deployment config
├── .env.example       # Environment variable template
└── .gitignore
```

---

## Deployment Steps (Render.com — Free Tier)

### Prerequisites
- A [Render.com](https://render.com) account (free)
- Your code pushed to a GitHub repository

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/embedding-api.git
   git push -u origin main
   ```

2. **Create a new Web Service on Render**
   - Go to [render.com/dashboard](https://dashboard.render.com)
   - Click **New → Web Service**
   - Connect your GitHub repo
   - Select **Docker** as the environment
   - Choose the **Free** plan

3. **Set Environment Variable**
   - Under **Environment**, add:
     - Key: `API_KEY`
     - Value: any secure random string (e.g. generate one at [randomkeygen.com](https://randomkeygen.com))

4. **Deploy**
   - Click **Create Web Service**
   - Render will build the Docker image and deploy (~5–10 minutes first time)
   - Your public URL will be: `https://embedding-api.onrender.com`

---

## Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/embedding-api.git
cd embedding-api

# 2. Set up environment
cp .env.example .env
# Edit .env and set your API_KEY

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload --port 8000
```

API will be available at `http://localhost:8000`

---

## API Reference

### Authentication

All requests to `/embed` must include the API key in the header:

```
X-API-Key: your-secret-api-key
```

---

### `GET /`
Health check.

**Response:**
```json
{ "status": "ok", "message": "Text Embedding API is running" }
```

---

### `GET /health`
Service health status.

**Response:**
```json
{ "status": "healthy" }
```

---

### `POST /embed`
Generate embeddings for one or more texts.

**Request Body:**
```json
{
  "text": "Your input text here"
}
```
or for batch:
```json
{
  "text": ["First sentence", "Second sentence"]
}
```

**Response:**
```json
{
  "embeddings": [[0.123, -0.045, ...], ...],
  "model": "sentence-transformers/all-MiniLM-L6-v2",
  "dimensions": 384
}
```

---

### Example — cURL

```bash
curl -X POST https://YOUR-APP.onrender.com/embed \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{"text": "What is the capital of France?"}'
```

### Example — Python

```python
import requests

url = "https://YOUR-APP.onrender.com/embed"
headers = {"X-API-Key": "your-secret-api-key"}
payload = {"text": "What is the capital of France?"}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

print(data["embeddings"])      # List of 384 floats
print(data["dimensions"])      # 384
```

---

## Notes

- The model (~90MB) is baked into the Docker image at build time to avoid cold-start delays.
- The model is loaded once at startup and reused across all requests.
- Render free-tier services spin down after inactivity — first request after idle may take ~30s.
