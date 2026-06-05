"""
backend/ingest/knowledge_base.py

JoSAA / CSAB Knowledge Base
-----------------------------
Contains structured text documents covering:
  - JoSAA process and rules
  - CSAB special rounds
  - Seat allotment logic (float/freeze/slide)
  - Reporting, document verification
  - Common FAQs

These get chunked and embedded into ChromaDB for semantic search.
Add more documents here as you collect official PDFs/circulars.
"""

# Each document is a dict with:
#   id       : unique string ID
#   title    : short title (used in citations)
#   source   : where this came from
#   content  : the actual text to embed
#   tags     : list of topic tags for filtering

KNOWLEDGE_BASE: list[dict] = [

    # ── JOSAA OVERVIEW ──────────────────────────────────────────────────────

    {
        "id": "josaa_overview_001",
        "title": "What is JoSAA?",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["josaa", "overview", "basics"],
        "content": """
JoSAA (Joint Seat Allocation Authority) conducts the joint seat allocation for
admissions to undergraduate programmes at IITs, NITs, IIITs, and other Government
Funded Technical Institutes (GFTIs). It is a joint body formed by the Ministry
of Education (MoE) to centrally manage and administer the seat allocation process
for all these institutes together in one single platform.

Eligibility:
- Candidates must qualify JEE Advanced to be eligible for IIT seats.
- Candidates with JEE Main scores can apply for NIT, IIIT, and GFTI seats.
- Candidates must also meet individual institute eligibility criteria (e.g., 75% in Class 12 or top 20 percentile).

JoSAA typically conducts 5-6 rounds of seat allotment. In each round, candidates
are allotted seats based on their JEE rank, filled choices, category, and seat availability.
        """.strip(),
    },

    {
        "id": "josaa_timeline_001",
        "title": "JoSAA Counselling Timeline and Process",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["josaa", "timeline", "process", "schedule"],
        "content": """
JoSAA counselling happens in the following sequence after JEE Advanced results:

1. REGISTRATION: Candidates register on the JoSAA portal and fill choices (choice filling is free and unlimited during the window).

2. CHOICE FILLING AND LOCKING: Candidates fill and order their preferred institute-programme combinations. The order matters — rank 1 preference is considered first. Choices must be locked before the deadline.

3. ROUND 1 SEAT ALLOTMENT: Based on JEE ranks and filled choices, the first provisional allotment is made.

4. ACCEPT SEAT / PAY FEE: After each round, candidates must log in and respond to their allotment:
   - "Freeze" — accept the seat and withdraw from further rounds
   - "Float" — accept the seat but remain in consideration for a better choice in the next round
   - "Slide" — accept the seat but want to move to a different programme in the SAME institute
   - "Reject and Withdraw" — reject the allotted seat and exit the counselling process

5. SUBSEQUENT ROUNDS: If a candidate chose Float/Slide and a better seat becomes available, they get it. Otherwise, they retain their previous allotment.

6. DOCUMENT VERIFICATION: After the final round, candidates must report to their allotted institute with original documents for verification.

Failure to respond to an allotment within the deadline results in automatic cancellation of the allotted seat.
        """.strip(),
    },

    # ── FLOAT, FREEZE, SLIDE ────────────────────────────────────────────────

    {
        "id": "float_freeze_slide_001",
        "title": "Understanding Float, Freeze, and Slide Options",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["float", "freeze", "slide", "seat allotment", "options"],
        "content": """
After each round of seat allotment, candidates who receive a seat must choose one of four options:

FREEZE:
- You accept the currently allotted seat permanently.
- You will NOT participate in any further rounds of JoSAA.
- Use this when you are fully satisfied with the allotted seat.
- Your seat is locked and confirmed.

FLOAT:
- You accept the allotted seat provisionally.
- You remain in consideration for a better allotment (higher preference in your choice list) in the next round.
- If a better seat (higher up in your choice list) becomes available, you get it automatically.
- If no better seat is available, you keep your current allotment.
- Use this when you are okay with your current seat but would prefer something higher on your list.

SLIDE:
- Similar to Float, but restricted to a different PROGRAMME within the SAME institute.
- Your institute doesn't change, but you might get a better branch.
- Use this when you are happy with the institute but want a better programme there.

REJECT AND WITHDRAW:
- You completely exit the JoSAA counselling process.
- You forfeit your seat and all fees paid are generally not refunded.
- Use only if you are not interested in any JoSAA allotment.

IMPORTANT: When you Float and get upgraded to a higher preference, your old seat is RELEASED and given to someone else. You cannot go back to the old seat.

IMPORTANT: If you do NOT respond to the allotment within the deadline, your seat is AUTOMATICALLY CANCELLED.
        """.strip(),
    },

    # ── SEAT TYPES AND QUOTAS ───────────────────────────────────────────────

    {
        "id": "quotas_001",
        "title": "Quotas in JoSAA: AI, HS, OS explained",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["quota", "AI", "HS", "OS", "home state", "all india"],
        "content": """
JoSAA seat allocation involves different quotas:

ALL INDIA (AI) QUOTA:
- Open to candidates from all states.
- Available at IITs (all seats are AI quota).
- NITs and IIITs also have a portion of AI quota seats (typically 50% for non-home state candidates).

HOME STATE (HS) QUOTA:
- Only for candidates from the state where the NIT/IIIT is located.
- For example, NIT Trichy Home State seats are for candidates who are domicile of Tamil Nadu.
- Typically 50% of NIT seats fall under HS quota.
- Cutoffs for HS quota are usually more relaxed than AI quota.

OTHER STATE (OS) QUOTA:
- For candidates NOT from the state where the NIT is located.
- Equivalent to AI quota at NITs for non-domicile candidates.
- Cutoffs are generally higher (tighter) than HS quota.

SPECIAL QUOTAS:
- Goa (GO), J&K (JK), Ladakh (LA): Special state quotas for specific NITs.
- Defence (DS): For children of defence personnel.
- Kashmiri Migrants (KM): Special provision.

IITs only have AI quota — there is no home state reservation at IITs.
NITs have both HS and OS quotas. When choosing preferences, candidates must know their home state to correctly identify applicable quotas.
        """.strip(),
    },

    {
        "id": "categories_001",
        "title": "Category-wise Reservations in JoSAA",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["category", "reservation", "OBC", "SC", "ST", "EWS", "PwD", "General"],
        "content": """
JoSAA follows government reservation policy. Seats are divided as follows:

GENERAL (Open / Unreserved):
- Open to all candidates. No reservation — purely merit based.
- ~40.5% of seats.

EWS (Economically Weaker Section):
- For General category candidates with annual family income below ₹8 lakh.
- 10% reservation introduced in 2019.
- Candidates need EWS certificate from competent authority.

OBC-NCL (Other Backward Classes - Non Creamy Layer):
- 27% reservation.
- "Non Creamy Layer" means annual family income below ₹8 lakh.
- Certificate must be issued by competent authority and be recent (usually within 1 year).

SC (Scheduled Caste):
- 15% reservation.
- Valid caste certificate required.

ST (Scheduled Tribe):
- 7.5% reservation.
- Valid tribe certificate required.

PwD (Persons with Disability):
- 5% horizontal reservation within each category (General-PwD, OBC-NCL-PwD, SC-PwD, ST-PwD, EWS-PwD).
- Candidates must have 40%+ disability certified by a government medical board.

GENDER-NEUTRAL vs FEMALE-ONLY SEATS:
- Some seats are specifically reserved for female candidates (Supernumerary seats at IITs, for example).
- These are additional seats, not taken from the main pool.

Candidates can only apply under the category they are certified for. Misrepresentation leads to cancellation.
        """.strip(),
    },

    # ── DOCUMENT VERIFICATION ───────────────────────────────────────────────

    {
        "id": "documents_001",
        "title": "Documents Required for JoSAA Reporting",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["documents", "verification", "reporting", "original documents"],
        "content": """
After final seat allotment, candidates must report to their allotted institute for document verification. Missing documents can result in seat cancellation.

MANDATORY DOCUMENTS (carry originals + self-attested photocopies):

1. JoSAA allotment letter (printout from portal)
2. JEE Main / JEE Advanced admit card and scorecard
3. Class 10 marksheet and certificate (for date of birth proof)
4. Class 12 marksheet and certificate
5. Category certificate (if applicable: OBC-NCL / SC / ST / EWS)
6. PwD certificate (if applicable) — from government medical board
7. Photo ID (Aadhaar card / Passport / Voter ID)
8. Passport-size photographs (usually 6-10 copies)
9. Medical fitness certificate (some institutes require this)

FOR OBC-NCL CANDIDATES:
- Certificate must be in the central government format.
- Must mention "Non-Creamy Layer."
- Usually must be dated within the last 1 year.

FOR EWS CANDIDATES:
- EWS income certificate from tehsildar/SDM.
- Must be for the financial year relevant to the admission year.

IMPORTANT: If original documents are missing or incorrect at the time of reporting, the allotted seat will be CANCELLED and cannot be recovered.
        """.strip(),
    },

    # ── CSAB ────────────────────────────────────────────────────────────────

    {
        "id": "csab_overview_001",
        "title": "What is CSAB? How is it different from JoSAA?",
        "source": "CSAB Official Guidelines 2024",
        "tags": ["csab", "overview", "special round", "vacancy"],
        "content": """
CSAB (Central Seat Allocation Board) conducts special rounds of seat allocation AFTER JoSAA counselling is over. It fills seats that remain vacant after all JoSAA rounds.

KEY DIFFERENCES FROM JoSAA:
- CSAB happens after JoSAA ends (typically September onwards).
- Only NIT+, IIITs, and GFTIs participate — IITs do NOT participate in CSAB.
- CSAB fills leftover/vacated seats.
- Candidates who did not participate in JoSAA OR did not get any allotment in JoSAA can participate.
- Even candidates who rejected their JoSAA seat can participate in CSAB.

CSAB ROUNDS:
1. CSAB Special Round 1
2. CSAB Special Round 2
(Sometimes CSAB NEUT rounds for Northeast and UT candidates)

CSAB NEUT (North East and Union Territory):
- Special provision for candidates from Northeast states and Union Territories.
- Lower cutoffs to encourage diversity.

WHO SHOULD APPLY FOR CSAB:
- Candidates with valid JEE Main score who did not get any seat in JoSAA.
- Candidates who rejected their JoSAA allotment.
- Candidates who want to try for a different NIT/IIIT after JoSAA.

CSAB cutoffs are generally more relaxed than JoSAA final round cutoffs since it is filling leftover seats.
        """.strip(),
    },

    # ── CHOICE FILLING STRATEGY ─────────────────────────────────────────────

    {
        "id": "choice_filling_001",
        "title": "How to Fill Choices Strategically in JoSAA",
        "source": "JoSAA Counselling Tips 2024",
        "tags": ["choice filling", "strategy", "tips", "preferences"],
        "content": """
Choice filling is the most critical step in JoSAA counselling. Here's how to do it right:

1. FILL AS MANY CHOICES AS POSSIBLE:
   There is no penalty for filling more choices. Always fill 20-30+ choices to maximize your chances. Leaving fewer choices means risking no allotment.

2. ORDER MATTERS — FILL IN ORDER OF PREFERENCE:
   Put your absolute dream college+branch at the top. The system gives you the highest available preference on your list. If Choice 1 is available, you get it. If not, it tries Choice 2, and so on.

3. DON'T FILL CHOICES YOU WOULD REJECT:
   Never fill a choice you wouldn't accept. If allotted, you must freeze/float — rejecting wastes a seat and harms others.

4. RESEARCH CUTOFFS BEFORE FILLING:
   Check 3-5 years of historical closing ranks for your target choices. If your rank is safely below the closing rank (lower rank number = better), it's a safe choice. If it's borderline, add it but also add safer backups.

5. MIX REACH, MATCH, AND SAFE CHOICES:
   - Reach: Your dream choice, slightly above your rank range.
   - Match: Choices where your rank is around the historical cutoff.
   - Safe: Choices where your rank is comfortably within range.

6. CONSIDER QUOTAS CORRECTLY:
   For NITs, check if you qualify for Home State quota. Home State cutoffs are often more relaxed — this significantly changes your strategy.

7. DON'T RELY ON A SINGLE INSTITUTE:
   Many students make the mistake of only filling choices for one institute. Always have diverse choices across multiple institutes.

8. LOCK CHOICES BEFORE DEADLINE:
   Unlocked choices are NOT considered. Always lock your final choice list before the deadline.
        """.strip(),
    },

    # ── COMMON FAQS ─────────────────────────────────────────────────────────

    {
        "id": "faq_rank_predictor_001",
        "title": "FAQ: How to use JEE rank to predict college?",
        "source": "JoSAA FAQ 2024",
        "tags": ["faq", "rank", "prediction", "college"],
        "content": """
Q: How do I know which college I can get with my JEE rank?

A: Use historical closing ranks as a reference. If your rank is LOWER than (better than) the closing rank of a branch, you have a good chance of getting it.

For example: If IIT Roorkee Civil Engineering General closing rank was 8,500 last year, and your rank is 7,200, you are within range. But cutoffs vary year to year, so always check 2-3 years of data.

Rule of thumb:
- If your rank is better than the last 3 years' closing ranks → very safe choice
- If your rank is within ±15% of closing rank → borderline, add as a choice but add safer options too
- If your rank is worse than closing rank → reach choice, possible if cutoffs relax

Q: Can cutoffs go up or down year to year?

A: Yes. Cutoffs fluctuate based on:
- Total number of candidates appearing for JEE
- Difficulty level of the exam that year
- Number of seats (new institutes, new branches)
- Student preferences shifting year to year

Q: What is the difference between CRL and category rank?

A: CRL (Common Rank List) is your overall rank among all candidates. Category rank is your rank within your category (e.g., OBC-NCL rank). For reserved category seats, your category rank is used. For open/General seats, CRL is used.
        """.strip(),
    },

    {
        "id": "faq_withdrawal_001",
        "title": "FAQ: Fees, Withdrawal, and Refund Policy",
        "source": "JoSAA FAQ 2024",
        "tags": ["faq", "fees", "refund", "withdrawal"],
        "content": """
Q: What fees are paid during JoSAA?

A: Two types of fees are paid:
1. Seat Acceptance Fee: Paid online when you accept an allotment. Usually ₹35,000 for General/EWS and ₹15,000 for SC/ST/PwD.
2. Remaining tuition and hostel fees: Paid at the institute during physical reporting.

Q: Is the seat acceptance fee refundable?

A: Partial refund policy:
- If you withdraw before a certain round: partial refund (deducting processing fee, usually ₹1,000-2,000).
- If you don't report to the institute after allotment: the fee is forfeited (not refunded).
- If you upgrade in Float/Slide: old seat fee is adjusted to new allotment.

Q: Can I participate in CSAB after paying JoSAA fees?

A: If you formally withdraw from JoSAA before CSAB registration opens, you can participate in CSAB. Your JoSAA fee may be partially refunded. Check the official schedule for deadlines.

Q: What happens if I don't report on the document verification day?

A: Your seat is CANCELLED automatically. There is generally no provision to extend the reporting deadline. The seat is then offered to the next candidate in subsequent rounds or CSAB.
        """.strip(),
    },

    {
        "id": "faq_pwd_001",
        "title": "FAQ: PwD Reservation and Special Provisions",
        "source": "JoSAA FAQ 2024",
        "tags": ["faq", "PwD", "disability", "reservation"],
        "content": """
Q: What is the PwD reservation in JoSAA?

A: PwD (Persons with Disability) candidates get 5% horizontal reservation within each category. This means:
- General-PwD seats: 5% of General seats
- OBC-NCL-PwD seats: 5% of OBC-NCL seats
- SC-PwD, ST-PwD, EWS-PwD similarly.

Q: What disability qualifies for PwD?

A: Candidates must have at least 40% disability as certified by a government medical board. Disabilities covered include locomotor disability, visual impairment, hearing impairment, and others as per the Rights of Persons with Disabilities Act 2016.

Q: How is rank calculated for PwD candidates at IITs?

A: IITs use a separate CRL-PwD rank. JEE Advanced publishes a separate PwD rank list. For NITs, the JEE Main PwD rank is used.

Q: Are there any relaxations in eligibility criteria for PwD?

A: Yes. PwD candidates with benchmark disability get relaxation in the 75% Class 12 marks requirement — they only need 65%. The specific conditions are defined by each institute.
        """.strip(),
    },

    {
        "id": "faq_supernumerary_001",
        "title": "FAQ: Supernumerary Seats for Female Candidates at IITs",
        "source": "JoSAA FAQ 2024",
        "tags": ["faq", "female", "supernumerary", "gender", "IIT"],
        "content": """
Q: What are supernumerary seats for female candidates?

A: IITs have a supernumerary seat scheme to increase female enrolment. These are ADDITIONAL seats created over and above the regular intake. They do NOT reduce the number of seats available to male candidates.

Key points:
- Only female candidates are eligible.
- The seats show as "Female-only (including Supernumerary)" in JoSAA.
- Cutoffs for these seats are generally more relaxed than Gender-Neutral seats of the same programme.
- These seats have been gradually increased to achieve a target of 20% female enrolment at IITs.

Q: Can a female candidate fill both Gender-Neutral and Female-only choices?

A: Yes! Female candidates can fill both Gender-Neutral and Female-only seats as separate choices. They should order them by preference. If they get a Gender-Neutral seat high on their list, great — if not, the Female-only seat acts as a backup (often with more relaxed cutoffs).

Q: Do Female-only seats exist at NITs too?

A: NITs do not have the supernumerary scheme. However, some NIT seats reserved under female quota may appear in specific cases. Generally, the supernumerary scheme is primarily an IIT initiative.
        """.strip(),
    },

]


def get_all_documents() -> list[dict]:
    """Returns the full knowledge base."""
    return KNOWLEDGE_BASE


def get_documents_by_tag(tag: str) -> list[dict]:
    """Filter documents by tag."""
    return [doc for doc in KNOWLEDGE_BASE if tag.lower() in [t.lower() for t in doc["tags"]]]


if __name__ == "__main__":
    print(f"Total documents: {len(KNOWLEDGE_BASE)}")
    all_tags = set()
    for doc in KNOWLEDGE_BASE:
        all_tags.update(doc["tags"])
    print(f"All tags: {sorted(all_tags)}")
