"""
backend/ingest/generate_sample_data.py

Generates realistic sample JoSAA cutoff data for local development.
Run this FIRST before real scraping so you can test the full pipeline immediately.

Usage:
    python backend/ingest/generate_sample_data.py
"""

import random
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ── Sample data definitions ────────────────────────────────────────────────

IIT_INSTITUTES = [
    "Indian Institute of Technology Bombay",
    "Indian Institute of Technology Delhi",
    "Indian Institute of Technology Madras",
    "Indian Institute of Technology Kharagpur",
    "Indian Institute of Technology Kanpur",
    "Indian Institute of Technology Roorkee",
    "Indian Institute of Technology Hyderabad",
    "Indian Institute of Technology Gandhinagar",
    "Indian Institute of Technology Jodhpur",
    "Indian Institute of Technology Patna",
]

NIT_INSTITUTES = [
    "National Institute of Technology Trichy",
    "National Institute of Technology Warangal",
    "National Institute of Technology Surathkal",
    "National Institute of Technology Calicut",
    "National Institute of Technology Rourkela",
    "Motilal Nehru National Institute of Technology Allahabad",
    "National Institute of Technology Kurukshetra",
]

IIIT_INSTITUTES = [
    "Indian Institute of Information Technology Allahabad",
    "Indian Institute of Information Technology Hyderabad",
    "Indian Institute of Information Technology Delhi",
    "Indian Institute of Information Technology Gwalior",
]

IIT_PROGRAMS = [
    "Computer Science and Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Aerospace Engineering",
    "Engineering Physics",
    "Mathematics and Computing",
    "Data Science and Artificial Intelligence",
    "Electrical Engineering (Power)",
]

NIT_PROGRAMS = [
    "Computer Science and Engineering",
    "Electronics and Communication Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical Engineering",
    "Information Technology",
    "Chemical Engineering",
    "Production and Industrial Engineering",
]

CATEGORIES = ["General", "OBC-NCL", "SC", "ST", "EWS"]
GENDERS = ["Gender-Neutral", "Female-only (including Supernumerary)"]
QUOTAS_IIT = ["All India"]
QUOTAS_NIT = ["All India", "Home State", "Other State"]
YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
ROUNDS = [1, 2, 3, 4, 5, 6]

# Approximate closing rank ranges by category (General → ST gets easier)
CATEGORY_RANK_MULTIPLIERS = {
    "General": 1.0,
    "EWS": 1.3,
    "OBC-NCL": 1.8,
    "SC": 4.0,
    "ST": 8.0,
}

# Base closing ranks for IIT programs (General, Round 6)
IIT_BASE_RANKS = {
    "Computer Science and Engineering": 100,
    "Mathematics and Computing": 400,
    "Electrical Engineering": 800,
    "Engineering Physics": 1200,
    "Data Science and Artificial Intelligence": 600,
    "Aerospace Engineering": 2000,
    "Chemical Engineering": 3000,
    "Mechanical Engineering": 2500,
    "Civil Engineering": 4000,
    "Electrical Engineering (Power)": 3500,
}

# IIT rank multiplier by institute prestige
IIT_PRESTIGE = {
    "Indian Institute of Technology Bombay": 1.0,
    "Indian Institute of Technology Delhi": 1.1,
    "Indian Institute of Technology Madras": 1.15,
    "Indian Institute of Technology Kharagpur": 1.3,
    "Indian Institute of Technology Kanpur": 1.2,
    "Indian Institute of Technology Roorkee": 1.5,
    "Indian Institute of Technology Hyderabad": 2.0,
    "Indian Institute of Technology Gandhinagar": 2.5,
    "Indian Institute of Technology Jodhpur": 3.0,
    "Indian Institute of Technology Patna": 3.5,
}

