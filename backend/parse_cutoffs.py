"""
backend/ingest/parse_cutoffs.py

Phase 1 — JoSAA Cutoff Data Parser
------------------------------------
Handles two data sources:
  1. Official JoSAA cutoff PDFs (downloaded locally)
  2. josaa.nic.in opening/closing rank tables (scraped)

Output: data/processed/cutoffs.csv with a clean, normalized schema.

Schema:
  year, round, institute_code, institute_name, institute_type,
  program_code, program_name, quota, category, gender,
  opening_rank, closing_rank
"""

import re
import time
import requests
import pdfplumber
import pandas as pd
from pathlib import Path
from loguru import logger
from bs4 import BeautifulSoup

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = PROCESSED_DIR / "cutoffs.csv"

# ── Constants ──────────────────────────────────────────────────────────────
JOSAA_BASE = "https://josaa.nic.in"
YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
ROUNDS = [1, 2, 3, 4, 5, 6]

INSTITUTE_TYPE_MAP = {
    "IIT": "IIT",
    "NIT": "NIT",
    "IIIT": "IIIT",
    "GFTI": "GFTI",
}

CATEGORY_NORMALIZE = {
    "OPEN": "General",
    "GEN": "General",
    "OBC-NCL": "OBC-NCL",
    "OBC": "OBC-NCL",
    "SC": "SC",
    "ST": "ST",
    "EWS": "EWS",
    "OPEN (PwD)": "General-PwD",
    "OBC-NCL (PwD)": "OBC-NCL-PwD",
    "SC (PwD)": "SC-PwD",
    "ST (PwD)": "ST-PwD",
    "EWS (PwD)": "EWS-PwD",
}

QUOTA_NORMALIZE = {
    "AI": "All India",
    "HS": "Home State",
    "OS": "Other State",
    "GO": "Goa",
    "JK": "J&K",
    "LA": "Ladakh",
}


# ── Utility helpers ────────────────────────────────────────────────────────

def normalize_rank(val: str) -> int | None:
    """Convert rank string to int, handling edge cases like 'P100' (prepared)."""
    if pd.isna(val) or str(val).strip() in ("", "-", "NA", "N/A"):
        return None
    cleaned = re.sub(r"[^\d]", "", str(val))
    return int(cleaned) if cleaned else None


def detect_institute_type(name: str) -> str:
    name_upper = name.upper()
    for key, val in INSTITUTE_TYPE_MAP.items():
        if key in name_upper:
            return val
    return "GFTI"


def normalize_category(raw: str) -> str:
    raw = raw.strip().upper()
    for k, v in CATEGORY_NORMALIZE.items():
        if k.upper() == raw:
            return v
    return raw  # return as-is if not found


def normalize_quota(raw: str) -> str:
    raw = raw.strip().upper()
    return QUOTA_NORMALIZE.get(raw, raw)


# ── PDF Parser ─────────────────────────────────────────────────────────────

