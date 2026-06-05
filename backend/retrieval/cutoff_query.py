"""
backend/retrieval/cutoff_query.py

Structured Query Engine for JoSAA Cutoffs
-------------------------------------------
Handles precise, structured queries against the cutoffs CSV:
  - "What is the closing rank for CSE at IIT Bombay for General category?"
  - "Which NITs can I get with rank 15000 OBC-NCL?"
  - "Show cutoff trends for IIT Delhi CSE from 2019 to 2024"

This is intentionally NOT a vector search — ranks/numbers need exact lookup,
not semantic similarity. The LLM calls this as a tool.
"""

import pandas as pd
from pathlib import Path
from loguru import logger
from dataclasses import dataclass
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
CUTOFFS_CSV = ROOT / "data" / "processed" / "cutoffs.csv"


@dataclass
class CutoffQuery:
    """Structured query parameters. All fields are optional filters."""
    rank: Optional[int] = None                    # user's JEE rank
    institute_type: Optional[str] = None          # "IIT", "NIT", "IIIT", "GFTI"
    institute_name: Optional[str] = None          # partial name match
    program_name: Optional[str] = None            # partial name match
    quota: Optional[str] = None                   # "All India", "Home State", etc.
    category: Optional[str] = None                # "General", "OBC-NCL", "SC", "ST", "EWS"
    gender: Optional[str] = None                  # "Gender-Neutral" or "Female-only..."
    year: Optional[int] = None                    # specific year, defaults to latest
    round_no: Optional[int] = None                # specific round, defaults to final (6)
    top_n: int = 20                               # max results to return


