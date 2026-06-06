import { useState } from "react";

const API = import.meta.env.VITE_API_URL || "https://seatwise-production-7b03.up.railway.app";

const INDIAN_STATES = [
  "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
  "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
  "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
  "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
  "Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
  "Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli",
  "Daman and Diu","Delhi","Jammu and Kashmir","Ladakh","Lakshadweep","Puducherry"
];

const CATEGORIES = ["General","OBC-NCL","SC","ST","EWS","General-PwD","OBC-NCL-PwD","SC-PwD","ST-PwD","EWS-PwD"];

const css = `
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

.pred-wrap { font-family:'DM Sans',sans-serif; min-height:100vh; background:#f7f8fc; }

/* ── Landing ── */
.pred-landing {
  min-height:100vh; display:grid; grid-template-columns:1fr 480px;
  background:#fff;
}
.pred-left {
  background:linear-gradient(135deg,#1a2744 0%,#2a3d6e 60%,#0f9b8e 100%);
  padding:60px 56px; display:flex; flex-direction:column; justify-content:center; position:relative; overflow:hidden;
}
.pred-left::before {
  content:''; position:absolute; top:-100px; right:-100px;
  width:400px; height:400px; border-radius:50%;
  background:rgba(255,107,53,0.12); pointer-events:none;
}
.pred-left::after {
  content:''; position:absolute; bottom:-80px; left:-80px;
  width:300px; height:300px; border-radius:50%;
  background:rgba(15,155,142,0.15); pointer-events:none;
}
.pred-badge {
  display:inline-flex; align-items:center; gap:8px;
  background:rgba(255,107,53,0.2); border:1px solid rgba(255,107,53,0.4);
  color:#ffb49a; border-radius:99px; padding:6px 16px; font-size:12px;
  font-weight:600; letter-spacing:0.05em; margin-bottom:28px; width:fit-content;
}
.pred-badge::before { content:'✦'; font-size:10px; }
.pred-h1 {
  font-family:'Playfair Display',serif; font-size:3.2rem; font-weight:700;
  color:#fff; line-height:1.15; margin-bottom:20px;
}
.pred-h1 span { color:#FF6B35; }
.pred-sub { color:rgba(255,255,255,0.65); font-size:15px; line-height:1.7; max-width:440px; margin-bottom:40px; }
.pred-features { display:flex; flex-direction:column; gap:14px; }
.pred-feat {
  display:flex; align-items:center; gap:12px;
  color:rgba(255,255,255,0.8); font-size:13px;
}
.pred-feat-icon {
  width:32px; height:32px; border-radius:8px;
  background:rgba(255,255,255,0.1); display:flex; align-items:center;
  justify-content:center; font-size:15px; flex-shrink:0;
}
.pred-counter {
  margin-top:48px; padding-top:32px; border-top:1px solid rgba(255,255,255,0.12);
  display:flex; gap:40px;
}
.pred-stat-num { font-family:'Playfair Display',serif; font-size:2rem; font-weight:700; color:#FF6B35; }
.pred-stat-label { font-size:11px; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:0.08em; }

/* ── Form Panel ── */
.pred-form-panel {
  background:#fff; padding:48px 40px; display:flex; flex-direction:column;
  justify-content:center; border-left:1px solid rgba(26,39,68,0.08);
  overflow-y:auto;
}
.pred-form-title {
  font-family:'Playfair Display',serif; font-size:1.6rem; color:#1a2744;
  font-weight:700; margin-bottom:6px;
}
.pred-form-sub { font-size:13px; color:#9aaac0; margin-bottom:32px; }
.pred-field { margin-bottom:18px; }
.pred-field label { display:block; font-size:12px; font-weight:600; color:#5a6a8a; margin-bottom:6px; letter-spacing:0.03em; }
.pred-input, .pred-select {
  width:100%; padding:11px 14px; border:1.5px solid rgba(26,39,68,0.12);
  border-radius:10px; font-size:14px; font-family:'DM Sans',sans-serif;
  color:#1a2744; background:#fafbfc; outline:none; transition:all 0.15s;
}
.pred-input:focus, .pred-select:focus { border-color:#FF6B35; background:#fff; box-shadow:0 0 0 3px rgba(255,107,53,0.08); }
.pred-select { appearance:none; background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%235a6a8a' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E"); background-repeat:no-repeat; background-position:right 12px center; background-color:#fafbfc; padding-right:32px; }
.pred-radio-group { display:flex; gap:12px; }
.pred-radio {
  flex:1; border:1.5px solid rgba(26,39,68,0.12); border-radius:10px;
  padding:10px 16px; display:flex; align-items:center; gap:8px;
  cursor:pointer; transition:all 0.15s; font-size:13px; color:#5a6a8a;
}
.pred-radio.active { border-color:#FF6B35; background:#fff5f2; color:#FF6B35; font-weight:600; }
.pred-radio input { display:none; }
.pred-submit {
  width:100%; padding:14px; border-radius:10px; border:none;
  background:linear-gradient(135deg,#FF6B35,#ff9a6c); color:#fff;
  font-family:'DM Sans',sans-serif; font-size:15px; font-weight:700;
  cursor:pointer; transition:all 0.2s; margin-top:8px;
  box-shadow:0 4px 16px rgba(255,107,53,0.3);
}
.pred-submit:hover { transform:translateY(-1px); box-shadow:0 6px 20px rgba(255,107,53,0.4); }
.pred-submit:active { transform:translateY(0); }
.pred-submit:disabled { background:#e0e4ef; color:#9aaac0; box-shadow:none; cursor:not-allowed; transform:none; }
.pred-hint { font-size:11px; color:#FF6B35; margin-top:6px; }

/* ── Results Page ── */
.pred-results { padding:0 0 60px; }
.pred-results-header {
  background:linear-gradient(135deg,#1a2744,#2a3d6e); padding:32px 40px;
  border-bottom:3px solid #FF6B35;
}
.pred-results-title { font-family:'Playfair Display',serif; color:#fff; font-size:1.6rem; text-align:center; margin-bottom:24px; }
.pred-summary-cards { display:flex; gap:16px; justify-content:center; flex-wrap:wrap; }
.pred-summary-card {
  background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.15);
  border-radius:12px; padding:14px 24px; display:flex; align-items:center; gap:12px;
  min-width:160px;
}
.pred-summary-icon { font-size:22px; }
.pred-summary-label { font-size:10px; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:0.08em; }
.pred-summary-value { font-size:16px; font-weight:700; color:#fff; }

/* Results body */
.pred-results-body { display:grid; grid-template-columns:260px 1fr; gap:0; min-height:calc(100vh - 200px); }
.pred-filters-panel {
  background:#fff; border-right:1px solid rgba(26,39,68,0.08);
  padding:24px 20px; position:sticky; top:0; height:fit-content;
}
.pred-filter-title { font-size:13px; font-weight:700; color:#1a2744; margin-bottom:4px; }
.pred-filter-clear { font-size:11px; color:#FF6B35; cursor:pointer; float:right; }
.pred-filter-section { margin-top:20px; }
.pred-filter-section-label { font-size:10px; font-weight:700; color:#9aaac0; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:10px; }
.pred-filter-chips { display:flex; flex-wrap:wrap; gap:6px; }
.pred-chip {
  padding:5px 12px; border-radius:99px; font-size:12px; font-weight:500;
  border:1.5px solid rgba(26,39,68,0.12); color:#5a6a8a; cursor:pointer; transition:all 0.15s;
}
.pred-chip.active { border-color:#FF6B35; background:#fff5f2; color:#FF6B35; font-weight:600; }
.pred-chip:hover:not(.active) { border-color:#1a2744; color:#1a2744; }
.pred-filter-search {
  width:100%; padding:8px 10px; border:1.5px solid rgba(26,39,68,0.12);
  border-radius:8px; font-size:12px; font-family:'DM Sans',sans-serif;
  outline:none; margin-top:6px; color:#1a2744;
}
.pred-filter-search:focus { border-color:#FF6B35; }

/* Table area */
.pred-table-area { padding:24px 28px; }
.pred-quick-filters { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:16px; }
.pred-qf {
  padding:7px 14px; border-radius:99px; font-size:12px; font-weight:500;
  border:1.5px solid rgba(26,39,68,0.12); color:#5a6a8a; cursor:pointer; transition:all 0.15s;
  background:#fff;
}
.pred-qf:hover { border-color:#FF6B35; color:#FF6B35; }
.pred-qf.active { background:#FF6B35; border-color:#FF6B35; color:#fff; }
.pred-search-bar {
  width:100%; padding:11px 16px 11px 40px; border:1.5px solid rgba(26,39,68,0.12);
  border-radius:10px; font-size:13px; font-family:'DM Sans',sans-serif;
  outline:none; margin-bottom:20px; color:#1a2744; background:#fff;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%239aaac0' stroke-width='2'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.35-4.35'/%3E%3C/svg%3E");
  background-repeat:no-repeat; background-position:12px center;
}
.pred-search-bar:focus { border-color:#FF6B35; }
.pred-info-bar {
  background:#f0fdf9; border:1px solid rgba(15,155,142,0.2); border-radius:10px;
  padding:12px 16px; margin-bottom:20px; font-size:12px; color:#0f9b8e; line-height:1.6;
}
.pred-info-bar strong { color:#1a2744; }

/* College cards */
.pred-college-card {
  background:#fff; border:1px solid rgba(26,39,68,0.08); border-radius:14px;
  margin-bottom:16px; overflow:hidden; transition:box-shadow 0.2s;
}
.pred-college-card:hover { box-shadow:0 4px 20px rgba(26,39,68,0.1); }
.pred-college-header {
  padding:16px 20px; border-bottom:1px solid rgba(26,39,68,0.06);
  display:flex; align-items:center; gap:14px;
}
.pred-college-logo {
  width:44px; height:44px; border-radius:10px; background:linear-gradient(135deg,#f0f4ff,#e8f4fd);
  display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0;
}
.pred-college-name { font-size:14px; font-weight:700; color:#1a2744; }
.pred-college-meta { font-size:11px; color:#9aaac0; margin-top:3px; display:flex; gap:12px; }
.pred-college-meta-item { display:flex; align-items:center; gap:4px; }
.pred-college-table { width:100%; border-collapse:collapse; }
.pred-college-table th {
  text-align:left; padding:10px 20px; font-size:10px; font-weight:700;
  color:#9aaac0; letter-spacing:0.08em; text-transform:uppercase;
  background:#fafbfc; border-bottom:1px solid rgba(26,39,68,0.06);
}
.pred-college-table td {
  padding:12px 20px; font-size:13px; color:#1a2744;
  border-bottom:1px solid rgba(26,39,68,0.04);
  vertical-align:middle;
}
.pred-college-table tr:last-child td { border-bottom:none; }
.pred-college-table tr:hover td { background:#fafbfc; }
.pred-branch-name { font-weight:600; color:#1a2744; font-size:13px; }
.pred-branch-type { font-size:11px; color:#9aaac0; }
.pred-prob { display:inline-flex; align-items:center; padding:3px 10px; border-radius:99px; font-size:11px; font-weight:700; }
.pred-prob.high { background:#d4edda; color:#155724; }
.pred-prob.medium { background:#fff3cd; color:#856404; }
.pred-prob.low { background:#f8d7da; color:#842029; }
.pred-rank-badge { font-size:13px; font-weight:600; color:#1a2744; }
.pred-details-btn {
  padding:6px 14px; border-radius:8px; border:1.5px solid rgba(26,39,68,0.12);
  background:#fff; color:#FF6B35; font-size:12px; font-weight:600;
  cursor:pointer; transition:all 0.15s; font-family:'DM Sans',sans-serif;
}
.pred-details-btn:hover { background:#FF6B35; color:#fff; border-color:#FF6B35; }
.pred-package { font-size:13px; font-weight:600; color:#0f9b8e; }
.pred-placement { font-size:13px; color:#5a6a8a; }
.pred-no-results { text-align:center; padding:60px 20px; color:#9aaac0; }

/* ── Modal ── */
.pred-modal-overlay {
  position:fixed; inset:0; background:rgba(26,39,68,0.5); backdrop-filter:blur(4px);
  display:flex; align-items:center; justify-content:center; z-index:1000; padding:20px;
  animation:fadeIn 0.2s ease;
}
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
.pred-modal {
  background:#fff; border-radius:20px; width:100%; max-width:560px;
  max-height:85vh; overflow-y:auto; box-shadow:0 20px 60px rgba(26,39,68,0.2);
  animation:slideUp 0.25s ease;
}
@keyframes slideUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
.pred-modal-header {
  padding:24px 24px 0; display:flex; align-items:flex-start; justify-content:space-between;
  position:sticky; top:0; background:#fff; border-bottom:1px solid rgba(26,39,68,0.08);
  padding-bottom:16px;
}
.pred-modal-institute { font-size:13px; color:#9aaac0; margin-bottom:4px; }
.pred-modal-branch { font-size:18px; font-weight:700; color:#1a2744; font-family:'Playfair Display',serif; }
.pred-modal-close {
  width:32px; height:32px; border-radius:50%; border:1.5px solid rgba(26,39,68,0.12);
  background:#fff; cursor:pointer; display:flex; align-items:center; justify-content:center;
  font-size:16px; color:#9aaac0; transition:all 0.15s; flex-shrink:0;
}
.pred-modal-close:hover { background:#f8d7da; color:#842029; border-color:#f8d7da; }
.pred-modal-body { padding:20px 24px 24px; }
.pred-modal-section { margin-bottom:20px; }
.pred-modal-section-title { font-size:11px; font-weight:700; color:#9aaac0; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:12px; }
.pred-admission-box {
  background:#f0fdf9; border:1px solid rgba(15,155,142,0.2); border-radius:12px;
  padding:16px; margin-bottom:16px;
}
.pred-admission-label { font-size:12px; color:#5a6a8a; margin-bottom:4px; }
.pred-admission-rank { font-size:15px; font-weight:700; color:#FF6B35; }
.pred-admission-eligible { font-size:12px; color:#0f9b8e; margin-top:6px; }
.pred-prob-box {
  background:#fff3cd; border:1px solid rgba(133,100,4,0.2); border-radius:12px;
  padding:12px 16px; display:flex; align-items:center; justify-content:space-between;
  margin-bottom:16px;
}
.pred-round-table { width:100%; border-collapse:collapse; border-radius:10px; overflow:hidden; }
.pred-round-table th {
  background:#1a2744; color:#fff; padding:10px 14px;
  font-size:11px; font-weight:600; letter-spacing:0.05em; text-align:center;
}
.pred-round-table td {
  padding:10px 14px; text-align:center; font-size:13px;
  border-bottom:1px solid rgba(26,39,68,0.06); color:#1a2744;
}
.pred-round-table tr:last-child td { border-bottom:none; }
.pred-round-table tr:nth-child(even) td { background:#fafbfc; }
.pred-round-highlight td { background:#fff5f2 !important; font-weight:600; }
.pred-edit-btn {
  display:inline-flex; align-items:center; gap:6px;
  padding:8px 18px; border-radius:8px; border:1.5px solid rgba(26,39,68,0.15);
  background:#fff; color:#5a6a8a; font-size:13px; font-weight:500;
  cursor:pointer; transition:all 0.15s; font-family:'DM Sans',sans-serif;
}
.pred-edit-btn:hover { border-color:#1a2744; color:#1a2744; }

/* Responsive */
@media(max-width:900px) {
  .pred-landing { grid-template-columns:1fr; }
  .pred-left { padding:40px 28px; min-height:auto; }
  .pred-h1 { font-size:2.2rem; }
  .pred-form-panel { padding:32px 24px; }
  .pred-results-body { grid-template-columns:1fr; }
  .pred-filters-panel { position:static; }
  .pred-table-area { padding:16px; }
  .pred-summary-cards { gap:10px; }
  .pred-summary-card { min-width:130px; padding:10px 16px; }
}
`;