NIT_BASE_RANKS = {
    "Computer Science and Engineering": 5000,
    "Electronics and Communication Engineering": 12000,
    "Information Technology": 15000,
    "Electrical Engineering": 20000,
    "Mechanical Engineering": 25000,
    "Civil Engineering": 35000,
    "Chemical Engineering": 30000,
    "Production and Industrial Engineering": 40000,
}

NIT_PRESTIGE = {
    "National Institute of Technology Trichy": 1.0,
    "National Institute of Technology Warangal": 1.1,
    "National Institute of Technology Surathkal": 1.2,
    "National Institute of Technology Calicut": 1.3,
    "National Institute of Technology Rourkela": 1.4,
    "Motilal Nehru National Institute of Technology Allahabad": 1.5,
    "National Institute of Technology Kurukshetra": 1.8,
}


def jitter(val: int, pct: float = 0.08) -> int:
    """Add ±pct% noise to simulate yearly rank variation."""
    return max(1, int(val * random.uniform(1 - pct, 1 + pct)))


def generate_rows():
    rows = []
    random.seed(42)

    for year in YEARS:
        year_factor = 1.0 + (year - 2019) * 0.02  # slight rank inflation over years

        for institute in IIT_INSTITUTES + NIT_INSTITUTES + IIIT_INSTITUTES:
            is_iit = "Indian Institute of Technology" in institute
            is_iiit = "Indian Institute of Information Technology" in institute

            programs = IIT_PROGRAMS if is_iit else NIT_PROGRAMS
            base_ranks = IIT_BASE_RANKS if is_iit else NIT_BASE_RANKS
            prestige_map = IIT_PRESTIGE if is_iit else NIT_PRESTIGE
            quotas = QUOTAS_IIT if is_iit else QUOTAS_NIT
            prestige = prestige_map.get(institute, 2.0)
            inst_type = "IIT" if is_iit else ("IIIT" if is_iiit else "NIT")

            for program in programs:
                base_close = base_ranks.get(program, 20000)

                for quota in quotas:
                    quota_factor = 1.0 if quota == "All India" else (0.9 if quota == "Home State" else 1.2)

                    for category in CATEGORIES:
                        cat_mult = CATEGORY_RANK_MULTIPLIERS[category]

                        for gender in GENDERS:
                            gender_factor = 1.15 if "Female" in gender else 1.0

                            # Closing rank for Round 6 (final allotment)
                            close_r6 = int(
                                base_close * prestige * cat_mult
                                * quota_factor * gender_factor * year_factor
                            )

                            for round_no in ROUNDS:
                                # Earlier rounds have slightly tighter cutoffs
                                round_factor = 1.0 + (6 - round_no) * 0.03
                                closing_rank = jitter(int(close_r6 * round_factor))
                                opening_rank = max(1, jitter(int(closing_rank * 0.6)))

                                rows.append({
                                    "year": year,
                                    "round": round_no,
                                    "institute_name": institute,
                                    "institute_type": inst_type,
                                    "program_name": program,
                                    "quota": quota,
                                    "category": category,
                                    "gender": gender,
                                    "opening_rank": opening_rank,
                                    "closing_rank": closing_rank,
                                })
    return rows


def main():
    print("Generating sample JoSAA cutoff data...")
    rows = generate_rows()
    df = pd.DataFrame(rows)
    df = df.sort_values(["year", "round", "institute_name", "program_name"])

    output_path = PROCESSED_DIR / "cutoffs.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Generated {len(df):,} rows → {output_path}")
    print(f"   Institutes : {df['institute_name'].nunique()}")
    print(f"   Programs   : {df['program_name'].nunique()}")
    print(f"   Years      : {sorted(df['year'].unique())}")
    print(f"   Categories : {sorted(df['category'].unique())}")
    print()
    print("Sample rows:")
    print(df[df["institute_name"].str.contains("Bombay") & (df["year"] == 2024) & (df["round"] == 6)].head(5).to_string(index=False))


if __name__ == "__main__":
    main()
