"""
backend/retrieval/hybrid_retriever.py

Hybrid Retriever
-----------------
The core retrieval layer. Combines:
  1. Semantic search (ChromaDB) — for rules, process, FAQs
  2. Structured query (CSV/pandas) — for exact rank/cutoff lookups

The LLM chain calls this to gather all context before answering.
Intent is classified first, then the right retriever (or both) is used.

Intent types:
  CUTOFF_QUERY    → "What is closing rank for IIT Bombay CSE General?"
  PROCESS_QUERY   → "What does float mean in JoSAA?"
  ELIGIBILITY     → "Am I eligible for NIT with 70% in Class 12?"
  STRATEGY        → "How should I fill my choices?"
  MIXED           → Needs both structured + semantic retrieval
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Literal
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.retrieval.cutoff_query import CutoffQueryEngine, CutoffQuery, get_engine
from backend.retrieval.vector_store import VectorStore, get_vector_store


# ── Intent Classification ──────────────────────────────────────────────────

Intent = Literal["CUTOFF_QUERY", "PROCESS_QUERY", "ELIGIBILITY", "STRATEGY", "MIXED"]

# Keyword patterns for fast rule-based intent detection
# (LLM-based classification used if this is ambiguous)
CUTOFF_KEYWORDS = [
    r"\branch\b", r"\bclosing rank\b", r"\bopening rank\b", r"\bcutoff\b",
    r"\bcut.?off\b", r"\brank\b.*\bget\b", r"\bget\b.*\brank\b",
    r"\bwhat.*rank\b", r"\bwhich.*college\b", r"\bwhich.*nit\b",
    r"\bwhich.*iit\b", r"\bcan i get\b", r"\bmy rank\b",
    r"\b\d{3,6}\b.*\b(rank|score)\b",
]

PROCESS_KEYWORDS = [
    r"\bfloat\b", r"\bfreeze\b", r"\bslide\b", r"\bwithdraw\b",
    r"\bwhat is josaa\b", r"\bhow does\b", r"\bwhat happens\b",
    r"\bdocument\b", r"\bverification\b", r"\breporting\b",
    r"\bdeadline\b", r"\bschedule\b", r"\btimeline\b",
    r"\brefund\b", r"\bfee\b", r"\bwithdrawal\b",
    r"\bcsab\b", r"\bspecial round\b",
]

STRATEGY_KEYWORDS = [
    r"\bhow.*fill\b", r"\bchoice filling\b", r"\bstrategy\b",
    r"\bshould i\b", r"\badvice\b", r"\btips\b", r"\bbetter\b.*\bcolleg\b",
    r"\bhow many choices\b", r"\border.*preference\b",
]


def classify_intent(query: str) -> Intent:
    """
    Rule-based intent classification.
    Returns the most likely intent for routing.
    """
    q_lower = query.lower()

    has_cutoff = any(re.search(p, q_lower) for p in CUTOFF_KEYWORDS)
    has_process = any(re.search(p, q_lower) for p in PROCESS_KEYWORDS)
    has_strategy = any(re.search(p, q_lower) for p in STRATEGY_KEYWORDS)

    if has_cutoff and (has_process or has_strategy):
        return "MIXED"
    if has_cutoff:
        return "CUTOFF_QUERY"
    if has_strategy:
        return "STRATEGY"
    if has_process:
        return "PROCESS_QUERY"
    return "PROCESS_QUERY"  # default to semantic search


def extract_rank(query: str) -> int | None:
    """Pull the first 3-6 digit number from query as the JEE rank."""
    match = re.search(r"\b(\d{3,6})\b", query)
    return int(match.group(1)) if match else None


def extract_category(query: str) -> str | None:
    """Extract category mention from query."""
    q = query.lower()
    if "obc" in q:
        return "OBC-NCL"
    if "sc" in q and "cse" not in q:
        return "SC"
    if "st" in q and "nit" not in q:
        return "ST"
    if "ews" in q:
        return "EWS"
    if "general" in q or "open" in q or "unreserved" in q:
        return "General"
    return None


def extract_institute_type(query: str) -> str | None:
    q = query.lower()
    if "iit" in q:
        return "IIT"
    if "nit" in q:
        return "NIT"
    if "iiit" in q:
        return "IIIT"
    return None


def extract_gender(query: str) -> str | None:
    q = query.lower()
    if "female" in q or "girl" in q or "women" in q:
        return "Female"
    return None


# ── Retrieval Result ───────────────────────────────────────────────────────

@dataclass
class RetrievalResult:
    intent: Intent
    structured_context: str      # formatted cutoff data
    semantic_context: str        # formatted doc chunks
    sources: list[str]           # citation list for the LLM
    raw_cutoff_rows: int         # how many cutoff rows were found
    raw_doc_chunks: int          # how many doc chunks were found


# ── Hybrid Retriever ───────────────────────────────────────────────────────

class HybridRetriever:
    """
    Main retrieval class used by the LLM chain.
    Routes queries to the right retriever and combines results.
    """

    def __init__(
        self,
        cutoff_engine: CutoffQueryEngine = None,
        vector_store: VectorStore = None,
    ):
        self.cutoff_engine = cutoff_engine or get_engine()
        self.vector_store = vector_store or get_vector_store()

    def retrieve(self, query: str, year: int = None) -> RetrievalResult:
        """
        Main entry point. Classifies intent and retrieves context.

        Args:
            query: user's natural language question
            year: override year for cutoff queries (defaults to latest)

        Returns:
            RetrievalResult with all context ready for the LLM
        """
        intent = classify_intent(query)
        logger.debug(f"Intent: {intent} | Query: '{query[:60]}'")

        structured_context = ""
        semantic_context = ""
        sources = []
        raw_cutoff_rows = 0
        raw_doc_chunks = 0

        # ── Structured retrieval ───────────────────────────────────────────
        if intent in ("CUTOFF_QUERY", "MIXED"):
            cq = CutoffQuery(
                rank=extract_rank(query),
                category=extract_category(query),
                institute_type=extract_institute_type(query),
                gender=extract_gender(query),
                year=year,
                top_n=15,
            )

            # Also extract institute/program name mentions
            cq.institute_name = self._extract_institute_name(query)
            cq.program_name = self._extract_program_name(query)

            df = self.cutoff_engine.query(cq)
            raw_cutoff_rows = len(df)
            structured_context = self.cutoff_engine.format_for_llm(df)

            if not df.empty:
                sources.append(f"JoSAA Cutoff Data {self.cutoff_engine.latest_year} (Round {self.cutoff_engine.final_round})")

        # ── Semantic retrieval ─────────────────────────────────────────────
        if intent in ("PROCESS_QUERY", "STRATEGY", "ELIGIBILITY", "MIXED"):
            if self.vector_store.count > 0:
                docs = self.vector_store.search(query, n=3)
                raw_doc_chunks = len(docs)
                semantic_context = self.vector_store.format_for_llm(docs)
                sources.extend([d["source"] for d in docs])
            else:
                logger.warning(
                    "Vector store is empty. Run: "
                    "python backend/retrieval/vector_store.py --build"
                )
                semantic_context = (
                    "Knowledge base not yet built. "
                    "Run vector_store.py --build to enable semantic search."
                )

        return RetrievalResult(
            intent=intent,
            structured_context=structured_context,
            semantic_context=semantic_context,
            sources=list(dict.fromkeys(sources)),  # deduplicate
            raw_cutoff_rows=raw_cutoff_rows,
            raw_doc_chunks=raw_doc_chunks,
        )

    def _extract_institute_name(self, query: str) -> str | None:
        """Extract partial institute name from query for fuzzy matching."""
        q = query.lower()
        # Common shorthand patterns
        shortcuts = {
            "iit b": "bombay", "iitb": "bombay",
            "iit d": "delhi", "iitd": "delhi",
            "iit m": "madras", "iitm": "madras",
            "iit kgp": "kharagpur", "iit k": "kanpur",
            "iit r": "roorkee", "iit h": "hyderabad",
            "nit t": "trichy", "nit w": "warangal",
            "nit k": "calicut", "nit surathkal": "surathkal",
        }
        for short, full in shortcuts.items():
            if short in q:
                return full

        # Try to extract institute name after keywords
        for keyword in ["at ", "in ", "from "]:
            idx = q.find(keyword)
            if idx != -1:
                after = q[idx + len(keyword):idx + len(keyword) + 30].strip()
                if after:
                    return after.split()[0]  # first word after keyword

        return None

    def _extract_program_name(self, query: str) -> str | None:
        """Extract program/branch name from query."""
        q = query.lower()
        program_map = {
            "cse": "computer science",
            "cs": "computer science",
            "computer science": "computer science",
            "ece": "electronics",
            "ee": "electrical",
            "electrical": "electrical",
            "mech": "mechanical",
            "mechanical": "mechanical",
            "civil": "civil",
            "chemical": "chemical",
            "aerospace": "aerospace",
            "maths": "mathematics",
            "math": "mathematics",
            "data science": "data science",
            "ai": "artificial intelligence",
        }
        for key, val in program_map.items():
            if key in q:
                return val
        return None


# ── Singleton ──────────────────────────────────────────────────────────────

_retriever_instance: HybridRetriever | None = None

def get_retriever() -> HybridRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = HybridRetriever()
    return _retriever_instance


# ── Quick test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    retriever = get_retriever()

    test_queries = [
        "What is the float option in JoSAA?",
        "Which IITs can I get with rank 2000 General?",
        "How should I fill my choices in JoSAA?",
        "What documents do I need for reporting?",
        "Can I get IIT Bombay CSE with rank 150 General?",
    ]

    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {q}")
        result = retriever.retrieve(q)
        print(f"Intent: {result.intent}")
        print(f"Cutoff rows: {result.raw_cutoff_rows} | Doc chunks: {result.raw_doc_chunks}")
        if result.structured_context:
            print(f"Structured (first 300 chars):\n{result.structured_context[:300]}...")
        if result.semantic_context:
            print(f"Semantic (first 300 chars):\n{result.semantic_context[:300]}...")
        print(f"Sources: {result.sources}")
