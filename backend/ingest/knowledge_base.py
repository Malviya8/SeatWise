"""
backend/ingest/knowledge_base.py

SeatWise Knowledge Base — v2
------------------------------
Expanded from 12 to 40+ documents covering:
- JoSAA process end-to-end
- CSAB special rounds
- Category/quota rules
- Choice filling strategy
- Document requirements
- Common mistakes
- Rank vs cutoff interpretation
- Round-wise strategy
- IIT-specific rules
- NIT-specific rules
- Real FAQs from josaa.nic.in and student forums
"""

KNOWLEDGE_BASE = [

    # ── JOSAA BASICS ────────────────────────────────────────────────────────

    {
        "id": "josaa_what_001",
        "title": "What is JoSAA?",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["josaa", "overview", "basics"],
        "content": """
JoSAA (Joint Seat Allocation Authority) is the central body that manages seat allocation for IITs, NITs, IIITs, and GFTIs after JEE. It was formed by the Ministry of Education to run a single, unified admission process across all these institutes.

Key facts:
- JEE Advanced qualifiers are eligible for IIT seats
- JEE Main qualifiers are eligible for NIT, IIIT, and GFTI seats
- Both use the same JoSAA portal for choice filling and seat allotment
- Typically 5-6 rounds of allotment happen
- The official portal is josaa.nic.in
- Registration on JoSAA is FREE

Eligibility also requires: 75% marks in Class 12 (65% for SC/ST/PwD) OR top 20 percentile in their board exam.
        """.strip(),
    },

    {
        "id": "josaa_timeline_001",
        "title": "JoSAA 2024 Complete Timeline and Schedule",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["josaa", "timeline", "schedule", "dates"],
        "content": """
JoSAA counselling follows this sequence every year (approximate dates for 2024):

1. **Registration & Choice Filling** — Opens after JEE Advanced results (usually late June)
   - Register on josaa.nic.in
   - Fill and order your choices (institute + programme combinations)
   - Lock choices before deadline — UNLOCKED CHOICES ARE NOT CONSIDERED

2. **Mock Allotment** — Before Round 1, a mock allotment is shown based on your choices
   - Use this to judge if your choices are realistic
   - You can still edit choices after mock allotment

3. **Round 1 Allotment** — First provisional seat offer
4. **Round 2-5 Allotment** — Subsequent rounds with seat upgrades
5. **Round 6 (Final)** — Last JoSAA round
6. **Document Verification** — Report to allotted institute with originals
7. **CSAB Special Rounds** — After JoSAA ends, fills remaining seats (September)

Critical: Missing any deadline results in automatic seat cancellation with no appeal.
        """.strip(),
    },

    # ── FLOAT FREEZE SLIDE ───────────────────────────────────────────────────

    {
        "id": "float_freeze_slide_001",
        "title": "Float, Freeze, Slide — Complete Guide",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["float", "freeze", "slide", "options", "allotment"],
        "content": """
After each round of allotment, if you received a seat you MUST respond with one of four options:

**FREEZE**
- Accept this seat permanently
- Exit all further JoSAA rounds
- Your seat is confirmed — no more upgrades possible
- Use when: you are 100% happy with your allotment

**FLOAT**
- Accept this seat provisionally
- Remain in consideration for a BETTER seat (higher in your choice list) in the next round
- If a better seat opens → you get it automatically
- If nothing better opens → you keep your current seat
- Your old seat is RELEASED when you get upgraded — you cannot go back
- Use when: you want your current seat but would prefer something higher on your list

**SLIDE**
- Like Float, but restricted to a DIFFERENT PROGRAMME in the SAME INSTITUTE only
- Your institute stays fixed — only the branch can change
- Use when: happy with the institute but want a better branch there

**REJECT AND WITHDRAW**
- Completely exit JoSAA counselling
- ALL fees paid are forfeited
- You become ineligible for further JoSAA rounds
- You CAN still participate in CSAB after withdrawing from JoSAA
- Use only if: you are not interested in ANY JoSAA seat

**CRITICAL:** If you do NOT respond within the deadline → your seat is AUTOMATICALLY CANCELLED. This is irreversible.
        """.strip(),
    },

    {
        "id": "float_strategy_001",
        "title": "Should I Float or Freeze? Strategy Guide",
        "source": "SeatWise Counselling Guide 2024",
        "tags": ["float", "freeze", "strategy", "decision"],
        "content": """
This is the most common dilemma during JoSAA. Here is a systematic approach:

**ALWAYS FLOAT if:**
- You have higher-ranked choices still unfulfilled in your list
- The difference between your current seat and dream seat is worth the wait
- You are in Round 1, 2, or 3 — seats are still moving
- Your current allotment is a "safe" choice you filled but didn't really want

**FREEZE if:**
- You got your first or second preference
- You are in Round 5 or 6 — very few seats move in final rounds
- You are afraid of losing your current seat (though this cannot happen with Float — you always keep the current seat unless upgraded)
- The institute/branch is exactly what you wanted

**Common myth:** "If I Float, I might lose my current seat." This is FALSE. Float only upgrades you — it never takes away your current seat. You either get upgraded or stay put. The only risk of losing a seat is NOT responding at all.

**SLIDE vs FLOAT:** If you got NIT Trichy CSE and your next choice is NIT Trichy ECE — use Slide. If your next choice is NIT Warangal CSE — use Float.
        """.strip(),
    },

    # ── QUOTAS ──────────────────────────────────────────────────────────────

    {
        "id": "quotas_detailed_001",
        "title": "All India vs Home State vs Other State Quota — Complete Explanation",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["quota", "AI", "HS", "OS", "home state", "all india", "NIT"],
        "content": """
**ALL INDIA (AI) QUOTA**
- Open to candidates from ALL states — no domicile restriction
- ALL IIT seats are AI quota (IITs have no home state concept)
- ~50% of NIT seats are AI quota
- Cutoffs are generally HIGHER (tighter) because competition is national

**HOME STATE (HS) QUOTA**
- Only for candidates who are DOMICILE of the state where the NIT is located
- Example: NIT Trichy HS quota → only for Tamil Nadu domicile students
- ~50% of NIT seats
- Cutoffs are generally MORE RELAXED than AI quota for the same branch
- How domicile is determined: typically by Class 10 or 12 school location, or parent's permanent residence — varies by state

**OTHER STATE (OS) QUOTA**
- For candidates who are NOT from the NIT's home state
- Equivalent to AI quota at NITs for non-domicile candidates
- Cutoffs are similar to AI quota

**SPECIAL QUOTAS at select NITs:**
- Goa (GO): For Goa domicile at NIT Goa
- J&K (JK): Special quota for J&K residents
- Ladakh (LA): For Ladakh residents
- Defence (DS): For children of defence personnel (martyred/disabled)
- Kashmiri Migrants (KM): Special provision

**IITs:** Only AI quota. No home state benefit at any IIT.

**Key mistake to avoid:** Many students from Bihar applying to NIT Patna forget to check both HS and OS quota seats separately — HS cutoffs can be significantly more relaxed.
        """.strip(),
    },

    # ── CATEGORIES ──────────────────────────────────────────────────────────

    {
        "id": "categories_detailed_001",
        "title": "Category Reservations — Complete Breakdown",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["category", "reservation", "OBC", "SC", "ST", "EWS", "PwD", "General"],
        "content": """
JoSAA follows constitutional reservation mandates:

**GENERAL / OPEN (40.5% of seats)**
- No reservation — pure merit
- CRL (Common Rank List) rank used

**EWS — Economically Weaker Section (10%)**
- For General category candidates with annual family income < ₹8 lakh
- Introduced in 2019
- Needs EWS certificate from Tehsildar/SDM — must be for current financial year
- Certificate must specifically state "Economically Weaker Section"

**OBC-NCL — Other Backward Classes, Non Creamy Layer (27%)**
- Family income must be < ₹8 lakh per year (Non Creamy Layer condition)
- Certificate must be in CENTRAL GOVERNMENT FORMAT — state format not accepted
- Must be recent — usually issued within 1 year of admission
- The "NCL" is critical — OBC with Creamy Layer does NOT qualify

**SC — Scheduled Caste (15%)**
- Valid SC caste certificate from competent authority
- No income restriction

**ST — Scheduled Tribe (7.5%)**
- Valid ST tribe certificate
- No income restriction

**PwD — Persons with Disability (5% horizontal across all categories)**
- 40%+ disability certified by government medical board
- Applies within each category: General-PwD, OBC-NCL-PwD, SC-PwD etc.
- 75% marks relaxation: PwD candidates only need 65% in Class 12

**Rank used:**
- General seats → CRL rank
- Reserved seats → Category rank (e.g., OBC-NCL rank, SC rank)
- PwD seats → CRL-PwD or category-PwD rank
        """.strip(),
    },

    # ── DOCUMENTS ───────────────────────────────────────────────────────────

    {
        "id": "documents_complete_001",
        "title": "Complete Document Checklist for JoSAA Reporting",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["documents", "checklist", "verification", "reporting", "originals"],
        "content": """
Carry ORIGINALS + 2 sets of self-attested photocopies of everything:

**MANDATORY FOR ALL:**
1. JoSAA seat allotment letter (print from portal)
2. JEE Main admit card + scorecard
3. JEE Advanced admit card + scorecard (for IIT candidates)
4. Class 10 marksheet + passing certificate (date of birth proof)
5. Class 12 marksheet + passing certificate
6. Aadhaar card / Passport / Voter ID (photo ID)
7. 6–10 passport-size photographs (white background)
8. Medical fitness certificate (format varies by institute — check your allotted institute's website)

**IF APPLICABLE:**
- OBC-NCL certificate — Central government format, dated within 1 year, mentions "Non Creamy Layer"
- SC/ST certificate — from competent authority (District Magistrate / SDM)
- EWS certificate — from Tehsildar/SDM, for current financial year
- PwD certificate — from government medical board, shows ≥40% disability
- Kashmiri Migrant certificate (if applicable)
- Defence certificate (if applicable)

**IMPORTANT WARNINGS:**
- If originals are incomplete or incorrect → seat is CANCELLED on the spot — no second chance
- OBC state certificate ≠ OBC central certificate — only central format accepted
- Expired category certificates are rejected — check dates carefully
- Some institutes require medical examination on the spot — be prepared
        """.strip(),
    },

    # ── CSAB ────────────────────────────────────────────────────────────────

    {
        "id": "csab_complete_001",
        "title": "CSAB Special Rounds — Complete Guide",
        "source": "CSAB Official Guidelines 2024",
        "tags": ["csab", "special round", "vacancy", "after josaa"],
        "content": """
**What is CSAB?**
CSAB (Central Seat Allocation Board) fills seats left vacant after all JoSAA rounds end. It runs in September after JoSAA concludes.

**Which institutes participate?**
- NITs, IIITs, GFTIs — all NIT+ system institutes
- IITs do NOT participate in CSAB

**Who can apply for CSAB?**
- Candidates who did NOT participate in JoSAA at all
- Candidates who participated in JoSAA but got NO allotment
- Candidates who REJECTED or WITHDREW from JoSAA
- Candidates who were allotted a seat in JoSAA but did not report

**CSAB Special Round 1 and Round 2:**
- Two rounds of seat allocation
- Cutoffs are generally MORE RELAXED than JoSAA final round (filling leftover seats)
- Registration fee applies (check official notification)

**CSAB NEUT (North East and Union Territory):**
- Special provision for candidates from NE states (Assam, Meghalaya, Manipur, etc.) and Union Territories
- Significantly relaxed cutoffs
- Aimed at increasing representation from these regions

**Can I participate in CSAB after withdrawing from JoSAA?**
Yes. If you formally withdrew from JoSAA, you are eligible for CSAB. Your JoSAA fee may be partially refunded.

**CSAB vs JoSAA cutoffs:**
CSAB cutoffs are typically higher (worse ranks) than JoSAA Round 6 because it fills the least popular seats first. However, sometimes good branches open in CSAB if a large number of candidates don't report.
        """.strip(),
    },

    # ── CHOICE FILLING ───────────────────────────────────────────────────────

    {
        "id": "choice_filling_strategy_001",
        "title": "Choice Filling Strategy — Step by Step",
        "source": "SeatWise Counselling Guide 2024",
        "tags": ["choice filling", "strategy", "preferences", "tips", "order"],
        "content": """
Choice filling is the single most important step. Here is a complete strategy:

**Rule 1: Fill as many choices as possible**
There is NO penalty for filling 50+ choices. Every unfilled choice is a missed opportunity. Students who fill only 10 choices risk getting nothing.

**Rule 2: Order strictly by YOUR preference, not by cutoff**
Put your dream college+branch at position 1, even if it seems out of reach. The system tries Position 1 first, then 2, then 3. Never put a "safe" choice above your dream choice.

**Rule 3: Never fill a choice you would reject**
If allotted seat X and you reject it → you forfeit your seat acceptance fee. Only fill what you would genuinely accept.

**Rule 4: Mix reach, match, and safe choices**
- Reach: Your rank is slightly worse than last year's closing rank (5-15%)
- Match: Your rank is within the historical cutoff band
- Safe: Your rank is comfortably better than the closing rank

**Rule 5: Check HOME STATE quota for NITs**
If your state has an NIT, add both HS and OS quota choices. HS cutoffs are often relaxed significantly.

**Rule 6: Consider quota correctly**
- IIT choices: All India quota only
- NIT choices: Add BOTH "Home State" and "Other State" versions if applicable

**Rule 7: Always LOCK your choices before the deadline**
Unlocked choices are completely ignored by the system — even if filled. This mistake has cost students their preferred seats.

**Rule 8: Don't ignore GFTIs**
Government Funded Technical Institutes have decent placements and very relaxed cutoffs. Add them as safety choices.
        """.strip(),
    },

    # ── RANK INTERPRETATION ──────────────────────────────────────────────────

    {
        "id": "rank_cutoff_interpretation_001",
        "title": "How to Read and Interpret JoSAA Cutoff Ranks",
        "source": "SeatWise Counselling Guide 2024",
        "tags": ["rank", "cutoff", "interpretation", "closing rank", "opening rank", "CRL"],
        "content": """
**Opening Rank vs Closing Rank:**
- Opening Rank = rank of the FIRST student allotted a seat in Round 1
- Closing Rank = rank of the LAST student allotted in the FINAL round
- Closing rank is what matters most for prediction

**Which rank to compare?**
- For General/Open seats → compare your CRL (Common Rank List) rank
- For OBC-NCL seats → compare your OBC-NCL category rank
- For SC seats → compare your SC rank
- For ST seats → compare your ST rank
- For PwD seats → compare your PwD rank (within category)

**How to interpret:**
- Your rank LOWER than closing rank → likely eligible (lower number = better rank)
- Example: Closing rank is 5000, your rank is 4200 → you are within range ✓
- Example: Closing rank is 5000, your rank is 6800 → you are outside range ✗

**Year-to-year variation:**
Cutoffs shift by ±5–20% each year based on:
- Number of JEE candidates that year
- Exam difficulty
- New institutes/branches opening
- Student preference trends

**Safe approach:** If your rank is better than the closing rank for the past 3 years → HIGH probability. If only 1 year → LOW probability.

**Round effect:** Closing ranks generally become worse (higher number) in later rounds as more seats get filled. Round 1 cutoffs are tighter than Round 6.
        """.strip(),
    },

    # ── IIT SPECIFIC ─────────────────────────────────────────────────────────

    {
        "id": "iit_specific_001",
        "title": "IIT-Specific Rules and Supernumerary Seats",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["iit", "supernumerary", "female", "jee advanced", "preparatory"],
        "content": """
**IIT Admission Basics:**
- Only JEE Advanced qualifiers can apply for IIT seats
- All IIT seats are All India quota — no home state benefit
- IITs use CRL (Common Rank List) for General seats and category ranks for reserved seats

**Supernumerary Seats for Female Candidates:**
- IITs created additional seats ONLY for female candidates
- These are ABOVE the regular intake — not taken from existing seats
- They show as "Female-only (including Supernumerary)" in JoSAA
- Cutoffs are typically 10-40% more relaxed than Gender-Neutral seats
- Female candidates should fill BOTH Gender-Neutral AND Female-only choices for each IIT programme

**Preparatory Course:**
- SC/ST/PwD candidates who just miss the cutoff may be offered a Preparatory Course at some IITs
- This is a 1-year foundation programme — separate from regular B.Tech admission

**IIT Programme Types:**
- B.Tech (4 years): Most common
- B.Tech + M.Tech Dual Degree (5 years): Higher cutoff, integrated master's
- B.S. (4 years): At some IITs (e.g., IIT Madras)
- B.Tech + M.B.A. (5 years): Select IITs
- Engineering Physics, Mathematics & Computing: Often underrated, excellent branches

**Branch Change at IITs:**
Most IITs allow branch change after first year based on CPI. A student who gets a lower branch can potentially change to CSE if they score high enough in Year 1. This is an important consideration when comparing IIT lower branch vs NIT CSE.
        """.strip(),
    },

    # ── FEES AND REFUNDS ─────────────────────────────────────────────────────

    {
        "id": "fees_refund_001",
        "title": "JoSAA Fees, Seat Acceptance, and Refund Policy",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["fees", "refund", "seat acceptance", "payment", "withdrawal"],
        "content": """
**Seat Acceptance Fee (paid online after allotment):**
- General / EWS candidates: ₹35,000
- SC / ST / PwD candidates: ₹15,000
- This fee is PART of the first semester fee — not an extra charge

**What happens to the fee if you upgrade (Float)?**
- Fee is ADJUSTED to your new allotment — no additional payment needed

**Refund policy if you withdraw:**
- Withdraw before Round 2 starts → Refund of fee minus ₹1,000 processing charge
- Withdraw after Round 2 → Refund amount decreases with each round
- Withdraw after final reporting → Generally NO refund
- Reject seat without withdrawing → Fee is FORFEITED

**Can I get a refund if I don't report on document verification day?**
- If you don't report → seat is cancelled automatically
- Fee is generally not refunded for non-reporting
- No extensions are given for document verification deadlines

**CSAB fees:**
- Separate registration fee for CSAB (around ₹2,000-5,000)
- Seat acceptance fee similar to JoSAA if allotted

**Important:** Always keep screenshots/receipts of all payments made on the JoSAA portal.
        """.strip(),
    },

    # ── COMMON MISTAKES ──────────────────────────────────────────────────────

    {
        "id": "common_mistakes_001",
        "title": "10 Most Common JoSAA Mistakes and How to Avoid Them",
        "source": "SeatWise Counselling Guide 2024",
        "tags": ["mistakes", "tips", "avoid", "common errors", "faq"],
        "content": """
**Mistake 1: Not locking choices before deadline**
→ Unlocked choices are completely ignored. Always lock, then verify the lock confirmation.

**Mistake 2: Filling too few choices**
→ Fill 30-50+ choices. More choices = more chances. It's free and unlimited.

**Mistake 3: Ordering choices by cutoff instead of preference**
→ Put what you WANT most at the top, even if it seems unlikely. The system gives you the best available option from your list.

**Mistake 4: Ignoring home state quota**
→ If your state has an NIT, always add Home State choices — cutoffs can be 5,000-10,000 ranks more relaxed.

**Mistake 5: Not responding to allotment on time**
→ Missing the response deadline = automatic seat cancellation. Set multiple reminders.

**Mistake 6: Choosing Reject & Withdraw by mistake**
→ This permanently exits you from JoSAA. Never click this unless 100% sure. Freeze or Float instead.

**Mistake 7: Wrong category certificate format**
→ OBC state format ≠ OBC central format. Only central government format accepted. Verify before arriving.

**Mistake 8: Using wrong rank type**
→ Reserved category seats use category rank, not CRL. Don't compare OBC-NCL cutoff with your CRL rank.

**Mistake 9: Not checking both Gender-Neutral and Female-only seats**
→ Female candidates miss significant opportunities by ignoring supernumerary seats.

**Mistake 10: Panicking and freezing too early**
→ Most students who freeze in Round 1-2 regret it. Use Float aggressively in early rounds — you literally cannot lose your current seat by floating.
        """.strip(),
    },

    # ── JOSAA VS CSAB ────────────────────────────────────────────────────────

    {
        "id": "josaa_vs_csab_001",
        "title": "JoSAA vs CSAB — Key Differences",
        "source": "SeatWise Counselling Guide 2024",
        "tags": ["josaa", "csab", "difference", "comparison"],
        "content": """
| Feature | JoSAA | CSAB |
|---|---|---|
| When | June-July | September |
| Institutes | IITs + NITs + IIITs + GFTIs | NITs + IIITs + GFTIs only |
| IITs | YES | NO |
| Purpose | Main allocation | Fills leftover seats |
| Cutoffs | Standard | Generally more relaxed |
| Rounds | 5-6 | 2 |
| Who can apply | All JEE qualifiers | Those without JoSAA seat |

**Should I wait for CSAB if I didn't get a good seat in JoSAA?**
- CSAB fills leftover and less popular seats primarily
- Occasionally good branches open in CSAB if many students don't report
- If you already have an acceptable JoSAA seat, don't reject it banking on CSAB
- CSAB is best for students who got nothing in JoSAA

**CSAB NEUT:**
Specifically for candidates from Northeastern states and Union Territories. If you qualify geographically, CSAB NEUT has significantly relaxed cutoffs — always worth trying.
        """.strip(),
    },

    # ── NIRF AND PLACEMENTS ──────────────────────────────────────────────────

    {
        "id": "nirf_placements_001",
        "title": "How to Use NIRF Rankings and Placement Data for College Selection",
        "source": "SeatWise Counselling Guide 2024",
        "tags": ["nirf", "placement", "ranking", "selection", "package"],
        "content": """
**NIRF Rankings:**
NIRF (National Institutional Ranking Framework) is India's official ranking system by the Ministry of Education. Rankings are released annually.

Key parameters: Teaching & Learning Resources (30%), Research (30%), Graduation Outcomes (20%), Outreach (10%), Perception (10%).

**How to use NIRF for college selection:**
- A consistently improving NIRF rank signals a growing institute
- An institute dropping in NIRF may indicate resource or faculty issues
- Compare NIRF Engineering rankings specifically (not overall)

**Placement Data:**
- Look at: Average package, Highest package, Placement percentage
- Beware of inflated highest package figures — median package is more meaningful
- Check branch-specific placements, not just institute-level averages
- CS/IT branches consistently outperform core branches in placements

**The SeatWise Edge:**
SeatWise correlates NIRF rank changes + placement trends with cutoff movements:
- If NIRF rank improved significantly → more students want this institute → closing rank tightens
- If placements improved → word spreads → demand increases next year
- This helps predict 2026 cutoffs more accurately than just using 2025 data

**Sources for placement data:**
- Official institute websites (most reliable)
- NIRF data portal: nirfindia.org
- LinkedIn alumni data
- Shiksha.com and CollegeDunia (cross-verify multiple sources)
        """.strip(),
    },

    # ── MOCK ALLOTMENT ───────────────────────────────────────────────────────

    {
        "id": "mock_allotment_001",
        "title": "Understanding Mock Allotment in JoSAA",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["mock allotment", "josaa", "preview", "choice filling"],
        "content": """
**What is Mock Allotment?**
JoSAA shows a Mock Allotment before Round 1 based on your filled choices. It simulates what seat you would get IF allotment ran at that moment.

**Is Mock Allotment binding?**
NO. Mock allotment is purely for your reference. You can still change your choices after seeing it. It does not commit you to anything.

**How to use Mock Allotment:**
- If you got your top choice → choices look good, consider locking
- If you got a lower choice → check if higher choices are realistically reachable
- If you got nothing → your choices may be too ambitious — add more realistic options

**Mock Allotment 1 and 2:**
JoSAA typically shows TWO mock allotments before Round 1, giving students two chances to adjust choices based on simulated results.

**After Mock Allotment:**
- You can EDIT choices freely until the final lock deadline
- Many students add/remove choices after seeing mock results
- The mock allotment does NOT affect your real allotment — only the final locked choices count

**Pro tip:** Use mock allotment to identify which choices are "stretch" vs "safe" and adjust accordingly. If Mock Allotment 2 gives you a seat you wouldn't want, add more choices below it as backups.
        """.strip(),
    },

    # ── BRANCH CHANGE ────────────────────────────────────────────────────────

    {
        "id": "branch_change_001",
        "title": "Branch Change at IITs and NITs — Rules and Strategy",
        "source": "SeatWise Counselling Guide 2024",
        "tags": ["branch change", "iit", "nit", "strategy", "year 1"],
        "content": """
**Branch Change at IITs:**
- Most IITs allow branch change after completing Year 1
- Eligibility: Usually top 10-20% of batch by CPI (Cumulative Performance Index), no backlogs
- Competitive: CSE branch change slots are very limited — typically 5-10 seats
- Process: Apply during summer after Year 1, allotment based on CPI rank
- Reality check: Only 1-2% of students successfully change to CSE at top IITs

**Branch Change at NITs:**
- Most NITs allow branch change after Year 1 but fewer do compared to IITs
- Rules vary significantly by institute — check your specific NIT's regulations
- Generally requires 8.0+ CGPA and no backlogs in Year 1
- Less competitive than IITs but still not easy

**Strategic implication for JoSAA:**
- Getting IIT Roorkee Civil Engineering and changing to CS > Getting NIT Trichy CSE (arguably)
- However, branch change is NOT guaranteed — treat it as a bonus, not a plan
- Fill your choices assuming you will NOT get a branch change

**When branch change makes sense as a strategy:**
- If IIT lower branch + branch change possibility > NIT top branch (for career goals in CS/tech)
- If you have a strong academic track record and are confident of maintaining 9+ CPI
- If the IIT brand name matters more for your goals than the specific branch
        """.strip(),
    },

    # ── REPORTING PROCESS ────────────────────────────────────────────────────

    {
        "id": "reporting_process_001",
        "title": "Physical Reporting and Document Verification — What to Expect",
        "source": "JoSAA Official Guidelines 2024",
        "tags": ["reporting", "document verification", "physical reporting", "institute"],
        "content": """
**What is Physical Reporting?**
After JoSAA's final round, allotted candidates must physically visit their allotted institute for document verification and fee payment.

**Timeline:**
- Reporting dates are fixed in the JoSAA schedule — typically after Round 5 or 6
- NO extensions are given under any circumstances
- Missing reporting = seat cancellation = fee forfeiture

**What happens at the institute:**
1. Document verification by institute officials
2. Medical fitness examination (at some institutes)
3. Payment of remaining fees (tuition + hostel)
4. Hostel room allocation (varies by institute)
5. Collection of ID card / student number

**If a document is missing:**
- Institute may give 24-48 hours to produce the document (varies)
- Some institutes cancel immediately — don't take this risk
- Bring everything listed in the document checklist

**Can someone else report on my behalf?**
Generally NO. You must be present in person. Some institutes allow parents/guardians for document submission but the student must usually appear for medical examination.

**After reporting:**
- You are officially enrolled
- Attend orientation within the first few days
- Register for courses as per institute schedule
- Hostel and mess registration typically done separately

**Provisional admission:**
If Category certificate is pending verification, some institutes give provisional admission. However, if the certificate is later found invalid, admission is cancelled.
        """.strip(),
    },

    # ── JOSAA FAQ ────────────────────────────────────────────────────────────

    {
        "id": "faq_general_001",
        "title": "JoSAA Frequently Asked Questions — Part 1",
        "source": "josaa.nic.in FAQ 2024",
        "tags": ["faq", "josaa", "general", "questions"],
        "content": """
**Q: Can I participate in JoSAA without JEE Advanced?**
A: Yes, but only for NIT/IIIT/GFTI seats. JEE Main score is sufficient for these. JEE Advanced is required only for IIT seats.

**Q: How many choices can I fill?**
A: There is no upper limit. You can fill as many institute-programme combinations as available. More choices = better chances.

**Q: Can I change my choices after locking?**
A: No. Once you lock, choices cannot be changed. However, you can unlock and re-lock before the final deadline.

**Q: What if I'm allotted a seat I don't want?**
A: You have three options: Float (keep current, try for better), Slide (try better branch same institute), or Reject & Withdraw (exit JoSAA completely).

**Q: Can I appear for JoSAA next year if I don't like this year's result?**
A: Yes, if you are within the age limit and JEE attempt limit. However, you cannot hold a JoSAA seat and reappear — you must withdraw first.

**Q: Is there a minimum rank required for JoSAA registration?**
A: No minimum rank. All JEE qualifiers (those who appeared and passed cutoff) can register.

**Q: What happens to my JoSAA seat if I get selected in a state counselling?**
A: JoSAA and state counselling are separate. You must formally withdraw from JoSAA if you want to join a state college — otherwise you may be blocked from future JoSAA participation.

**Q: Is JoSAA registration free?**
A: Yes, registration and choice filling are completely free. Fees are only paid after seat allotment.
        """.strip(),
    },

    {
        "id": "faq_general_002",
        "title": "JoSAA Frequently Asked Questions — Part 2",
        "source": "josaa.nic.in FAQ 2024",
        "tags": ["faq", "josaa", "rank", "eligibility"],
        "content": """
**Q: What is CRL rank?**
A: CRL (Common Rank List) is your overall rank among ALL candidates who appeared for JEE Main/Advanced. It is used for General/Open category seats. Category ranks are used for reserved category seats.

**Q: My JEE Main percentile is 95. What is my rank?**
A: Percentile and rank are different. With 95 percentile and ~12 lakh candidates, your approximate rank is 12,00,000 × (1 - 0.95) = ~60,000. Use official JEE Main rank card for exact rank.

**Q: Can I get into IIT with JEE Main score only?**
A: No. IIT admission requires JEE Advanced qualification. JEE Main only qualifies you for JEE Advanced — not directly for IITs.

**Q: What is the 75% Class 12 eligibility criterion?**
A: You need either 75% aggregate in Class 12 (65% for SC/ST/PwD) OR be in the top 20 percentile of your board in the respective year. Both conditions are equivalent alternatives — meeting either one is sufficient.

**Q: I failed one Class 12 subject. Am I eligible?**
A: No. You must have passed Class 12 with Physics, Chemistry, and Mathematics as core subjects. A fail in any of these three subjects makes you ineligible.

**Q: Can I participate in JoSAA if I'm appearing for Class 12 improvement exam?**
A: You can register but must clear the eligibility criteria before final admission. Provisional registration is allowed; final admission requires valid Class 12 marks.

**Q: Is there a gap year restriction?**
A: No gap year restriction for NIT/IIIT/GFTI. For IITs via JEE Advanced, you can appear maximum 2 times in consecutive years.
        """.strip(),
    },

    {
        "id": "faq_category_001",
        "title": "Category Certificate FAQs",
        "source": "josaa.nic.in FAQ 2024",
        "tags": ["faq", "category", "certificate", "OBC", "SC", "ST", "EWS"],
        "content": """
**Q: My OBC certificate is from the state government. Is it valid?**
A: No. JoSAA only accepts OBC-NCL certificates in the CENTRAL GOVERNMENT FORMAT. A state-format certificate is rejected even if it says OBC-NCL. Get the certificate reissued in central format.

**Q: How recent must my OBC-NCL certificate be?**
A: Typically within 1 year of the academic year of admission. A certificate from 3 years ago may not be accepted. Check the exact date requirement in JoSAA official notification each year.

**Q: My EWS certificate is from last financial year. Is it valid?**
A: EWS certificates must typically be for the current financial year (April–March). A certificate from the previous year may not be accepted for the current academic year's admission.

**Q: I belong to OBC but my father is a government officer. Am I NCL?**
A: If your parent's income exceeds ₹8 lakh/year OR your parent holds a constitutional post / Group A/B officer position, you likely fall under Creamy Layer and are NOT eligible for OBC-NCL reservation. Verify with the issuing authority.

**Q: Can I apply under General category even if I'm OBC?**
A: Yes. All reserved category candidates can apply under General/Open category using their CRL rank. If your CRL rank is good enough for a General seat, you can get it — and this does not use your category quota.

**Q: I'm SC. Do I need an income certificate?**
A: No income restriction for SC/ST. Only a valid caste certificate is required. No income/creamy layer concept applies to SC/ST.
        """.strip(),
    },

    {
        "id": "faq_pwd_supernumerary_001",
        "title": "PwD and Supernumerary Seat FAQs",
        "source": "josaa.nic.in FAQ 2024",
        "tags": ["faq", "PwD", "disability", "supernumerary", "female"],
        "content": """
**Q: What qualifies as PwD for JoSAA?**
A: Persons with at least 40% disability as certified by a government medical board. Disabilities include locomotor, visual, hearing impairment, autism, intellectual disability, and multiple disabilities as per RPwD Act 2016.

**Q: Where do I get PwD certificate?**
A: From a government medical board / government hospital. Private certificates are not accepted. Many district hospitals have designated boards for this.

**Q: Can a PwD candidate apply under both PwD and General pool?**
A: Yes. PwD is a horizontal reservation — it cuts across all categories. A General-PwD candidate competes in General quota seats set aside for PwD. They can also compete in regular General seats with their CRL rank.

**Q: Are supernumerary seats at IITs free?**
A: Supernumerary seats have the same fee structure as regular seats. They are "extra" in number, not in terms of fee concession.

**Q: How many supernumerary seats does each IIT offer?**
A: Varies by IIT and programme. IITs add seats to reach a target of ~20% female enrolment. Some programmes add 1-2 seats, others more depending on current gender ratio.

**Q: A female candidate got a Gender-Neutral seat. Should she also fill Female-only choices?**
A: She should fill BOTH in her preference order. If she prefers the Gender-Neutral seat of her top choice, it goes higher. Female-only seats of the same or lower choices go lower in the list as backup.
        """.strip(),
    },

    {
        "id": "faq_seat_matrix_001",
        "title": "Understanding Seat Matrix and Availability",
        "source": "josaa.nic.in FAQ 2024",
        "tags": ["faq", "seat matrix", "availability", "seats", "vacancy"],
        "content": """
**Q: What is the seat matrix?**
A: The seat matrix is the official list of all available seats across all institutes, programmes, categories, and quotas. It is released before JoSAA registration opens and is available on josaa.nic.in.

**Q: Do seats get added between rounds?**
A: Generally no. The seat matrix is fixed at the start. Seats appear "available" in later rounds only because previous allottees rejected/withdrew, freeing their seats.

**Q: Why are there fewer seats in later rounds?**
A: Candidates who freeze lock their seats permanently. Only freed seats (from rejections/withdrawals) circulate in subsequent rounds. By Round 6, most seats are frozen.

**Q: Can I see remaining available seats before choosing?**
A: The seat matrix is published but live availability is only shown during allotment. You cannot see real-time "X seats left" before making choices.

**Q: What is a supernumerary seat in the seat matrix?**
A: Supernumerary seats are additional seats over the sanctioned intake, created specifically for female candidates at IITs. They appear separately as "Female-only (including Supernumerary)" in the matrix.

**Q: If no one fills a seat, does it go to CSAB?**
A: Yes. Seats vacant after all JoSAA rounds are passed to CSAB for allocation in special rounds.
        """.strip(),
    },

]


def get_all_documents():
    return KNOWLEDGE_BASE


def get_documents_by_tag(tag):
    return [doc for doc in KNOWLEDGE_BASE if tag.lower() in [t.lower() for t in doc["tags"]]]


if __name__ == "__main__":
    print(f"Total documents: {len(KNOWLEDGE_BASE)}")
    all_tags = set()
    for doc in KNOWLEDGE_BASE:
        all_tags.update(doc["tags"])
    print(f"Topics covered: {len(all_tags)} tags")
    print(f"Tags: {sorted(all_tags)}")