class PDFCutoffParser:
    """
    Parses JoSAA cutoff PDFs downloaded from josaa.nic.in.
    
    JoSAA PDFs typically have tables with columns:
    Institute | Program | Quota | Category | Gender | Opening Rank | Closing Rank
    
    Usage:
        parser = PDFCutoffParser(year=2024, round_no=6)
        df = parser.parse(pdf_path)
    """

    EXPECTED_COLS = [
        "institute", "program", "quota", "category",
        "gender", "opening_rank", "closing_rank"
    ]

    def __init__(self, year: int, round_no: int):
        self.year = year
        self.round_no = round_no

    def parse(self, pdf_path: Path) -> pd.DataFrame:
        logger.info(f"Parsing PDF: {pdf_path}")
        rows = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if not table:
                    continue

                # Find header row
                header_idx = self._find_header(table)
                if header_idx is None:
                    continue

                col_map = self._map_columns(table[header_idx])

                for row in table[header_idx + 1:]:
                    parsed = self._parse_row(row, col_map)
                    if parsed:
                        rows.append(parsed)

        df = pd.DataFrame(rows)
        df["year"] = self.year
        df["round"] = self.round_no
        logger.success(f"  → {len(df)} rows parsed from {pdf_path.name}")
        return df

    def _find_header(self, table: list) -> int | None:
        for i, row in enumerate(table):
            row_text = " ".join(str(c).lower() for c in row if c)
            if "institute" in row_text and "rank" in row_text:
                return i
        return None

    def _map_columns(self, header_row: list) -> dict:
        """Map column indices to our normalized names."""
        mapping = {}
        for i, cell in enumerate(header_row):
            if not cell:
                continue
            cell_lower = str(cell).lower().strip()
            if "institute" in cell_lower:
                mapping["institute"] = i
            elif "program" in cell_lower or "branch" in cell_lower:
                mapping["program"] = i
            elif "quota" in cell_lower:
                mapping["quota"] = i
            elif "category" in cell_lower or "seat type" in cell_lower:
                mapping["category"] = i
            elif "gender" in cell_lower:
                mapping["gender"] = i
            elif "opening" in cell_lower:
                mapping["opening_rank"] = i
            elif "closing" in cell_lower:
                mapping["closing_rank"] = i
        return mapping

    def _parse_row(self, row: list, col_map: dict) -> dict | None:
        try:
            institute = str(row[col_map["institute"]]).strip() if "institute" in col_map else ""
            program = str(row[col_map["program"]]).strip() if "program" in col_map else ""

            if not institute or not program or institute.lower() in ("institute", ""):
                return None

            return {
                "institute_name": institute,
                "institute_type": detect_institute_type(institute),
                "program_name": program,
                "quota": normalize_quota(str(row[col_map.get("quota", 0)] or "")),
                "category": normalize_category(str(row[col_map.get("category", 0)] or "")),
                "gender": str(row[col_map.get("gender", 0)] or "").strip(),
                "opening_rank": normalize_rank(row[col_map.get("opening_rank", 0)]),
                "closing_rank": normalize_rank(row[col_map.get("closing_rank", 0)]),
            }
        except (IndexError, KeyError, TypeError):
            return None


# ── Web Scraper (fallback for years without PDFs) ──────────────────────────

