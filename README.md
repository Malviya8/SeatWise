# SeatWise

An intelligent RAG-based counselling assistant for JoSAA/CSAB admissions.

## Progress

- [x] **Phase 1** — Data Pipeline
  - [x] JoSAA cutoff PDF parser (`backend/ingest/parse_cutoffs.py`)
  - [x] Sample data generator — 131,040 rows across 21 institutes, 6 years
  - [x] Structured cutoff query engine (`backend/retrieval/cutoff_query.py`)

- [x] **Phase 2** — RAG Backend
  - [x] Knowledge base — 12 documents covering all JoSAA/CSAB rules
  - [x] ChromaDB vector store with local + OpenAI embedding support
  - [x] Hybrid retriever — intent classification + smart routing

- [x] **Phase 3** — LLM Layer + FastAPI
  - [x] Prompt templates + system prompt engineering
  - [x] LangChain-style chain with conversation history + streaming
  - [x] 13-route FastAPI server with SSE streaming

- [x] **Phase 4** — React Frontend
  - [x] Chat UI with source badges + metadata
  - [x] Sidebar with rank/category/quota filters
  - [x] Suggested questions + welcome screen

- [ ] **Phase 5** — Deployment + Evals

## Quick Start

```bash
# 1. Install Python deps
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Add: ANTHROPIC_API_KEY=your_key_here
# Add: OPENAI_API_KEY=your_key_here  (for better embeddings, optional)

# 3. Generate sample data
python backend/ingest/generate_sample_data.py

# 4. Build the vector store
python backend/retrieval/vector_store.py --build

# 5. Start the backend
uvicorn backend.api.main:app --reload --port 8000

# 6. Start the frontend (new terminal)
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

## Architecture

```
User Query
    │
    ▼
React Frontend (port 5173)
    │  POST /chat
    ▼
FastAPI Backend (port 8000)
    │
    ├─ Intent Classifier
    │       │
    │       ├── CUTOFF_QUERY ──► CutoffQueryEngine (131K rows CSV)
    │       ├── PROCESS_QUERY ──► ChromaDB (12 doc chunks)
    │       ├── STRATEGY ──────► ChromaDB
    │       └── MIXED ──────────► Both
    │
    └─ Claude API (claude-sonnet-4-20250514)
            │
            ▼
        Answer + Sources + Metadata
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/chat` | Main Q&A (JSON) |
| POST | `/chat/stream` | Streaming Q&A (SSE) |
| POST | `/cutoffs` | Direct cutoff query |
| GET | `/cutoffs/trend` | Year-over-year trend |
| GET | `/institutes` | List all institutes |
| GET | `/programs` | List all programs |
| GET | `/health` | Health check |
| GET | `/stats` | Debug stats |
| POST | `/reset` | Clear chat history |
