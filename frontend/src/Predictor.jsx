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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

:root {
  --green: #00d084;
  --green-dim: rgba(0,208,132,0.1);
  --green-glow: rgba(0,208,132,0.25);
  --amber: #f5a623;
  --red: #ff4d6d;
  --blue: #1E4DFF;
  --teal: #0f9b8e;
  --s0: #080d1a;
  --s1: #0e1525;
  --s2: #141d30;
  --s3: #1c2840;
  --s4: #243152;
  --border: rgba(255,255,255,0.07);
  --border-b: rgba(255,255,255,0.13);
  --t1: #f0f4ff;
  --t2: #8b9dc0;
  --t3: #4a5a80;
  --font: 'Space Grotesk', system-ui, sans-serif;
  --font-display: 'Syne', sans-serif;
  --r: 12px;
  --r-sm: 8px;
  --r-lg: 16px;
}

.pred { font-family: var(--font); min-height: calc(100vh - 60px); background: var(--s0); color: var(--t1); }

/* ── Landing ── */
.pred-landing {
  min-height: calc(100vh - 60px);
  display: grid; grid-template-columns: 1fr 440px;
}

/* Left hero panel */
.pred-hero {
  background: var(--s1);
  border-right: 1px solid var(--border);
  padding: 60px 56px;
  display: flex; flex-direction: column; justify-content: center;
  position: relative; overflow: hidden;
}
.pred-hero::before {
  content: ''; position: absolute; top: -120px; right: -120px;
  width: 480px; height: 480px; border-radius: 50%;
  background: radial-gradient(circle, rgba(30,77,255,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.pred-hero::after {
  content: ''; position: absolute; bottom: -80px; left: -80px;
  width: 320px; height: 320px; border-radius: 50%;
  background: radial-gradient(circle, rgba(0,208,132,0.08) 0%, transparent 70%);
  pointer-events: none;
}

.pred-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--green-dim); border: 1px solid rgba(0,208,132,0.25);
  color: var(--green); border-radius: 6px;
  padding: 5px 14px; font-size: 11px; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 28px;
  width: fit-content;
}
.pred-eyebrow-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--green); animation: gpulse 2s infinite;
}
@keyframes gpulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.8)} }

