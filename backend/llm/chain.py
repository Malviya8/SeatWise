"""
backend/llm/chain.py

SeatWise LLM Chain (Groq)
--------------------------
Uses Groq's free API with llama-3.3-70b-versatile.
Get a free key at: https://console.groq.com
"""

import os
import sys
import time
from pathlib import Path
from dataclasses import dataclass, field
from loguru import logger

from groq import Groq

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.retrieval.hybrid_retriever import HybridRetriever, get_retriever, RetrievalResult
from backend.llm.prompt_templates import (
    SYSTEM_PROMPT,
    RAG_PROMPT_TEMPLATE,
    STANDALONE_PROMPT_TEMPLATE,
)

# ── Response model ─────────────────────────────────────────────────────────

@dataclass
class CounsellorResponse:
    answer: str
    sources: list
    intent: str
    cutoff_rows_used: int
    doc_chunks_used: int
    latency_ms: int
    model: str = "llama-3.3-70b-versatile"
    error: str = None

    def to_dict(self):
        return {
            "answer": self.answer,
            "sources": self.sources,
            "intent": self.intent,
            "cutoff_rows_used": self.cutoff_rows_used,
            "doc_chunks_used": self.doc_chunks_used,
            "latency_ms": self.latency_ms,
            "model": self.model,
            "error": self.error,
        }


# ── Conversation history ───────────────────────────────────────────────────

@dataclass
class Message:
    role: str
    content: str

@dataclass
class ConversationHistory:
    messages: list = field(default_factory=list)
    max_turns: int = 10

    def add(self, role, content):
        self.messages.append(Message(role=role, content=content))
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-(self.max_turns * 2):]

    def to_api_format(self):
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def clear(self):
        self.messages = []


# ── Main Chain ─────────────────────────────────────────────────────────────

class SeatWiseChain:

    def __init__(self, retriever=None, model="llama-3.3-70b-versatile",
                 max_tokens=1024, temperature=0.3):

        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set. Add it to your .env file.")

        self.client = Groq(api_key=api_key)
        self.retriever = retriever or get_retriever()
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.history = ConversationHistory()

        logger.info(f"SeatWiseChain ready | model={model}")

    def ask(self, question, year=None, stream=False):
        t_start = time.time()

        try:
            # 1. Retrieve context
            retrieval = self.retriever.retrieve(question, year=year)
            logger.debug(
                f"Retrieved | intent={retrieval.intent} | "
                f"cutoff_rows={retrieval.raw_cutoff_rows} | "
                f"doc_chunks={retrieval.raw_doc_chunks}"
            )

            # 2. Build prompt
            user_prompt = self._build_user_prompt(question, retrieval)

            # 3. Call Groq
            self.history.add("user", user_prompt)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.history.to_api_format()

            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=messages,
            )

            answer = response.choices[0].message.content
            self.history.add("assistant", answer)

            latency_ms = int((time.time() - t_start) * 1000)
            logger.info(f"Response generated | latency={latency_ms}ms")

            return CounsellorResponse(
                answer=answer,
                sources=retrieval.sources,
                intent=retrieval.intent,
                cutoff_rows_used=retrieval.raw_cutoff_rows,
                doc_chunks_used=retrieval.raw_doc_chunks,
                latency_ms=latency_ms,
                model=self.model,
            )

        except Exception as e:
            logger.error(f"Chain error: {e}")
            msg = str(e)
            if "401" in msg or "auth" in msg.lower():
                answer = "Authentication failed. Please check your GROQ_API_KEY in .env"
                err = "auth_error"
            elif "429" in msg:
                answer = "Rate limit reached. Please wait a moment and try again."
                err = "rate_limit"
            elif "model_not_found" in msg or "404" in msg:
                answer = "Model not found. Make sure GROQ_API_KEY is set correctly."
                err = "model_error"
            else:
                answer = f"Something went wrong: {msg}"
                err = str(e)

            return CounsellorResponse(
                answer=answer,
                sources=[],
                intent="ERROR",
                cutoff_rows_used=0,
                doc_chunks_used=0,
                latency_ms=int((time.time() - t_start) * 1000),
                error=err,
            )

    def _build_user_prompt(self, question, retrieval):
        context_parts = []
        if retrieval.structured_context and retrieval.raw_cutoff_rows > 0:
            context_parts.append(f"### Cutoff Data\n{retrieval.structured_context}")
        if retrieval.semantic_context and retrieval.raw_doc_chunks > 0:
            context_parts.append(f"### Official Guidelines\n{retrieval.semantic_context}")

        if context_parts:
            return RAG_PROMPT_TEMPLATE.format(
                context="\n\n".join(context_parts),
                question=question,
            )
        return STANDALONE_PROMPT_TEMPLATE.format(question=question)

    def reset(self):
        self.history.clear()
        logger.info("Conversation history cleared.")


# ── Singleton ──────────────────────────────────────────────────────────────

_chain_instance = None

def get_chain():
    global _chain_instance
    if _chain_instance is None:
        _chain_instance = SeatWiseChain()
    return _chain_instance