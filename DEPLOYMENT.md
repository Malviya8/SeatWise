# SeatWise — Deployment Guide

## Option A: Local Dev (Recommended to start)

```bash
# 1. Clone and install
git clone <your-repo>
cd seatwise
pip install -r requirements.txt

# 2. Set up env
cp .env.example .env
# Edit .env → add ANTHROPIC_API_KEY (required)
#            → add OPENAI_API_KEY (optional, better embeddings)

# 3. Generate data + build vector store
python backend/ingest/generate_sample_data.py
python backend/retrieval/vector_store.py --build

# 4. Start backend
uvicorn backend.api.main:app --reload --port 8000

# 5. Start frontend (new terminal)
cd frontend && npm install && npm run dev
# → open http://localhost:5173
```

---

## Option B: Docker Compose (One-command stack)

```bash
# Requires Docker Desktop installed

cp .env.example .env   # fill in API keys

docker compose up --build
# → Backend:  http://localhost:8000
# → Frontend: http://localhost:5173
# → API docs: http://localhost:8000/docs
```

---

## Option C: Deploy to Render + Vercel (Free tier)

### Step 1: Push to GitHub
```bash
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/seatwise
git push -u origin main
```

### Step 2: Deploy backend to Render
1. Go to https://render.com → New → Web Service
2. Connect your GitHub repo
3. Set:
   - **Build command:** `pip install -r requirements.txt && python backend/ingest/generate_sample_data.py && python backend/retrieval/vector_store.py --build`
   - **Start command:** `uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT`
   - **Add disk** → mount at `/opt/render/project/src/data`, 1GB
4. Under Environment → Add:
   - `ANTHROPIC_API_KEY` = your key
   - `OPENAI_API_KEY` = your key (optional)
5. Deploy → copy your Render URL (e.g. `https://josaa-api.onrender.com`)

### Step 3: Deploy frontend to Vercel
1. Go to https://vercel.com → New Project → Import from GitHub
2. Set root directory to `frontend`
3. Under Environment Variables → Add:
   - `VITE_API_URL` = your Render backend URL
4. Deploy → get your frontend URL

### Step 4: Update CORS
In Render dashboard → Environment → update `CORS_ORIGINS` to your Vercel URL.

---

## Running Evals

```bash
# Run all 31 test cases (requires ANTHROPIC_API_KEY)
python evals/eval_suite.py

# Run only cutoff queries
python evals/eval_suite.py --type CUTOFF_QUERY

# Verbose mode (shows full answers)
python evals/eval_suite.py --verbose

# Run a specific case
python evals/eval_suite.py --id C01

# Results saved to evals/results/eval_YYYY-MM-DD_HH-MM.json
```

**Target scores for production readiness:**
- Pass rate ≥ 80%
- Avg score ≥ 0.75
- Zero safety failures (no guarantee language)

---

## Getting Real JoSAA Data

The sample data generator creates realistic but synthetic data.
For real cutoffs, download PDFs from https://josaa.nic.in:

```bash
# Place PDFs in data/raw/ with naming convention:
# josaa_2024_round6.pdf, josaa_2023_round6.pdf etc.

# Then run the real parser
python backend/ingest/parse_cutoffs.py

# This replaces the sample data in data/processed/cutoffs.csv
```

---

## API Quick Reference

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Which IITs can I get with rank 2000 General?"}'

# Direct cutoff query (no LLM)
curl -X POST http://localhost:8000/cutoffs \
  -H "Content-Type: application/json" \
  -d '{"rank": 2000, "category": "General", "institute_type": "IIT"}'

# Year-over-year trend
curl "http://localhost:8000/cutoffs/trend?institute=bombay&program=computer+science&category=General"

# Full API docs
open http://localhost:8000/docs
```