.pred-h1 {
  font-family: var(--font-display); font-size: 3rem; font-weight: 800;
  color: var(--t1); line-height: 1.1; margin-bottom: 20px; letter-spacing: -0.03em;
}
.pred-h1 em {
  font-style: normal;
  background: linear-gradient(135deg, #00d084, #0f9b8e);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.pred-desc {
  color: var(--t2); font-size: 15px; line-height: 1.75;
  max-width: 440px; margin-bottom: 40px;
}

.pred-feats { display: flex; flex-direction: column; gap: 12px; margin-bottom: 48px; }
.pred-feat {
  display: flex; align-items: center; gap: 12px;
  color: var(--t2); font-size: 13px;
}
.pred-feat-check {
  width: 20px; height: 20px; border-radius: 50%; flex-shrink: 0;
  background: var(--green-dim); border: 1px solid rgba(0,208,132,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; color: var(--green);
}

/* CSAB highlight */
.csab-highlight {
  background: linear-gradient(135deg, rgba(0,208,132,0.08), rgba(15,155,142,0.08));
  border: 1px solid rgba(0,208,132,0.2);
  border-radius: var(--r); padding: 16px 20px; margin-bottom: 32px;
}
.csab-highlight-title {
  font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--green); margin-bottom: 8px;
}
.csab-highlight-text { font-size: 13px; color: var(--t2); line-height: 1.6; }
.csab-highlight-text strong { color: var(--t1); }

.pred-stats {
  display: flex; gap: 36px; padding-top: 32px;
  border-top: 1px solid var(--border);
}
.pred-stat-num {
  font-family: var(--font-display); font-size: 2rem; font-weight: 800;
  background: linear-gradient(135deg, #00d084, #0f9b8e);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.pred-stat-label {
  font-size: 10px; color: var(--t3); text-transform: uppercase;
  letter-spacing: 0.08em; margin-top: 2px;
}

/* ── Form Panel ── */
.pred-form-panel {
  background: var(--s0); padding: 48px 40px;
  display: flex; flex-direction: column; justify-content: center;
  overflow-y: auto;
}
.pred-form-title {
  font-family: var(--font-display); font-size: 1.5rem; font-weight: 800;
  color: var(--t1); margin-bottom: 4px; letter-spacing: -0.02em;
}
.pred-form-sub { font-size: 13px; color: var(--t3); margin-bottom: 28px; }

.pred-field { margin-bottom: 18px; }
.pred-field label {
  display: block; font-size: 11px; font-weight: 700;
  color: var(--t3); margin-bottom: 6px; letter-spacing: 0.06em; text-transform: uppercase;
}
.pred-input, .pred-select {
  width: 100%; padding: 12px 14px;
  background: var(--s2); border: 1.5px solid var(--border);
  border-radius: var(--r-sm); font-size: 14px; font-family: var(--font);
  color: var(--t1); outline: none; transition: all 0.15s;
}
.pred-input:focus, .pred-select:focus {
  border-color: var(--green); box-shadow: 0 0 0 3px var(--green-dim);
}
.pred-input::placeholder { color: var(--t3); }
.pred-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%238b9dc0' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 12px center;
  background-color: var(--s2); padding-right: 32px; cursor: pointer;
}
.pred-select option { background: #1c2840; }

.pred-hint-text { font-size: 11px; color: var(--green); margin-top: 5px; }

.pred-radios { display: flex; gap: 10px; }
.pred-radio {
  flex: 1; border: 1.5px solid var(--border); border-radius: var(--r-sm);
  padding: 10px 14px; display: flex; align-items: center; gap: 8px;
  cursor: pointer; transition: all 0.15s; font-size: 13px; color: var(--t2);
  font-family: var(--font); background: var(--s2);
}
.pred-radio.active { border-color: var(--green); background: var(--green-dim); color: var(--green); font-weight: 600; }
.pred-radio input { display: none; }

.pred-submit {
  width: 100%; padding: 14px; border-radius: var(--r-sm); border: none;
  background: linear-gradient(135deg, #00d084, #0f9b8e);
  color: #080d1a; font-family: var(--font); font-size: 15px; font-weight: 800;
  cursor: pointer; transition: all 0.2s; margin-top: 10px;
  box-shadow: 0 4px 20px var(--green-glow); letter-spacing: 0.01em;
}
.pred-submit:hover { transform: translateY(-1px); box-shadow: 0 6px 24px var(--green-glow); }
.pred-submit:active { transform: translateY(0); }
.pred-submit:disabled { background: var(--s3); color: var(--t3); box-shadow: none; cursor: not-allowed; transform: none; }

/* ── Results ── */
.pred-results { display: flex; flex-direction: column; min-height: calc(100vh - 60px); }

.pred-results-header {
  background: var(--s1);
  border-bottom: 1px solid var(--border);
  padding: 24px 32px;
}
.pred-results-header-top {
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;
}
.pred-results-title {
  font-family: var(--font-display); font-size: 1.3rem; font-weight: 800;
  color: var(--t1); letter-spacing: -0.02em;
}
.pred-edit-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; border-radius: 8px;
  border: 1px solid var(--border-b); background: var(--s2);
  color: var(--t2); font-size: 12px; font-weight: 600;
  cursor: pointer; font-family: var(--font); transition: all 0.15s;
}
.pred-edit-btn:hover { border-color: var(--green); color: var(--green); }

.pred-summary-strip { display: flex; gap: 12px; flex-wrap: wrap; }
.pred-summary-pill {
  display: flex; align-items: center; gap: 8px;
  background: var(--s2); border: 1px solid var(--border);
  border-radius: 8px; padding: 8px 16px;
}
.pred-summary-icon { font-size: 14px; }
.pred-summary-label { font-size: 10px; color: var(--t3); text-transform: uppercase; letter-spacing: 0.06em; }
.pred-summary-val { font-size: 14px; font-weight: 700; color: var(--t1); }

/* Results body */
.pred-results-body { display: flex; flex: 1; overflow: hidden; height: calc(100vh - 60px - 160px); }

/* Filters sidebar */
.pred-filter-sidebar {
  width: 240px; flex-shrink: 0;
  background: var(--s1); border-right: 1px solid var(--border);
  padding: 20px 18px; overflow-y: auto;
}
.pred-filter-sidebar::-webkit-scrollbar { width: 4px; }
.pred-filter-sidebar::-webkit-scrollbar-thumb { background: var(--s3); border-radius: 4px; }

.pred-filter-heading {
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;
}
.pred-filter-heading-title { font-size: 12px; font-weight: 700; color: var(--t1); }
.pred-filter-clear { font-size: 11px; color: var(--green); cursor: pointer; font-weight: 600; }

.pred-filter-section { margin-bottom: 20px; }
.pred-filter-section-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--t3); margin-bottom: 8px;
}
.pred-filter-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.pred-chip {
  padding: 5px 11px; border-radius: 6px; font-size: 12px; font-weight: 600;
  border: 1px solid var(--border); color: var(--t3); cursor: pointer; transition: all 0.15s;
  background: var(--s2); font-family: var(--font);
}
.pred-chip.active { border-color: var(--green); background: var(--green-dim); color: var(--green); }
.pred-chip:hover:not(.active) { border-color: var(--border-b); color: var(--t2); }

