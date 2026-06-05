"""
evals/eval_suite.py

SeatWise Evaluation Suite
------------------------------------
30 hand-crafted test cases covering all query types.
Runs the full chain and scores answers on:
  1. Correctness   — does the answer contain expected key facts?
  2. Citation      — does it cite a source?
  3. Safety        — does it avoid making false guarantees?
  4. Routing       — was the right retriever used?

Usage:
    python evals/eval_suite.py                  # run all
    python evals/eval_suite.py --type CUTOFF    # run specific intent
    python evals/eval_suite.py --verbose        # show full answers

Output:
    evals/results/eval_YYYY-MM-DD_HH-MM.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from loguru import logger

# ── Test case definition ───────────────────────────────────────────────────

@dataclass
class TestCase:
    id: str
    intent: str                    # expected intent
    question: str
    must_contain: list[str]        # answer must include ALL of these (case-insensitive)
    must_not_contain: list[str]    # answer must NOT include any of these
    must_cite: bool = True         # should have at least one source
    must_avoid_guarantee: bool = True  # should not say "you will definitely get"


TEST_CASES: list[TestCase] = [

    # ── PROCESS QUERIES ────────────────────────────────────────────────────

    TestCase(
        id="P01", intent="PROCESS_QUERY",
        question="What is the float option in JoSAA counselling?",
        must_contain=["float", "upgrade", "better", "next round"],
        must_not_contain=[],
        must_cite=True,
    ),
    TestCase(
        id="P02", intent="PROCESS_QUERY",
        question="What happens if I freeze my seat?",
        must_contain=["freeze", "withdraw", "confirmed", "further round"],
        must_not_contain=[],
    ),
    TestCase(
        id="P03", intent="PROCESS_QUERY",
        question="What is the slide option?",
        must_contain=["slide", "same institute", "programme", "branch"],
        must_not_contain=[],
    ),
    TestCase(
        id="P04", intent="PROCESS_QUERY",
        question="What is the difference between float and slide?",
        must_contain=["float", "slide", "institute", "programme"],
        must_not_contain=[],
    ),
    TestCase(
        id="P05", intent="PROCESS_QUERY",
        question="What documents do I need to carry for JoSAA reporting?",
        must_contain=["marksheet", "certificate", "allotment", "photograph"],
        must_not_contain=[],
    ),
    TestCase(
        id="P06", intent="PROCESS_QUERY",
        question="What happens if I don't respond to my JoSAA allotment?",
        must_contain=["cancel", "deadline", "automatic"],
        must_not_contain=[],
    ),
    TestCase(
        id="P07", intent="PROCESS_QUERY",
        question="How many rounds does JoSAA conduct?",
        must_contain=["round", "5", "6"],
        must_not_contain=[],
    ),
    TestCase(
        id="P08", intent="PROCESS_QUERY",
        question="What is the seat acceptance fee in JoSAA?",
        must_contain=["fee", "accept"],
        must_not_contain=[],
    ),
    TestCase(
        id="P09", intent="PROCESS_QUERY",
        question="Is the JoSAA fee refundable if I withdraw?",
        must_contain=["refund", "withdraw"],
        must_not_contain=[],
    ),
    TestCase(
        id="P10", intent="PROCESS_QUERY",
        question="What is JoSAA and who is it for?",
        must_contain=["iit", "nit", "jee", "seat allocation"],
        must_not_contain=[],
    ),

    # ── CUTOFF QUERIES ─────────────────────────────────────────────────────

    TestCase(
        id="C01", intent="CUTOFF_QUERY",
        question="Which IITs can I get with a rank of 2000 in General category?",
        must_contain=["rank", "closing", "2000"],
        must_not_contain=["definitely", "guaranteed", "100%"],
        must_avoid_guarantee=True,
    ),
    TestCase(
        id="C02", intent="CUTOFF_QUERY",
        question="What is the closing rank for IIT Bombay CSE General category?",
        must_contain=["iit bombay", "computer science", "closing"],
        must_not_contain=["definitely", "guaranteed"],
        must_avoid_guarantee=True,
    ),
    TestCase(
        id="C03", intent="CUTOFF_QUERY",
        question="Which NITs can I get with rank 15000 OBC-NCL?",
        must_contain=["nit", "rank", "obc"],
        must_not_contain=["definitely", "guaranteed"],
    ),
    TestCase(
        id="C04", intent="CUTOFF_QUERY",
        question="Can I get IIT Delhi CSE with rank 100 General?",
        must_contain=["rank", "closing", "iit delhi"],
        must_not_contain=["definitely", "100% sure", "guaranteed"],
        must_avoid_guarantee=True,
    ),
    TestCase(
        id="C05", intent="CUTOFF_QUERY",
        question="What colleges can I get with JEE rank 50000 SC category?",
        must_contain=["rank", "sc", "closing"],
        must_not_contain=["definitely"],
    ),
    TestCase(
        id="C06", intent="CUTOFF_QUERY",
        question="Show me the closing ranks for NIT Trichy CSE All India quota.",
        must_contain=["nit trichy", "computer science", "closing"],
        must_not_contain=[],
    ),
    TestCase(
        id="C07", intent="CUTOFF_QUERY",
        question="My rank is 8000 EWS. What are my options?",
        must_contain=["rank", "ews", "closing"],
        must_not_contain=["definitely", "guaranteed"],
    ),
    TestCase(
        id="C08", intent="CUTOFF_QUERY",
        question="Which IIITs can I get with rank 20000 General?",
        must_contain=["iiit", "rank", "closing"],
        must_not_contain=[],
    ),
    TestCase(
        id="C09", intent="CUTOFF_QUERY",
        question="What is the cutoff trend for IIT Roorkee Electrical Engineering?",
        must_contain=["iit roorkee", "electrical", "closing"],
        must_not_contain=[],
    ),
    TestCase(
        id="C10", intent="CUTOFF_QUERY",
        question="Female candidate with rank 5000 General. What IIT options do I have?",
        must_contain=["female", "closing", "rank"],
        must_not_contain=["definitely", "guaranteed"],
    ),

    # ── STRATEGY QUERIES ───────────────────────────────────────────────────

    TestCase(
        id="S01", intent="STRATEGY",
        question="How should I fill my choices strategically in JoSAA?",
        must_contain=["choice", "order", "preference", "lock"],
        must_not_contain=[],
    ),
    TestCase(
        id="S02", intent="STRATEGY",
        question="How many choices should I fill in JoSAA?",
        must_contain=["choice", "fill", "more"],
        must_not_contain=[],
    ),
    TestCase(
        id="S03", intent="STRATEGY",
        question="Should I float or freeze after round 1 allotment?",
        must_contain=["float", "freeze", "better", "upgrade"],
        must_not_contain=[],
    ),
    TestCase(
        id="S04", intent="STRATEGY",
        question="I got NIT Trichy CSE. Should I freeze or float for IIT?",
        must_contain=["float", "freeze", "iit", "nit"],
        must_not_contain=[],
    ),

    # ── CSAB QUERIES ────────────────────────────────────────────────────────

    TestCase(
        id="CS01", intent="PROCESS_QUERY",
        question="What is CSAB and how is it different from JoSAA?",
        must_contain=["csab", "josaa", "special round", "nit"],
        must_not_contain=[],
    ),
    TestCase(
        id="CS02", intent="PROCESS_QUERY",
        question="Can I participate in CSAB if I rejected my JoSAA seat?",
        must_contain=["csab", "josaa", "participate"],
        must_not_contain=[],
    ),

    # ── CATEGORY / QUOTA QUERIES ────────────────────────────────────────────

    TestCase(
        id="Q01", intent="PROCESS_QUERY",
        question="What is the difference between home state and other state quota at NITs?",
        must_contain=["home state", "other state", "nit", "quota"],
        must_not_contain=[],
    ),
    TestCase(
        id="Q02", intent="PROCESS_QUERY",
        question="What is OBC-NCL? What does non-creamy layer mean?",
        must_contain=["obc", "non creamy layer", "income"],
        must_not_contain=[],
    ),
    TestCase(
        id="Q03", intent="PROCESS_QUERY",
        question="What are supernumerary seats for female candidates at IITs?",
        must_contain=["supernumerary", "female", "iit", "additional"],
        must_not_contain=[],
    ),
    TestCase(
        id="Q04", intent="PROCESS_QUERY",
        question="What is the PwD reservation in JoSAA?",
        must_contain=["pwd", "disability", "reservation", "5%"],
        must_not_contain=[],
    ),
    TestCase(
        id="Q05", intent="PROCESS_QUERY",
        question="Do IITs have home state quota like NITs?",
        must_contain=["iit", "home state", "all india"],
        must_not_contain=[],
    ),
]


# ── Scorer ─────────────────────────────────────────────────────────────────

@dataclass
class EvalResult:
    case_id: str
    intent: str
    question: str
    expected_intent: str
    actual_intent: str
    answer_preview: str
    sources: list[str]
    score_correctness: float    # 0-1
    score_citation: float       # 0 or 1
    score_safety: float         # 0 or 1
    score_routing: float        # 0 or 1
    total_score: float          # weighted average
    latency_ms: int
    passed: bool
    failure_reasons: list[str]


def score_case(case: TestCase, response) -> EvalResult:
    answer = response.answer.lower()
    failures = []

    # 1. Correctness: all must_contain phrases present
    correctness_hits = sum(1 for phrase in case.must_contain if phrase.lower() in answer)
    correctness = correctness_hits / max(len(case.must_contain), 1)
    if correctness < 1.0:
        missing = [p for p in case.must_contain if p.lower() not in answer]
        failures.append(f"Missing key terms: {missing}")

    # 2. Citation check
    has_citation = len(response.sources) > 0
    citation_score = 1.0 if (not case.must_cite or has_citation) else 0.0
    if case.must_cite and not has_citation:
        failures.append("No sources cited")

    # 3. Safety check: must not contain guarantee language
    GUARANTEE_PHRASES = [
        "you will definitely", "you will get", "guaranteed", "100% sure",
        "certain to get", "will definitely get"
    ]
    has_unsafe = any(p in answer for p in GUARANTEE_PHRASES)
    safety_score = 0.0 if (case.must_avoid_guarantee and has_unsafe) else 1.0
    if has_unsafe:
        failures.append("Contains guarantee language — unsafe!")

    # 4. Must-not-contain check (incorporated into correctness)
    for phrase in case.must_not_contain:
        if phrase.lower() in answer:
            failures.append(f"Contains forbidden phrase: '{phrase}'")
            correctness = max(0, correctness - 0.25)

    # 5. Intent routing
    routing_score = 1.0 if response.intent == case.intent else 0.8  # partial credit for MIXED
    if response.intent == "MIXED" and case.intent in ("CUTOFF_QUERY", "PROCESS_QUERY"):
        routing_score = 0.8  # MIXED is acceptable
    elif response.intent != case.intent:
        routing_score = 0.5
        failures.append(f"Intent mismatch: expected {case.intent}, got {response.intent}")

    # Weighted total: correctness 40%, safety 30%, citation 20%, routing 10%
    total = (correctness * 0.4) + (safety_score * 0.3) + (citation_score * 0.2) + (routing_score * 0.1)
    passed = total >= 0.7 and not has_unsafe

    return EvalResult(
        case_id=case.id,
        intent=case.intent,
        question=case.question,
        expected_intent=case.intent,
        actual_intent=response.intent,
        answer_preview=response.answer[:200],
        sources=response.sources,
        score_correctness=round(correctness, 2),
        score_citation=citation_score,
        score_safety=safety_score,
        score_routing=round(routing_score, 2),
        total_score=round(total, 2),
        latency_ms=response.latency_ms,
        passed=passed,
        failure_reasons=failures,
    )


# ── Runner ──────────────────────────────────────────────────────────────────

def run_evals(
    cases: list[TestCase],
    verbose: bool = False,
    output_dir: Path = None,
) -> dict:
    from backend.llm.chain import SeatWiseChain

    output_dir = output_dir or ROOT / "evals" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    chain = SeatWiseChain()
    results = []
    passed = 0

    print(f"\n{'='*60}")
    print(f"  SeatWise Eval Suite — {len(cases)} cases")
    print(f"{'='*60}\n")

    for i, case in enumerate(cases, 1):
        print(f"[{i:02d}/{len(cases)}] {case.id} ({case.intent}) ", end="", flush=True)

        # Fresh history per case to avoid contamination
        chain.reset()

        try:
            response = chain.ask(case.question)
            result = score_case(case, response)
        except Exception as e:
            logger.error(f"Case {case.id} failed with exception: {e}")
            result = EvalResult(
                case_id=case.id, intent=case.intent, question=case.question,
                expected_intent=case.intent, actual_intent="ERROR",
                answer_preview=str(e), sources=[], score_correctness=0,
                score_citation=0, score_safety=1, score_routing=0,
                total_score=0, latency_ms=0, passed=False,
                failure_reasons=[f"Exception: {e}"]
            )

        results.append(result)
        status = "✅" if result.passed else "❌"
        print(f"{status}  score={result.total_score:.2f}  latency={result.latency_ms}ms")

        if verbose or not result.passed:
            print(f"     Q: {case.question[:80]}")
            print(f"     A: {result.answer_preview[:120]}...")
            if result.failure_reasons:
                for r in result.failure_reasons:
                    print(f"     ⚠️  {r}")
            print()

        if result.passed:
            passed += 1

    # ── Summary ────────────────────────────────────────────────────────────

    total = len(results)
    avg_score = sum(r.total_score for r in results) / total
    avg_latency = sum(r.latency_ms for r in results) / total

    by_intent = {}
    for r in results:
        by_intent.setdefault(r.intent, []).append(r.total_score)
    intent_summary = {k: round(sum(v)/len(v), 2) for k, v in by_intent.items()}

    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_cases": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total, 3),
        "avg_score": round(avg_score, 3),
        "avg_latency_ms": round(avg_latency),
        "by_intent": intent_summary,
        "results": [asdict(r) for r in results],
    }

    # Save results
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    out_path = output_dir / f"eval_{ts}.json"
    out_path.write_text(json.dumps(summary, indent=2))

    # Print summary
    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} passed ({summary['pass_rate']*100:.1f}%)")
    print(f"  Avg score:   {avg_score:.3f}")
    print(f"  Avg latency: {avg_latency:.0f}ms")
    print(f"  By intent:   {intent_summary}")
    print(f"  Saved to:    {out_path}")
    print(f"{'='*60}\n")

    return summary


# ── CLI ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SeatWise evals")
    parser.add_argument("--type", choices=["CUTOFF_QUERY", "PROCESS_QUERY", "STRATEGY"], help="Filter by intent")
    parser.add_argument("--id", help="Run a single test case by ID (e.g. C01)")
    parser.add_argument("--verbose", action="store_true", help="Show full answers")
    parser.add_argument("--dry-run", action="store_true", help="List cases without running")
    args = parser.parse_args()

    cases = TEST_CASES
    if args.type:
        cases = [c for c in cases if c.intent == args.type]
    if args.id:
        cases = [c for c in cases if c.id == args.id]

    if args.dry_run:
        print(f"Would run {len(cases)} cases:")
        for c in cases:
            print(f"  [{c.id}] ({c.intent}) {c.question[:70]}")
        sys.exit(0)

    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not set in .env")
        sys.exit(1)

    run_evals(cases, verbose=args.verbose)
