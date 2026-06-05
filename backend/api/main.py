"""
backend/api/main.py

FastAPI Application
--------------------
Exposes the SeatWise AI counsellor as a REST API.

Routes:
  POST /chat          — main Q&A endpoint (JSON response)
  POST /chat/stream   — streaming Q&A (Server-Sent Events)
  GET  /cutoffs       — direct structured cutoff query
  GET  /health        — health check
  POST /reset         — clear conversation history
  GET  /stats         — DB stats (for debugging)
"""

import os
import sys
import json
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from loguru import logger
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from backend.llm.chain import SeatWiseChain
from backend.retrieval.cutoff_query import CutoffQuery, get_engine
from backend.retrieval.hybrid_retriever import get_retriever
from backend.retrieval.vector_store import get_vector_store


# ── Lifespan (startup/shutdown) ────────────────────────────────────────────

chain: SeatWiseChain | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load all heavy resources on startup."""
    global chain
    logger.info("Starting up SeatWise API...")

    # Pre-load retriever components (CSV + vector store)
    get_engine()
    get_retriever()

    # Init the chain (validates API key early)
    try:
        chain = SeatWiseChain()
        logger.success("Chain initialized successfully.")
    except ValueError as e:
        logger.error(f"Chain init failed: {e}")
        # App still starts — /health will report degraded state

    logger.success("API ready.")
    yield
    logger.info("Shutting down...")


# ── App ────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="SeatWise API",
    description="AI-powered JoSAA/CSAB counselling assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    year: int | None = Field(None, ge=2019, le=2030)
    session_id: str | None = None   # future: per-session history isolation


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    intent: str
    cutoff_rows_used: int
    doc_chunks_used: int
    latency_ms: int
    model: str
    error: str | None = None


class CutoffQueryRequest(BaseModel):
    rank: int | None = Field(None, ge=1, le=500000)
    institute_type: str | None = None
    institute_name: str | None = None
    program_name: str | None = None
    quota: str | None = None
    category: str | None = None
    gender: str | None = None
    year: int | None = Field(None, ge=2019, le=2030)
    round_no: int | None = Field(None, ge=1, le=6)
    top_n: int = Field(20, ge=1, le=100)


# ── Routes ─────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    engine = get_engine()
    vs = get_vector_store()
    return {
        "status": "ok" if chain else "degraded",
        "chain_ready": chain is not None,
        "cutoff_rows": len(engine.df),
        "vector_docs": vs.count,
        "latest_year": engine.latest_year,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Main Q&A endpoint. Returns full response as JSON.
    Use /chat/stream for streaming.
    """
    if not chain:
        raise HTTPException(503, "Chain not initialized. Check ANTHROPIC_API_KEY.")

    resp = chain.ask(req.question, year=req.year)

    if resp.error and resp.error not in ("rate_limit", "auth_error"):
        logger.error(f"Chain error: {resp.error}")

    return ChatResponse(**resp.to_dict())


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    Streaming Q&A endpoint using Server-Sent Events (SSE).
    Frontend should use EventSource or fetch with streaming.

    Stream format:
      data: <text chunk>\\n\\n        — answer text chunks
      data: [META]{...}[/META]\\n\\n  — final metadata
    """
    if not chain:
        raise HTTPException(503, "Chain not initialized. Check ANTHROPIC_API_KEY.")

    retriever = get_retriever()
    retrieval = retriever.retrieve(req.question, year=req.year)

    from backend.llm.prompt_templates import RAG_PROMPT_TEMPLATE, STANDALONE_PROMPT_TEMPLATE
    context_parts = []
    if retrieval.structured_context and retrieval.raw_cutoff_rows > 0:
        context_parts.append(f"### Cutoff Data\n{retrieval.structured_context}")
    if retrieval.semantic_context and retrieval.raw_doc_chunks > 0:
        context_parts.append(f"### Official Guidelines\n{retrieval.semantic_context}")

    if context_parts:
        user_prompt = RAG_PROMPT_TEMPLATE.format(
            context="\n\n".join(context_parts),
            question=req.question,
        )
    else:
        user_prompt = STANDALONE_PROMPT_TEMPLATE.format(question=req.question)

    chain.history.add("user", user_prompt)
    messages = chain.history.to_api_format()

    async def generate():
        import time
        t_start = time.time()
        full = []

        with chain.client.messages.stream(
            model=chain.model,
            max_tokens=chain.max_tokens,
            temperature=chain.temperature,
            system=chain.system_prompt if hasattr(chain, 'system_prompt') else __import__('backend.llm.prompt_templates', fromlist=['SYSTEM_PROMPT']).SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                full.append(text)
                yield f"data: {json.dumps({'text': text})}\n\n"

        complete = "".join(full)
        chain.history.add("assistant", complete)

        meta = {
            "sources": retrieval.sources,
            "intent": retrieval.intent,
            "cutoff_rows_used": retrieval.raw_cutoff_rows,
            "doc_chunks_used": retrieval.raw_doc_chunks,
            "latency_ms": int((time.time() - t_start) * 1000),
        }
        yield f"data: {json.dumps({'meta': meta})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/cutoffs")
async def query_cutoffs(req: CutoffQueryRequest):
    """
    Direct structured cutoff query — no LLM involved.
    Returns raw matching rows for the given filters.
    """
    engine = get_engine()
    cq = CutoffQuery(
        rank=req.rank,
        institute_type=req.institute_type,
        institute_name=req.institute_name,
        program_name=req.program_name,
        quota=req.quota,
        category=req.category,
        gender=req.gender,
        year=req.year,
        round_no=req.round_no,
        top_n=req.top_n,
    )
    df = engine.query(cq)
    return {
        "count": len(df),
        "year": req.year or engine.latest_year,
        "round": req.round_no or engine.final_round,
        "results": df.to_dict(orient="records"),
    }


@app.get("/cutoffs/trend")
async def cutoff_trend(
    institute: str = Query(..., description="Partial institute name, e.g. 'bombay'"),
    program: str = Query(..., description="Partial program name, e.g. 'computer science'"),
    category: str = Query("General"),
    gender: str = Query("Gender-Neutral"),
    quota: str = Query("All India"),
):
    """Year-over-year closing rank trend for a specific branch."""
    engine = get_engine()
    df = engine.get_trend(institute, program, category, gender, quota)
    return {
        "institute": institute,
        "program": program,
        "category": category,
        "trend": df.to_dict(orient="records"),
    }


@app.get("/institutes")
async def list_institutes(type: str | None = Query(None)):
    """List all institutes, optionally filtered by type (IIT/NIT/IIIT/GFTI)."""
    engine = get_engine()
    return {"institutes": engine.list_institutes(type_filter=type)}


@app.get("/programs")
async def list_programs(institute: str | None = Query(None)):
    """List programs, optionally filtered by institute name."""
    engine = get_engine()
    return {"programs": engine.list_programs(institute_partial=institute)}


@app.post("/reset")
async def reset_conversation():
    """Clear conversation history for the current session."""
    if chain:
        chain.reset()
    return {"status": "ok", "message": "Conversation history cleared."}


@app.get("/stats")
async def stats():
    """Debug endpoint — shows DB stats."""
    engine = get_engine()
    vs = get_vector_store()
    return {
        "cutoff_db": engine.stats,
        "vector_store": {
            "doc_count": vs.count,
            "docs": [d["title"] for d in vs.list_all()],
        },
    }