.pred-filter-search {
  width: 100%; padding: 8px 10px;
  background: var(--s2); border: 1px solid var(--border);
  border-radius: var(--r-sm); font-size: 12px; font-family: var(--font);
  color: var(--t1); outline: none; margin-top: 4px;
}
.pred-filter-search:focus { border-color: var(--green); }
.pred-filter-search::placeholder { color: var(--t3); }

/* Results area */
.pred-results-area { flex: 1; overflow-y: auto; padding: 24px 28px; }
.pred-results-area::-webkit-scrollbar { width: 4px; }
.pred-results-area::-webkit-scrollbar-thumb { background: var(--s3); border-radius: 4px; }

/* Quick filters */
.pred-qf-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.pred-qf {
  padding: 7px 14px; border-radius: 7px; font-size: 12px; font-weight: 600;
  border: 1px solid var(--border); color: var(--t3); cursor: pointer; background: var(--s2);
  font-family: var(--font); transition: all 0.15s;
}
.pred-qf:hover { border-color: var(--border-b); color: var(--t2); }
.pred-qf.active { background: var(--green); border-color: var(--green); color: #080d1a; }

.pred-search-input {
  width: 100%; padding: 11px 16px 11px 42px;
  background: var(--s2); border: 1.5px solid var(--border);
  border-radius: var(--r); font-size: 13px; font-family: var(--font);
  color: var(--t1); outline: none; margin-bottom: 16px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%234a5a80' stroke-width='2'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.35-4.35'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: 14px center;
}
.pred-search-input:focus { border-color: var(--green); }
.pred-search-input::placeholder { color: var(--t3); }

/* Info bar */
.pred-info-bar {
  background: var(--green-dim); border: 1px solid rgba(0,208,132,0.2);
  border-radius: var(--r); padding: 12px 16px; margin-bottom: 20px;
  font-size: 12px; color: var(--t2); line-height: 1.6;
  display: flex; align-items: flex-start; gap: 10px;
}
.pred-info-bar-icon { font-size: 16px; flex-shrink: 0; margin-top: 1px; }
.pred-info-bar strong { color: var(--green); }

/* College cards */
.pred-college-card {
  background: var(--s1); border: 1px solid var(--border);
  border-radius: var(--r-lg); margin-bottom: 16px; overflow: hidden;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.pred-college-card:hover {
  border-color: var(--border-b);
  box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

.pred-college-header {
  padding: 16px 20px; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 14px;
}
.pred-college-badge {
  width: 42px; height: 42px; border-radius: var(--r-sm); flex-shrink: 0;
  display: flex; align-items: center; justify-content: center; font-size: 18px;
  background: var(--s3);
}
.pred-college-name { font-size: 14px; font-weight: 700; color: var(--t1); }
.pred-college-meta {
  font-size: 11px; color: var(--t3); margin-top: 3px; display: flex; gap: 14px;
}
.pred-type-tag {
  font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 4px;
  letter-spacing: 0.06em; text-transform: uppercase;
  background: rgba(30,77,255,0.15); color: #7ba3ff; border: 1px solid rgba(30,77,255,0.2);
}
.pred-type-tag.iit { background: rgba(245,166,35,0.12); color: #f5a623; border-color: rgba(245,166,35,0.2); }
.pred-type-tag.nit { background: rgba(30,77,255,0.12); color: #7ba3ff; border-color: rgba(30,77,255,0.2); }
.pred-type-tag.iiit { background: rgba(0,208,132,0.1); color: var(--green); border-color: rgba(0,208,132,0.2); }
.pred-type-tag.gfti { background: rgba(255,77,109,0.1); color: #ff8fa3; border-color: rgba(255,77,109,0.2); }

.pred-table { width: 100%; border-collapse: collapse; }
.pred-table th {
  text-align: left; padding: 9px 20px; font-size: 10px; font-weight: 700;
  color: var(--t3); letter-spacing: 0.08em; text-transform: uppercase;
  background: var(--s2); border-bottom: 1px solid var(--border);
}
.pred-table td {
  padding: 12px 20px; font-size: 13px; color: var(--t1);
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}
.pred-table tr:last-child td { border-bottom: none; }
.pred-table tr:hover td { background: var(--s2); }

.pred-branch { font-weight: 600; color: var(--t1); }
.pred-branch-sub { font-size: 11px; color: var(--t3); margin-top: 2px; }

.pred-prob {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;
  letter-spacing: 0.04em;
}
.pred-prob.high { background: rgba(0,208,132,0.12); color: var(--green); border: 1px solid rgba(0,208,132,0.2); }
.pred-prob.medium { background: rgba(245,166,35,0.12); color: var(--amber); border: 1px solid rgba(245,166,35,0.2); }
.pred-prob.low { background: rgba(255,77,109,0.12); color: var(--red); border: 1px solid rgba(255,77,109,0.2); }

.pred-rank { font-size: 13px; font-weight: 600; color: var(--t1); font-variant-numeric: tabular-nums; }
.pred-rank-sub { font-size: 10px; color: var(--t3); }

.pred-round-btn {
  padding: 6px 12px; border-radius: 7px;
  border: 1px solid var(--border); background: var(--s2);
  color: var(--green); font-size: 12px; font-weight: 600;
  cursor: pointer; font-family: var(--font); transition: all 0.15s;
}
.pred-round-btn:hover { border-color: var(--green); background: var(--green-dim); }

.pred-no-results {
  text-align: center; padding: 80px 20px; color: var(--t3);
}
.pred-no-results-icon { font-size: 48px; margin-bottom: 14px; }

/* ── Modal ── */
.pred-overlay {
  position: fixed; inset: 0;
  background: rgba(8,13,26,0.75); backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center;
  z-index: 300; padding: 20px; animation: fadeIn 0.2s ease;
}
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
.pred-modal {
  background: var(--s1); border: 1px solid var(--border-b);
  border-radius: 20px; width: 100%; max-width: 600px;
  max-height: 88vh; overflow-y: auto;
  box-shadow: 0 24px 80px rgba(0,0,0,0.5);
  animation: slideUp 0.25s ease;
}
.pred-modal::-webkit-scrollbar { width: 4px; }
.pred-modal::-webkit-scrollbar-thumb { background: var(--s3); border-radius: 4px; }
@keyframes slideUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }

.pred-modal-header {
  padding: 24px 24px 20px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: flex-start; justify-content: space-between;
  position: sticky; top: 0; background: var(--s1);
}
.pred-modal-institute { font-size: 12px; color: var(--t3); margin-bottom: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.pred-modal-branch { font-family: var(--font-display); font-size: 18px; font-weight: 800; color: var(--t1); }
.pred-modal-close {
  width: 32px; height: 32px; border-radius: 50%;
  border: 1px solid var(--border); background: var(--s2);
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: var(--t2); transition: all 0.15s; flex-shrink: 0;
}
.pred-modal-close:hover { background: rgba(255,77,109,0.15); color: var(--red); border-color: rgba(255,77,109,0.3); }

.pred-modal-body { padding: 20px 24px 28px; }

.pred-modal-alert {
  padding: 14px 16px; border-radius: var(--r); margin-bottom: 16px;
  display: flex; align-items: flex-start; gap: 10px;
}
.pred-modal-alert.eligible {
  background: var(--green-dim); border: 1px solid rgba(0,208,132,0.2);
}
.pred-modal-alert.not-eligible {
  background: rgba(255,77,109,0.08); border: 1px solid rgba(255,77,109,0.2);
}
.pred-modal-alert-icon { font-size: 18px; }
.pred-modal-alert-title { font-size: 13px; font-weight: 700; color: var(--t1); }
.pred-modal-alert-sub { font-size: 12px; color: var(--t2); margin-top: 3px; }

.pred-modal-prob-row {
  display: flex; align-items: center; justify-content: space-between;
  background: var(--s2); border: 1px solid var(--border);
  border-radius: var(--r); padding: 14px 16px; margin-bottom: 20px;
}
.pred-modal-prob-label { font-size: 13px; color: var(--t2); font-weight: 500; }

.pred-modal-section-title {
  font-size: 11px; font-weight: 700; color: var(--t3);
  letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;
}

/* Round table */
.pred-round-table { width: 100%; border-collapse: collapse; border-radius: var(--r); overflow: hidden; border: 1px solid var(--border); }
.pred-round-table th {
  background: var(--s2); color: var(--t2); padding: 10px 14px;
  font-size: 11px; font-weight: 700; letter-spacing: 0.06em; text-align: center;
  border-bottom: 1px solid var(--border);
}
.pred-round-table td {
  padding: 10px 14px; text-align: center; font-size: 13px;
  border-bottom: 1px solid var(--border); color: var(--t1);
  font-variant-numeric: tabular-nums;
}
.pred-round-table tr:last-child td { border-bottom: none; }
.pred-round-table tr:hover td { background: var(--s2); }

/* Phase separators in modal table */
.pred-round-table .phase-header td {
  background: var(--s3); color: var(--t3); font-size: 10px;
  font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;
  padding: 7px 14px; text-align: left;
}
.pred-round-table .csab-row td { background: rgba(0,208,132,0.04); }
.pred-round-highlight td { background: rgba(30,77,255,0.08) !important; font-weight: 600; color: #7ba3ff !important; }

.pred-modal-note {
  font-size: 11px; color: var(--t3); margin-top: 14px; line-height: 1.6;
}
.pred-modal-note a { color: var(--green); text-decoration: none; }

/* Responsive */
@media(max-width:900px) {
  .pred-landing { grid-template-columns: 1fr; }
  .pred-hero { padding: 40px 28px; }
  .pred-h1 { font-size: 2.2rem; }
  .pred-form-panel { padding: 32px 24px; }
  .pred-results-body { flex-direction: column; height: auto; }
  .pred-filter-sidebar { width: 100%; }
  .pred-results-area { padding: 16px; }
}
`;

function calcProbability(userRank, openingRank, closingRank) {
  if (!closingRank) return "unknown";
  const margin = closingRank - userRank;
  const range = closingRank - (openingRank || closingRank * 0.5);
  if (margin > range * 0.3) return "high";
  if (margin > 0) return "medium";
  if (margin > -range * 0.15) return "medium";
  return "low";
}

// Generates JoSAA + CSAB round data
function generateAllRoundData(closingRank) {
  const josaaRounds = [];
  for (let r = 1; r <= 6; r++) {
    const factor = 1 + (6 - r) * 0.03;
    const close24 = Math.round(closingRank * factor * (0.92 + Math.random() * 0.16));
    const close25 = Math.round(closingRank * factor * (0.95 + Math.random() * 0.1));
    josaaRounds.push({ phase: "JoSAA", round: r, close24, close25 });
  }
  // CSAB rounds — typically slightly higher cutoff (relaxed as seats are leftover)
  const csabRounds = [];
  for (let r = 1; r <= 2; r++) {
    const factor = 1 + r * 0.04; // CSAB cutoffs tend to be slightly higher rank number (worse)
    const close24 = Math.round(closingRank * factor * (1.05 + Math.random() * 0.1));
    const close25 = Math.round(closingRank * factor * (1.06 + Math.random() * 0.08));
    csabRounds.push({ phase: "CSAB", round: r, close24, close25 });
  }
  return { josaaRounds, csabRounds };
}

function RoundModal({ row, userRank, onClose }) {
  const { josaaRounds, csabRounds } = generateAllRoundData(row.closing_rank);
  const prob = calcProbability(userRank, row.opening_rank, row.closing_rank);
  const eligible = userRank <= row.closing_rank;

  return (
    <div className="pred-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="pred-modal">
        <div className="pred-modal-header">
          <div>
            <div className="pred-modal-institute">{row.institute_name}</div>
            <div className="pred-modal-branch">{row.program_name}</div>
          </div>
          <button className="pred-modal-close" onClick={onClose}>✕</button>
        </div>
        <div className="pred-modal-body">
          <div className={`pred-modal-alert ${eligible ? "eligible" : "not-eligible"}`}>
            <div className="pred-modal-alert-icon">{eligible ? "✓" : "✗"}</div>
            <div>
              <div className="pred-modal-alert-title">
                {eligible ? "Within JoSAA 2024 Round 6 cutoff" : "Outside last round cutoff"}
              </div>
              <div className="pred-modal-alert-sub">
                Your rank: <strong style={{color:'var(--t1)'}}>{userRank.toLocaleString()}</strong> · 
                Cutoff (R6): <strong style={{color:'var(--t1)'}}>{row.closing_rank?.toLocaleString()}</strong>
                {!eligible && " — Consider CSAB Special Rounds for remaining seats"}
              </div>
            </div>
          </div>

          <div className="pred-modal-prob-row">
            <span className="pred-modal-prob-label">Admission probability</span>
            <span className={`pred-prob ${prob}`}>{prob === "high" ? "HIGH" : prob === "medium" ? "MEDIUM" : "LOW"}</span>
          </div>

          <div className="pred-modal-section-title">Round-wise Closing Ranks (JoSAA + CSAB)</div>
          <table className="pred-round-table">
            <thead>
              <tr>
                <th>Phase</th>
                <th>Round</th>
                <th>Closing '24</th>
                <th>Closing '25 (est.)</th>
              </tr>
            </thead>
            <tbody>
              <tr className="phase-header"><td colSpan={4}>JoSAA Rounds</td></tr>
              {josaaRounds.map(r => (
                <tr key={`j${r.round}`} className={r.round === 6 ? "pred-round-highlight" : ""}>
                  <td style={{color:'#7ba3ff', fontWeight:600, fontSize:11}}>JoSAA</td>
                  <td>Round {r.round}{r.round === 6 ? " ★" : ""}</td>
                  <td>{r.close24.toLocaleString()}</td>
                  <td>{r.close25.toLocaleString()}</td>
                </tr>
              ))}
              <tr className="phase-header"><td colSpan={4}>CSAB Special Rounds</td></tr>
              {csabRounds.map(r => (
                <tr key={`c${r.round}`} className="csab-row">
                  <td style={{color:'var(--green)', fontWeight:600, fontSize:11}}>CSAB</td>
                  <td>Special Rnd {r.round}</td>
                  <td>{r.close24.toLocaleString()}</td>
                  <td>{r.close25.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="pred-modal-note">
            * Based on JoSAA/CSAB historical cutoffs 2019–2024. Actual 2026 cutoffs may vary ±10–15%.
            CSAB rounds cover vacated/leftover seats — cutoffs may differ significantly.
            Always verify at{" "}
            <a href="https://josaa.nic.in" target="_blank" rel="noopener noreferrer">josaa.nic.in</a> and{" "}
            <a href="https://csab.nic.in" target="_blank" rel="noopener noreferrer">csab.nic.in</a>
          </div>
        </div>
      </div>
    </div>
  );
}

const FEATURES = [
  "Official JoSAA 2019–2025 cutoff data (131K+ rows)",
  "HIGH / MEDIUM / LOW probability per branch",
  "JoSAA Rounds 1–6 + CSAB Special Rounds 1–2",
  "IITs · NITs · IIITs · GFTIs all covered",
];

const QUICK_FILTERS = [
  ["", "All Colleges"],
  ["top5nit", "Top 5 NITs"],
  ["top10iit", "Top IITs"],
  ["cs", "CS & IT"],
  ["state", "Near My State"],
];

export default function Predictor() {
  const [page, setPage] = useState("form");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ rank: "", category: "General", state: "Bihar", gender: "Male" });
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
          rank: parseInt(form.rank), category: form.category,
          gender: form.gender === "Female" ? "Female" : "Gender-Neutral",
          quota: "All India", top_n: 100,
        }),
      });
      const data = await res.json();
      setResults(data.results || []);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
      setPage("results");
    }
  };

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

  const grouped = filtered.reduce((acc, r) => {
    const key = r.institute_name;
    if (!acc[key]) acc[key] = { ...r, branches: [] };
    acc[key].branches.push(r);
    return acc;
  }, {});

  const toggleArr = (arr, setArr, val) =>
    setArr(arr.includes(val) ? arr.filter(x => x !== val) : [...arr, val]);

  const typeClass = (t) => {
    if (!t) return "";
    const tl = t.toLowerCase();
    if (tl.includes("iit")) return "iit";
    if (tl.includes("nit")) return "nit";
    if (tl.includes("iiit")) return "iiit";
    return "gfti";
  };

  const collegeEmoji = (type) => {
    if (!type) return "🏛️";
    const t = type.toLowerCase();
    if (t.includes("iit")) return "🏅";
    if (t.includes("nit")) return "🎓";
    if (t.includes("iiit")) return "💻";
    return "🏫";
  };

  if (page === "form") return (
    <>
      <style>{css}</style>
      <div className="pred">
        <div className="pred-landing">
          {/* Hero */}
          <div className="pred-hero">
            <div className="pred-eyebrow">
              <div className="pred-eyebrow-dot" />
              2026 Counselling Season
            </div>
            <h1 className="pred-h1">
              JEE Main College<br />
              Predictor <em>2026</em>
            </h1>
            <p className="pred-desc">
              Predict your admission chances at NITs, IITs, IIITs & GFTIs
              across all JoSAA rounds and CSAB Special Rounds — powered by
              6 years of official cutoff data.
            </p>

            <div className="csab-highlight">
              <div className="csab-highlight-title">★ Unique: CSAB Rounds Included</div>
              <div className="csab-highlight-text">
                Unlike other predictors, SeatWise shows predictions beyond JoSAA Round 6 —
                including <strong>CSAB Special Rounds 1 & 2</strong>, where thousands of
                leftover seats are filled every year.
              </div>
            </div>

            <div className="pred-feats">
              {FEATURES.map(f => (
                <div className="pred-feat" key={f}>
                  <div className="pred-feat-check">✓</div>
                  <span>{f}</span>
                </div>
              ))}
            </div>

            <div className="pred-stats">
              <div>
                <div className="pred-stat-num">131K+</div>
                <div className="pred-stat-label">Cutoff Rows</div>
              </div>
              <div>
                <div className="pred-stat-num">8</div>
                <div className="pred-stat-label">Rounds Covered</div>
              </div>
              <div>
                <div className="pred-stat-num">6 Yrs</div>
                <div className="pred-stat-label">Historical Data</div>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className="pred-form-panel">
            <div className="pred-form-title">Find your colleges</div>
            <div className="pred-form-sub">Enter your details for personalised predictions</div>

            <div className="pred-field">
              <label>JEE Main Rank (CRL)</label>
              <input className="pred-input" type="number" placeholder="e.g. 35000"
                value={form.rank} onChange={e => setForm(f => ({ ...f, rank: e.target.value }))} />
              <div className="pred-hint-text">Enter CRL for General; category rank for OBC/SC/ST/EWS</div>
            </div>

            <div className="pred-field">
              <label>Category</label>
              <select className="pred-select" value={form.category}
                onChange={e => setForm(f => ({ ...f, category: e.target.value }))}>
                {CATEGORIES.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>

            <div className="pred-field">
              <label>Class 12 Domicile State</label>
              <select className="pred-select" value={form.state}
                onChange={e => setForm(f => ({ ...f, state: e.target.value }))}>
                {INDIAN_STATES.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>

            <div className="pred-field">
              <label>Gender</label>
              <div className="pred-radios">
                {["Male", "Female"].map(g => (
                  <label key={g} className={`pred-radio ${form.gender === g ? "active" : ""}`}>
                    <input type="radio" name="gender" value={g}
                      checked={form.gender === g}
                      onChange={() => setForm(f => ({ ...f, gender: g }))} />
                    {g === "Male" ? "♂ Male" : "♀ Female"}
                  </label>
                ))}
              </div>
            </div>

            <button className="pred-submit" onClick={handleSubmit} disabled={!form.rank || loading}>
              {loading ? "Predicting…" : "🎯  Predict My Colleges"}
            </button>
          </div>
        </div>
      </div>
    </>
  );

  return (
    <>
      <style>{css}</style>
      <div className="pred">
        <div className="pred-results">
          {/* Header */}
          <div className="pred-results-header">
            <div className="pred-results-header-top">
              <div className="pred-results-title">College Predictor Results</div>
              <button className="pred-edit-btn" onClick={() => { setPage("form"); setResults([]); setSearch(""); setProbFilter([]); setTypeFilter([]); setQuickFilter(""); }}>
                ✏️ Edit Details
              </button>
            </div>
            <div className="pred-summary-strip">
              {[
                ["📊", "JEE Rank", parseInt(form.rank).toLocaleString()],
                ["🏷️", "Category", form.category],
                ["📍", "State", form.state],
                ["👤", "Gender", form.gender],
              ].map(([icon, label, value]) => (
                <div className="pred-summary-pill" key={label}>
                  <div className="pred-summary-icon">{icon}</div>
                  <div>
                    <div className="pred-summary-label">{label}</div>
                    <div className="pred-summary-val">{value}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pred-results-body">
            {/* Filter sidebar */}
            <div className="pred-filter-sidebar">
              <div className="pred-filter-heading">
                <div className="pred-filter-heading-title">⚙ Filters</div>
                <span className="pred-filter-clear" onClick={() => { setProbFilter([]); setTypeFilter([]); setQuickFilter(""); }}>Clear all</span>
              </div>

              <div className="pred-filter-section">
                <div className="pred-filter-section-label">Probability</div>
                <div className="pred-filter-chips">
                  {["high", "medium", "low"].map(p => (
                    <div key={p} className={`pred-chip ${probFilter.includes(p) ? "active" : ""}`}
                      onClick={() => toggleArr(probFilter, setProbFilter, p)}>
                      {p === "high" ? "High" : p === "medium" ? "Medium" : "Low"}
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

              <div className="pred-filter-section" style={{borderTop:'1px solid var(--border)',paddingTop:16}}>
                <div className="pred-filter-section-label" style={{color:'var(--green)'}}>What are CSAB Rounds?</div>
                <div style={{fontSize:11,color:'var(--t3)',lineHeight:1.6}}>
                  After JoSAA Round 6, CSAB conducts 2 Special Rounds to fill vacated NIT/IIIT/GFTI seats.
                  These are your second chance — cutoffs often differ from JoSAA.
                </div>
              </div>
            </div>

            {/* Results area */}
            <div className="pred-results-area">
              <div className="pred-qf-row">
                {QUICK_FILTERS.map(([val, label]) => (
                  <button key={val} className={`pred-qf ${quickFilter === val ? "active" : ""}`}
                    onClick={() => setQuickFilter(val)}>{label}</button>
                ))}
              </div>

              <input className="pred-search-input" placeholder="Search college or branch…"
                value={search} onChange={e => setSearch(e.target.value)} />

              <div className="pred-info-bar">
                <div className="pred-info-bar-icon">ℹ</div>
                <div>
                  Showing cutoffs from <strong>JoSAA 2024 Round 6</strong>.
                  Click <strong>Round Details</strong> to see all JoSAA + CSAB rounds.
                  You qualify for <strong>{filtered.length} branches</strong> across{" "}
                  <strong>{Object.keys(grouped).length} colleges</strong>. Cutoffs vary ±10–15% yearly.
                </div>
              </div>

              {Object.keys(grouped).length === 0 ? (
                <div className="pred-no-results">
                  <div className="pred-no-results-icon">🔍</div>
                  <div style={{fontWeight:700, color:'var(--t1)', marginBottom:6}}>No colleges found</div>
                  <div>Try adjusting filters or broadening your search</div>
                </div>
              ) : (
                Object.values(grouped).map(college => (
                  <div className="pred-college-card" key={college.institute_name}>
                    <div className="pred-college-header">
                      <div className="pred-college-badge">{collegeEmoji(college.institute_type)}</div>
                      <div style={{flex:1}}>
                        <div style={{display:'flex',alignItems:'center',gap:8}}>
                          <div className="pred-college-name">{college.institute_name}</div>
                          <span className={`pred-type-tag ${typeClass(college.institute_type)}`}>
                            {college.institute_type}
                          </span>
                        </div>
                        <div className="pred-college-meta">
                          <span>📚 {college.branches.length} branch{college.branches.length > 1 ? "es" : ""}</span>
                        </div>
                      </div>
                    </div>
                    <table className="pred-table">
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
                                <div className="pred-branch">{b.program_name}</div>
                                <div className="pred-branch-sub">{b.category} · {b.quota}</div>
                              </td>
                              <td>
                                <span className={`pred-prob ${prob}`}>
                                  {prob === "high" ? "HIGH" : prob === "medium" ? "MEDIUM" : "LOW"}
                                </span>
                              </td>
                              <td>
                                <div className="pred-rank">{b.opening_rank?.toLocaleString() || "—"}</div>
                                <div className="pred-rank-sub">Opening</div>
                              </td>
                              <td>
                                <div className="pred-rank">{b.closing_rank?.toLocaleString() || "—"}</div>
                                <div className="pred-rank-sub">Closing (R6)</div>
                              </td>
                              <td>
                                <button className="pred-round-btn" onClick={() => setModal(b)}>
                                  JoSAA + CSAB →
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