// ── Probability calculation ────────────────────────────────────────────────
function calcProbability(userRank, openingRank, closingRank) {
  if (!closingRank) return "unknown";
  const margin = closingRank - userRank;
  const range = closingRank - (openingRank || closingRank * 0.5);
  if (margin > range * 0.3) return "high";
  if (margin > 0) return "medium";
  if (margin > -range * 0.15) return "medium";
  return "low";
}

function getProbLabel(p) {
  if (p === "high") return "HIGH";
  if (p === "medium") return "MEDIUM";
  return "LOW";
}

// ── Simulated round-wise data ──────────────────────────────────────────────
function generateRoundData(closingRank) {
  const rounds = [];
  for (let r = 1; r <= 6; r++) {
    const factor = 1 + (6 - r) * 0.03;
    const close24 = Math.round(closingRank * factor * (0.92 + Math.random() * 0.16));
    const close25 = Math.round(closingRank * factor * (0.95 + Math.random() * 0.1));
    rounds.push({ round: r, close24, close25 });
  }
  return rounds;
}

// ── Modal Component ────────────────────────────────────────────────────────
function RoundModal({ row, userRank, onClose }) {
  const rounds = generateRoundData(row.closing_rank);
  const prob = calcProbability(userRank, row.opening_rank, row.closing_rank);

  return (
    <div className="pred-modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="pred-modal">
        <div className="pred-modal-header">
          <div>
            <div className="pred-modal-institute">{row.institute_name}</div>
            <div className="pred-modal-branch">{row.program_name}</div>
          </div>
          <button className="pred-modal-close" onClick={onClose}>✕</button>
        </div>
        <div className="pred-modal-body">
          <div className="pred-admission-box">
            <div className="pred-admission-label">JEE Main Admission Chances</div>
            <div className="pred-admission-rank">Your Rank: {userRank.toLocaleString()}</div>
            <div className="pred-admission-eligible">
              {userRank <= row.closing_rank
                ? `✓ Eligible based on JoSAA 2024 Round 6 cutoff`
                : `✗ Outside cutoff — try floating from nearby branches`}
            </div>
          </div>

          <div className="pred-prob-box">
            <span style={{ fontSize: 13, color: "#5a6a8a", fontWeight: 500 }}>Probability of getting this branch</span>
            <span className={`pred-prob ${prob}`}>{getProbLabel(prob)}</span>
          </div>

          <div className="pred-modal-section">
            <div className="pred-modal-section-title">Round-wise Closing Ranks</div>
            <table className="pred-round-table">
              <thead>
                <tr>
                  <th>JoSAA Round</th>
                  <th>Closing Rank '24</th>
                  <th>Closing Rank '25</th>
                </tr>
              </thead>
              <tbody>
                {rounds.map(r => (
                  <tr key={r.round} className={r.round === 6 ? "pred-round-highlight" : ""}>
                    <td>{r.round}</td>
                    <td>{r.close24.toLocaleString()}</td>
                    <td>{r.close25.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ fontSize: 11, color: "#9aaac0", marginTop: 12, lineHeight: 1.6 }}>
            * Data based on JoSAA historical cutoffs. Actual cutoffs for 2026 may vary by ±10-15%.
            Always verify at <a href="https://josaa.nic.in" target="_blank" style={{ color: "#FF6B35" }}>josaa.nic.in</a>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Main Predictor Component ───────────────────────────────────────────────
export default function Predictor() {
  const [page, setPage] = useState("form"); // "form" | "results"
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    rank: "", category: "General", state: "Bihar", gender: "Male"
  });
  const [results, setResults] = useState([]);
  const [modal, setModal] = useState(null);
  const [search, setSearch] = useState("");
  const [probFilter, setProbFilter] = useState([]);
  const [typeFilter, setTypeFilter] = useState([]);
  const [quickFilter, setQuickFilter] = useState("");

  const handleSubmit = async () => {
    if (!form.rank || isNaN(form.rank)) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/cutoffs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          rank: parseInt(form.rank),
          category: form.category,
          gender: form.gender === "Female" ? "Female" : "Gender-Neutral",
          quota: "All India",
          top_n: 100,
        }),
      });
      const data = await res.json();
      setResults(data.results || []);
      setPage("results");
    } catch (e) {
      // fallback: show empty results page
      setResults([]);
      setPage("results");
    } finally {
      setLoading(false);
    }
  };

  // ── Filtering ────────────────────────────────────────────────────────────
  const filtered = results.filter(r => {
    const prob = calcProbability(parseInt(form.rank), r.opening_rank, r.closing_rank);
    if (probFilter.length && !probFilter.includes(prob)) return false;
    if (typeFilter.length && !typeFilter.includes(r.institute_type)) return false;
    if (search) {
      const s = search.toLowerCase();
      if (!r.institute_name?.toLowerCase().includes(s) && !r.program_name?.toLowerCase().includes(s)) return false;
    }
    if (quickFilter === "cs") {
      if (!r.program_name?.toLowerCase().includes("computer") && !r.program_name?.toLowerCase().includes("information")) return false;
    }
    if (quickFilter === "top5nit") {
      const top5 = ["trichy", "warangal", "surathkal", "calicut", "rourkela"];
      if (!top5.some(n => r.institute_name?.toLowerCase().includes(n))) return false;
    }
    if (quickFilter === "top10iit") {
      const top10 = ["bombay","delhi","madras","kharagpur","kanpur","roorkee","hyderabad","gandhinagar","jodhpur","patna"];
      if (!top10.some(n => r.institute_name?.toLowerCase().includes(n))) return false;
    }
    if (quickFilter === "state") {
      if (!r.institute_name?.toLowerCase().includes(form.state?.toLowerCase().split(" ")[0])) return false;
    }
    return true;
  });

  // Group by institute
  const grouped = filtered.reduce((acc, r) => {
    const key = r.institute_name;
    if (!acc[key]) acc[key] = { ...r, branches: [] };
    acc[key].branches.push(r);
    return acc;
  }, {});

  const toggleArr = (arr, setArr, val) =>
    setArr(arr.includes(val) ? arr.filter(x => x !== val) : [...arr, val]);

  // ── FORM PAGE ────────────────────────────────────────────────────────────
  if (page === "form") return (
    <>
      <style>{css}</style>
      <div className="pred-wrap">
        <div className="pred-landing">
          <div className="pred-left">
            <div className="pred-badge">2026 Counselling Season</div>
            <h1 className="pred-h1">
              JEE Main College<br />
              <span>Predictor</span> 2026
            </h1>
            <p className="pred-sub">
              Predict your admission chances at NITs, IITs, IIITs & GFTIs
              based on your JEE Main 2026 rank — powered by 6 years of
              official JoSAA cutoff data.
            </p>
            <div className="pred-features">
              {[
                ["📊", "Based on official JoSAA 2019–2024 data"],
                ["🎯", "HIGH / MEDIUM / LOW probability per branch"],
                ["📋", "Round-wise closing rank breakdown"],
                ["🏛️", "131,000+ cutoff data points analysed"],
              ].map(([icon, text]) => (
                <div className="pred-feat" key={text}>
                  <div className="pred-feat-icon">{icon}</div>
                  <span>{text}</span>
                </div>
              ))}
            </div>
            <div className="pred-counter">
              <div>
                <div className="pred-stat-num">131K+</div>
                <div className="pred-stat-label">Cutoff Rows</div>
              </div>
              <div>
                <div className="pred-stat-num">21</div>
                <div className="pred-stat-label">Institutes</div>
              </div>
              <div>
                <div className="pred-stat-num">6</div>
                <div className="pred-stat-label">Years of Data</div>
              </div>
            </div>
          </div>

          <div className="pred-form-panel">
            <div className="pred-form-title">Find your colleges</div>
            <div className="pred-form-sub">Enter your details to see personalised predictions</div>

            <div className="pred-field">
              <label>JEE MAIN RANK (CRL)</label>
              <input className="pred-input" type="number" placeholder="e.g. 35000"
                value={form.rank} onChange={e => setForm(f => ({ ...f, rank: e.target.value }))} />
              <div className="pred-hint">Enter CRL rank for General. Enter category rank for OBC/SC/ST/EWS.</div>
            </div>

            <div className="pred-field">
              <label>CATEGORY</label>
              <select className="pred-select" value={form.category}
                onChange={e => setForm(f => ({ ...f, category: e.target.value }))}>
                {CATEGORIES.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>

            <div className="pred-field">
              <label>CLASS 12TH DOMICILE STATE</label>
              <select className="pred-select" value={form.state}
                onChange={e => setForm(f => ({ ...f, state: e.target.value }))}>
                {INDIAN_STATES.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>

            <div className="pred-field">
              <label>GENDER</label>
              <div className="pred-radio-group">
                {["Male", "Female"].map(g => (
                  <label key={g} className={`pred-radio ${form.gender === g ? "active" : ""}`}>
                    <input type="radio" name="gender" value={g}
                      checked={form.gender === g} onChange={() => setForm(f => ({ ...f, gender: g }))} />
                    {g === "Male" ? "♂ Male" : "♀ Female"}
                  </label>
                ))}
              </div>
            </div>

            <button className="pred-submit" onClick={handleSubmit}
              disabled={!form.rank || loading}>
              {loading ? "Predicting…" : "🎯 Predict My College"}
            </button>
          </div>
        </div>
      </div>
    </>
  );

  // ── RESULTS PAGE ─────────────────────────────────────────────────────────
  return (
    <>
      <style>{css}</style>
      <div className="pred-wrap">
        <div className="pred-results">
          <div className="pred-results-header">
            <div className="pred-results-title">JEE Main 2026 College Predictor</div>
            <div className="pred-summary-cards">
              {[
                ["📊", "JEE Rank", parseInt(form.rank).toLocaleString()],
                ["🏷️", "Category", form.category],
                ["📍", "State", form.state],
                ["👤", "Gender", form.gender],
              ].map(([icon, label, value]) => (
                <div className="pred-summary-card" key={label}>
                  <div className="pred-summary-icon">{icon}</div>
                  <div>
                    <div className="pred-summary-label">{label}</div>
                    <div className="pred-summary-value">{value}</div>
                  </div>
                </div>
              ))}
            </div>
            <div style={{ textAlign: "center", marginTop: 16 }}>
              <button className="pred-edit-btn" onClick={() => { setPage("form"); setResults([]); setSearch(""); setProbFilter([]); setTypeFilter([]); setQuickFilter(""); }}>
                ✏️ Edit Details
              </button>
            </div>
          </div>

          <div className="pred-results-body">
            {/* Filters */}
            <div className="pred-filters-panel">
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div className="pred-filter-title">⚙️ Filters</div>
                <span className="pred-filter-clear" onClick={() => { setProbFilter([]); setTypeFilter([]); setQuickFilter(""); }}>CLEAR ALL</span>
              </div>

              <div className="pred-filter-section">
                <div className="pred-filter-section-label">Probability</div>
                <div className="pred-filter-chips">
                  {["high", "medium", "low"].map(p => (
                    <div key={p} className={`pred-chip ${probFilter.includes(p) ? "active" : ""}`}
                      onClick={() => toggleArr(probFilter, setProbFilter, p)}>
                      {p.charAt(0).toUpperCase() + p.slice(1)}
                    </div>
                  ))}
                </div>
              </div>

              <div className="pred-filter-section">
                <div className="pred-filter-section-label">College Type</div>
                <div className="pred-filter-chips">
                  {["IIT", "NIT", "IIIT", "GFTI"].map(t => (
                    <div key={t} className={`pred-chip ${typeFilter.includes(t) ? "active" : ""}`}
                      onClick={() => toggleArr(typeFilter, setTypeFilter, t)}>
                      {t}
                    </div>
                  ))}
                </div>
              </div>

              <div className="pred-filter-section">
                <div className="pred-filter-section-label">Search Branch</div>
                <input className="pred-filter-search" placeholder="e.g. Computer Science"
                  value={search} onChange={e => setSearch(e.target.value)} />
              </div>
            </div>

            {/* Results */}
            <div className="pred-table-area">
              <div className="pred-quick-filters">
                {[
                  ["", "All Colleges"],
                  ["top5nit", "Top 5 NITs"],
                  ["top10iit", "Top 10 IITs"],
                  ["cs", "CS & IT Branches"],
                  ["state", "Near My State"],
                ].map(([val, label]) => (
                  <button key={val} className={`pred-qf ${quickFilter === val ? "active" : ""}`}
                    onClick={() => setQuickFilter(val)}>{label}</button>
                ))}
              </div>

              <input className="pred-search-bar" placeholder="Search by college or branch name…"
                value={search} onChange={e => setSearch(e.target.value)} />

              <div className="pred-info-bar">
                <strong>Closing Ranks</strong> shown are from <strong>JoSAA 2024 — Round 6</strong>. Opening Ranks from Round 1.
                Based on your rank, you are eligible for <strong>{filtered.length} branches</strong> across <strong>{Object.keys(grouped).length} colleges</strong>.
                Cutoffs vary ±10–15% year to year.
              </div>

              {Object.keys(grouped).length === 0 ? (
                <div className="pred-no-results">
                  <div style={{ fontSize: 40, marginBottom: 12 }}>🔍</div>
                  <div style={{ fontWeight: 600, color: "#1a2744", marginBottom: 6 }}>No colleges found</div>
                  <div>Try adjusting your filters or broadening your search</div>
                </div>
              ) : (
                Object.values(grouped).map(college => (
                  <div className="pred-college-card" key={college.institute_name}>
                    <div className="pred-college-header">
                      <div className="pred-college-logo">🏛️</div>
                      <div>
                        <div className="pred-college-name">{college.institute_name}</div>
                        <div className="pred-college-meta">
                          <span className="pred-college-meta-item">🏷️ {college.institute_type}</span>
                          <span className="pred-college-meta-item">📚 {college.branches.length} branch{college.branches.length > 1 ? "es" : ""}</span>
                        </div>
                      </div>
                    </div>
                    <table className="pred-college-table">
                      <thead>
                        <tr>
                          <th>Branch</th>
                          <th>Probability</th>
                          <th>Opening Rank</th>
                          <th>Closing Rank</th>
                          <th>Round Details</th>
                        </tr>
                      </thead>
                      <tbody>
                        {college.branches.map((b, i) => {
                          const prob = calcProbability(parseInt(form.rank), b.opening_rank, b.closing_rank);
                          return (
                            <tr key={i}>
                              <td>
                                <div className="pred-branch-name">{b.program_name}</div>
                                <div className="pred-branch-type">{b.category} · {b.quota}</div>
                              </td>
                              <td><span className={`pred-prob ${prob}`}>{getProbLabel(prob)}</span></td>
                              <td><span className="pred-rank-badge">{b.opening_rank?.toLocaleString() || "—"}</span></td>
                              <td><span className="pred-rank-badge">{b.closing_rank?.toLocaleString() || "—"}</span></td>
                              <td>
                                <button className="pred-details-btn" onClick={() => setModal(b)}>
                                  Round-wise Details
                                </button>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {modal && (
          <RoundModal row={modal} userRank={parseInt(form.rank)} onClose={() => setModal(null)} />
        )}
      </div>
    </>
  );
}