class JoSAAScraper:
    """
    Scrapes opening/closing ranks directly from josaa.nic.in result pages.
    Used as fallback when PDFs are not available or are scanned images.
    
    NOTE: JoSAA changes their site structure yearly — inspect the live site
    and update RESULT_URL_TEMPLATE accordingly before each counselling cycle.
    """

    RESULT_URL_TEMPLATE = (
        "https://josaa.nic.in/result/candidate/currentorcr.aspx"
        "?rid={round}&type=1&Year={year}"
    )
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
        )
    }

    def __init__(self, year: int, round_no: int, delay: float = 1.5):
        self.year = year
        self.round_no = round_no
        self.delay = delay  # be polite to the server

    def scrape(self) -> pd.DataFrame:
        url = self.RESULT_URL_TEMPLATE.format(round=self.round_no, year=self.year)
        logger.info(f"Scraping: {url}")

        try:
            resp = requests.get(url, headers=self.HEADERS, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return pd.DataFrame()

        time.sleep(self.delay)
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_GridView1"})

        if not table:
            logger.warning(f"No table found for year={self.year} round={self.round_no}")
            return pd.DataFrame()

        rows = []
        headers = [th.get_text(strip=True) for th in table.find_all("th")]

        for tr in table.find_all("tr")[1:]:  # skip header
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            if len(cells) < 7:
                continue
            rows.append(dict(zip(headers, cells)))

        df = pd.DataFrame(rows)
        df = self._normalize_scraped(df)
        df["year"] = self.year
        df["round"] = self.round_no
        logger.success(f"  → {len(df)} rows scraped for {self.year} R{self.round_no}")
        return df

    def _normalize_scraped(self, df: pd.DataFrame) -> pd.DataFrame:
        rename_map = {
            "Institute": "institute_name",
            "Academic Program Name": "program_name",
            "Quota": "quota",
            "Seat Type": "category",
            "Gender": "gender",
            "Opening Rank": "opening_rank",
            "Closing Rank": "closing_rank",
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

        if "institute_name" in df.columns:
            df["institute_type"] = df["institute_name"].apply(detect_institute_type)
        if "quota" in df.columns:
            df["quota"] = df["quota"].apply(normalize_quota)
        if "category" in df.columns:
            df["category"] = df["category"].apply(normalize_category)
        if "opening_rank" in df.columns:
            df["opening_rank"] = df["opening_rank"].apply(normalize_rank)
        if "closing_rank" in df.columns:
            df["closing_rank"] = df["closing_rank"].apply(normalize_rank)

        return df


# ── Orchestrator ───────────────────────────────────────────────────────────

def build_cutoff_dataset(
    pdf_dir: Path = RAW_DIR,
    years: list = YEARS,
    rounds: list = ROUNDS,
    scrape_fallback: bool = True,
) -> pd.DataFrame:
    """
    Master function: parse all available PDFs, scrape missing years.
    Merges everything into one clean DataFrame and saves to CSV.
    """
    all_dfs = []

    # 1. Parse local PDFs if they exist
    # Expected naming: raw/josaa_2024_round6.pdf
    for pdf_path in sorted(pdf_dir.glob("josaa_*.pdf")):
        match = re.match(r"josaa_(\d{4})_round(\d+)\.pdf", pdf_path.name)
        if not match:
            logger.warning(f"Unrecognized filename format: {pdf_path.name}, skipping.")
            continue
        year, round_no = int(match.group(1)), int(match.group(2))
        parser = PDFCutoffParser(year=year, round_no=round_no)
        df = parser.parse(pdf_path)
        if not df.empty:
            all_dfs.append(df)

    # 2. Scrape fallback for years/rounds not covered by PDFs
    if scrape_fallback:
        parsed_combos = {
            (int(d["year"].iloc[0]), int(d["round"].iloc[0]))
            for d in all_dfs if not d.empty
        }
        for year in years:
            for round_no in rounds:
                if (year, round_no) not in parsed_combos:
                    scraper = JoSAAScraper(year=year, round_no=round_no)
                    df = scraper.scrape()
                    if not df.empty:
                        all_dfs.append(df)

    if not all_dfs:
        logger.error("No data collected. Check PDF dir or network access.")
        return pd.DataFrame()

    # 3. Merge + clean
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df = final_df.drop_duplicates()
    final_df = final_df.dropna(subset=["institute_name", "program_name", "closing_rank"])

    # Enforce column order
    col_order = [
        "year", "round", "institute_name", "institute_type",
        "program_name", "quota", "category", "gender",
        "opening_rank", "closing_rank",
    ]
    final_df = final_df[[c for c in col_order if c in final_df.columns]]
    final_df = final_df.sort_values(["year", "round", "institute_name", "program_name"])

    final_df.to_csv(OUTPUT_CSV, index=False)
    logger.success(f"Saved {len(final_df)} rows → {OUTPUT_CSV}")
    return final_df


# ── CLI entry point ────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="JoSAA Cutoff Data Parser")
    parser.add_argument("--pdf-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--no-scrape", action="store_true", help="Skip web scraping")
    parser.add_argument("--years", nargs="+", type=int, default=YEARS)
    args = parser.parse_args()

    df = build_cutoff_dataset(
        pdf_dir=args.pdf_dir,
        years=args.years,
        scrape_fallback=not args.no_scrape,
    )
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"Institutes: {df['institute_name'].nunique() if 'institute_name' in df else 'N/A'}")
    print(f"Years covered: {sorted(df['year'].unique()) if 'year' in df else 'N/A'}")