class CutoffQueryEngine:
    """
    Loads the cutoffs CSV once and serves structured queries efficiently.
    Designed to be used as a LangChain tool by the LLM.
    """

    def __init__(self, csv_path: Path = CUTOFFS_CSV):
        if not csv_path.exists():
            raise FileNotFoundError(
                f"Cutoffs CSV not found at {csv_path}. "
                "Run backend/ingest/generate_sample_data.py first."
            )
        logger.info(f"Loading cutoffs from {csv_path}...")
        self.df = pd.read_csv(csv_path)
        self._preprocess()
        logger.success(f"Loaded {len(self.df):,} cutoff rows.")

    def _preprocess(self):
        """Normalize columns for fast querying."""
        self.df["institute_name_lower"] = self.df["institute_name"].str.lower()
        self.df["program_name_lower"] = self.df["program_name"].str.lower()
        self.df["category_lower"] = self.df["category"].str.lower()
        self.df["opening_rank"] = pd.to_numeric(self.df["opening_rank"], errors="coerce")
        self.df["closing_rank"] = pd.to_numeric(self.df["closing_rank"], errors="coerce")
        self.latest_year = int(self.df["year"].max())
        self.final_round = int(self.df["round"].max())

    # ── Public query methods ───────────────────────────────────────────────

    def query(self, q: CutoffQuery) -> pd.DataFrame:
        """
        Main query entry point. Applies all filters and returns results.
        """
        df = self.df.copy()

        # Default to latest year + final round
        year = q.year or self.latest_year
        round_no = q.round_no or self.final_round

        df = df[(df["year"] == year) & (df["round"] == round_no)]

        if q.institute_type:
            df = df[df["institute_type"].str.upper() == q.institute_type.upper()]

        if q.institute_name:
            df = df[df["institute_name_lower"].str.contains(
                q.institute_name.lower(), na=False
            )]

        if q.program_name:
            df = df[df["program_name_lower"].str.contains(
                q.program_name.lower(), na=False
            )]

        if q.quota:
            df = df[df["quota"].str.lower() == q.quota.lower()]

        if q.category:
            df = df[df["category_lower"] == q.category.lower()]

        if q.gender:
            # flexible: "female" matches "Female-only (including Supernumerary)"
            df = df[df["gender"].str.lower().str.contains(q.gender.lower(), na=False)]

        # Rank-based filter: show programs where closing_rank >= user's rank
        # (user can get in if their rank is within closing rank)
        if q.rank:
            df = df[df["closing_rank"] >= q.rank]
            df = df.sort_values("closing_rank")  # best matches first

        result = df.drop(columns=["institute_name_lower", "program_name_lower", "category_lower"])
        return result.head(q.top_n)

    def get_institute_programs(self, institute_partial: str, year: int = None) -> pd.DataFrame:
        """Get all programs offered by an institute."""
        year = year or self.latest_year
        df = self.df[
            (self.df["year"] == year) &
            (self.df["round"] == self.final_round) &
            (self.df["institute_name_lower"].str.contains(institute_partial.lower(), na=False))
        ]
        return df.drop(columns=["institute_name_lower", "program_name_lower", "category_lower"])

    def get_trend(
        self,
        institute_partial: str,
        program_partial: str,
        category: str = "General",
        gender: str = "Gender-Neutral",
        quota: str = "All India",
    ) -> pd.DataFrame:
        """
        Returns year-over-year closing rank trend for a specific branch/institute combo.
        Useful for: "How has IIT Bombay CSE General cutoff changed over the years?"
        """
        df = self.df[
            self.df["institute_name_lower"].str.contains(institute_partial.lower(), na=False) &
            self.df["program_name_lower"].str.contains(program_partial.lower(), na=False) &
            (self.df["category_lower"] == category.lower()) &
            self.df["gender"].str.lower().str.contains(gender.lower(), na=False) &
            (self.df["quota"].str.lower() == quota.lower()) &
            (self.df["round"] == self.final_round)
        ]
        return (
            df[["year", "opening_rank", "closing_rank"]]
            .sort_values("year")
            .drop(columns=["institute_name_lower", "program_name_lower", "category_lower"], errors="ignore")
        )

    def format_for_llm(self, df: pd.DataFrame, max_rows: int = 15) -> str:
        """
        Convert query results to a clean string the LLM can reason over.
        Keeps it concise to avoid blowing the context window.
        """
        if df.empty:
            return "No results found for the given filters."

        df = df.head(max_rows)
        lines = []
        for _, row in df.iterrows():
            lines.append(
                f"• {row.get('institute_name', 'N/A')} | {row.get('program_name', 'N/A')} | "
                f"{row.get('category', 'N/A')} | {row.get('gender', 'N/A')} | "
                f"Quota: {row.get('quota', 'N/A')} | "
                f"Opening: {int(row['opening_rank']) if pd.notna(row.get('opening_rank')) else 'N/A'} | "
                f"Closing: {int(row['closing_rank']) if pd.notna(row.get('closing_rank')) else 'N/A'} "
                f"(Year: {int(row.get('year', 0))}, Round: {int(row.get('round', 0))})"
            )

        total = len(df)
        header = f"Found {total} result(s):\n"
        return header + "\n".join(lines)

    # ── Metadata helpers ───────────────────────────────────────────────────

    def list_institutes(self, type_filter: str = None) -> list[str]:
        df = self.df
        if type_filter:
            df = df[df["institute_type"].str.upper() == type_filter.upper()]
        return sorted(df["institute_name"].unique().tolist())

    def list_programs(self, institute_partial: str = None) -> list[str]:
        df = self.df
        if institute_partial:
            df = df[df["institute_name_lower"].str.contains(institute_partial.lower(), na=False)]
        return sorted(df["program_name"].unique().tolist())

    @property
    def stats(self) -> dict:
        return {
            "total_rows": len(self.df),
            "years": sorted(self.df["year"].unique().tolist()),
            "rounds": sorted(self.df["round"].unique().tolist()),
            "institutes": self.df["institute_name"].nunique(),
            "programs": self.df["program_name"].nunique(),
            "categories": sorted(self.df["category"].unique().tolist()),
            "latest_year": self.latest_year,
        }


# ── Singleton for reuse across the app ────────────────────────────────────
_engine_instance: CutoffQueryEngine | None = None

def get_engine() -> CutoffQueryEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = CutoffQueryEngine()
    return _engine_instance


# ── Quick test ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    engine = get_engine()
    print("Engine stats:", engine.stats)
    print()

    # Test 1: What can I get with rank 1500 General?
    q = CutoffQuery(rank=1500, category="General", gender="Gender-Neutral", quota="All India")
    result = engine.query(q)
    print("=== Rank 1500 General All India ===")
    print(engine.format_for_llm(result))
    print()

    # Test 2: IIT Bombay all programs
    result2 = engine.get_institute_programs("bombay")
    print(f"=== IIT Bombay programs ({len(result2)} rows) ===")
    print(result2[["program_name", "category", "closing_rank"]].head(8).to_string(index=False))
    print()

    # Test 3: CSE trend at IIT Delhi
    trend = engine.get_trend("delhi", "computer science", category="General")
    print("=== IIT Delhi CSE General Trend ===")
    print(trend.to_string(index=False))
