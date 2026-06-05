"""
backend/retrieval/vector_store.py

ChromaDB Vector Store
----------------------
Embeds all knowledge base documents into ChromaDB for semantic search.
Uses OpenAI text-embedding-3-small (recommended for production).

Falls back to a lightweight local TF-IDF-style embedding for offline dev.

Usage:
    # Build the store (run once)
    python backend/retrieval/vector_store.py --build

    # Then query
    from backend.retrieval.vector_store import get_vector_store
    store = get_vector_store()
    results = store.search("what is float option in josaa", n=3)
"""

import os
import re
import sys
import math
import hashlib
import argparse
from pathlib import Path
from loguru import logger
from collections import Counter

import chromadb
from chromadb.config import Settings

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.ingest.knowledge_base import get_all_documents

CHROMA_DIR = ROOT / "data" / "embeddings"
COLLECTION_NAME = "josaa_knowledge"
EMBEDDING_DIM = 256   # dimension for local fallback embeddings


# ── Local fallback embedding (no external deps) ────────────────────────────

from chromadb import EmbeddingFunction, Documents, Embeddings

class LocalEmbeddingFunction(EmbeddingFunction):
    """
    Lightweight keyword-frequency embedding for offline development.
    Produces 256-dim vectors. Not as good as OpenAI but works anywhere.

    Replace with OpenAI embeddings for production — just set OPENAI_API_KEY.
    """

    @staticmethod
    def name() -> str:
        return "local_keyword_embedding"

    def build_from_config(self, config):
        return LocalEmbeddingFunction()

    def get_config(self):
        return {}

    # JoSAA-domain vocabulary for better coverage
    DOMAIN_VOCAB = [
        "josaa", "csab", "iit", "nit", "iiit", "gfti", "jee", "advanced", "main",
        "rank", "cutoff", "closing", "opening", "allotment", "seat", "round",
        "float", "freeze", "slide", "withdraw", "reject", "accept", "lock",
        "choice", "filling", "preference", "category", "quota", "general",
        "obc", "ncl", "sc", "st", "ews", "pwd", "disability", "reservation",
        "female", "supernumerary", "gender", "neutral",
        "home", "state", "other", "india", "all",
        "document", "verification", "reporting", "certificate",
        "fee", "refund", "payment", "deposit",
        "computer", "science", "engineering", "electrical", "mechanical",
        "civil", "chemical", "aerospace", "mathematics", "computing",
        "data", "artificial", "intelligence", "information", "technology",
        "bombay", "delhi", "madras", "kharagpur", "kanpur", "roorkee",
        "hyderabad", "trichy", "warangal", "surathkal", "calicut",
        "eligibility", "criteria", "marks", "percentage", "class", "twelve",
        "domicile", "creamy", "layer", "income", "certificate",
        "schedule", "timeline", "deadline", "portal", "register",
    ]

    def __init__(self):
        self._vocab = {w: i for i, w in enumerate(self.DOMAIN_VOCAB)}

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r'\b[a-z]{2,}\b', text.lower())

    def _embed_one(self, text: str) -> list[float]:
        tokens = self._tokenize(text)
        vec = [0.0] * EMBEDDING_DIM

        # Domain vocab term frequency (first 64 dims)
        counts = Counter(tokens)
        total = max(len(tokens), 1)
        for word, idx in self._vocab.items():
            if idx < 64:
                vec[idx] = counts.get(word, 0) / total

        # Character n-gram hashing (remaining dims for coverage)
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
        for bg in bigrams:
            h = int(hashlib.md5(bg.encode()).hexdigest(), 16)
            idx = 64 + (h % (EMBEDDING_DIM - 64))
            vec[idx] = min(vec[idx] + 0.1, 1.0)

        # L2 normalize
        norm = math.sqrt(sum(x*x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def __call__(self, input: list[str]) -> list[list[float]]:
        return [self._embed_one(t) for t in input]


# ── Embedding function factory ─────────────────────────────────────────────

def get_embedding_function():
    """
    Returns the best available embedding function.
    Priority: OpenAI (if key set) → local fallback.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")

    if api_key and api_key not in ("your_openai_api_key_here", ""):
        logger.info("Using OpenAI text-embedding-3-small")
        from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
        return OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small",
        )

    logger.warning(
        "No OPENAI_API_KEY — using local keyword embedding (dev mode).\n"
        "Set OPENAI_API_KEY in .env for production-quality semantic search."
    )
    return LocalEmbeddingFunction()


# ── Vector Store ───────────────────────────────────────────────────────────

class VectorStore:
    """
    Wraps ChromaDB with helpers for building, searching, and inspecting
    the JoSAA knowledge base collection.
    """

    def __init__(self, persist_dir: Path = CHROMA_DIR):
        persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self.ef = get_embedding_function()
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.ef,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            f"VectorStore ready | collection={COLLECTION_NAME} | "
            f"docs={self.collection.count()}"
        )

    # ── Build ──────────────────────────────────────────────────────────────

    def build(self, documents: list[dict] = None, reset: bool = False) -> int:
        if reset:
            logger.warning("Resetting existing collection...")
            self.client.delete_collection(COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                embedding_function=self.ef,
                metadata={"hnsw:space": "cosine"},
            )

        documents = documents or get_all_documents()
        existing_ids = set(self.collection.get()["ids"])
        new_docs = [d for d in documents if d["id"] not in existing_ids]

        if not new_docs:
            logger.info("All documents already embedded. Nothing to add.")
            return 0

        logger.info(f"Embedding {len(new_docs)} documents...")

        ids = [d["id"] for d in new_docs]
        texts = [self._format_for_embedding(d) for d in new_docs]
        metadatas = [
            {
                "title": d["title"],
                "source": d["source"],
                "tags": ",".join(d.get("tags", [])),
            }
            for d in new_docs
        ]

        BATCH = 50
        for i in range(0, len(ids), BATCH):
            self.collection.add(
                ids=ids[i:i+BATCH],
                documents=texts[i:i+BATCH],
                metadatas=metadatas[i:i+BATCH],
            )
            logger.info(f"  Embedded {min(i+BATCH, len(ids))}/{len(ids)} docs")

        logger.success(f"Build complete. Total docs in store: {self.collection.count()}")
        return len(new_docs)

    def _format_for_embedding(self, doc: dict) -> str:
        return f"Title: {doc['title']}\n\n{doc['content']}"

    # ── Search ─────────────────────────────────────────────────────────────

    def search(self, query: str, n: int = 4, tag_filter: str = None) -> list[dict]:
        where = None
        if tag_filter:
            where = {"tags": {"$contains": tag_filter}}

        results = self.collection.query(
            query_texts=[query],
            n_results=min(n, max(self.collection.count(), 1)),
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "title": results["metadatas"][0][i]["title"],
                "source": results["metadatas"][0][i]["source"],
                "tags": results["metadatas"][0][i]["tags"].split(","),
                "content": results["documents"][0][i],
                "distance": round(results["distances"][0][i], 4),
            })
        return output

    def format_for_llm(self, results: list[dict]) -> str:
        if not results:
            return "No relevant documents found."
        sections = []
        for i, r in enumerate(results, 1):
            sections.append(
                f"[Source {i}: {r['title']} — {r['source']}]\n{r['content']}"
            )
        return "\n\n---\n\n".join(sections)

    @property
    def count(self) -> int:
        return self.collection.count()

    def list_all(self) -> list[dict]:
        result = self.collection.get(include=["metadatas"])
        return [
            {"id": id_, **meta}
            for id_, meta in zip(result["ids"], result["metadatas"])
        ]


# ── Singleton ──────────────────────────────────────────────────────────────

_store_instance: VectorStore | None = None

def get_vector_store() -> VectorStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = VectorStore()
    return _store_instance


# ── CLI ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JoSAA Vector Store Manager")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--search", type=str)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    store = VectorStore()

    if args.build:
        store.build(reset=args.reset)

    if args.list:
        docs = store.list_all()
        print(f"\n{len(docs)} documents in store:")
        for d in docs:
            print(f"  [{d['id']}] {d['title']}")

    if args.search:
        print(f"\nSearching: '{args.search}'")
        results = store.search(args.search, n=3)
        for r in results:
            print(f"\n  [{r['distance']:.4f}] {r['title']}")
            print(f"  {r['content'][:250]}...")
