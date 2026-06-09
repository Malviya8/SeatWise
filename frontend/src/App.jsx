import { useState, useRef, useEffect, useCallback } from "react";

const API = import.meta.env.VITE_API_URL || "https://seatwise-production-7b03.up.railway.app";

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --blue: #1E4DFF;
    --blue-dim: rgba(30,77,255,0.12);
    --blue-glow: rgba(30,77,255,0.3);
    --teal: #0f9b8e;
    --teal-dim: rgba(15,155,142,0.12);
    --surface-0: #080d1a;
    --surface-1: #0e1525;
    --surface-2: #141d30;
    --surface-3: #1c2840;
    --border: rgba(255,255,255,0.07);
    --border-bright: rgba(255,255,255,0.14);
    --text-1: #f0f4ff;
    --text-2: #8b9dc0;
    --text-3: #4a5a80;
    --accent-grad: linear-gradient(135deg, #1E4DFF, #0f9b8e);
    --r: 12px;
    --r-sm: 8px;
    --r-lg: 16px;
    --font: 'Space Grotesk', system-ui, sans-serif;
    --font-display: 'Syne', sans-serif;
  }

  .chat-root {
    display: flex; height: calc(100vh - 60px);
    background: var(--surface-0); font-family: var(--font);
    color: var(--text-1); overflow: hidden;
  }

  /* ── Sidebar ── */
  .chat-sidebar {
    width: 272px; flex-shrink: 0;
    background: var(--surface-1);
    border-right: 1px solid var(--border);
    display: flex; flex-direction: column; overflow: hidden;
  }

  .sidebar-header {
    padding: 20px 20px 16px;
    border-bottom: 1px solid var(--border);
  }
  .sidebar-header-title {
    font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--text-3); margin-bottom: 14px;
  }

  .context-card {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r); padding: 14px; margin-bottom: 10px;
  }
  .context-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--text-3); margin-bottom: 8px;
  }

  .filter-row { margin-bottom: 10px; }
  .filter-row:last-child { margin-bottom: 0; }
  .filter-label {
    font-size: 11px; color: var(--text-2); margin-bottom: 5px; font-weight: 500;
  }
  .filter-input, .filter-select {
    width: 100%; padding: 8px 11px;
    background: var(--surface-3); border: 1px solid var(--border);
    border-radius: var(--r-sm); font-size: 13px; font-family: var(--font);
    color: var(--text-1); outline: none; transition: border-color 0.15s;
  }
  .filter-input:focus, .filter-select:focus { border-color: var(--blue); }
  .filter-select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%238b9dc0' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 10px center;
    background-color: var(--surface-3); padding-right: 28px; cursor: pointer;
  }
  .filter-select option { background: #1c2840; }

  .btn-find {
    width: 100%; padding: 10px; border: none; border-radius: var(--r-sm);
    background: var(--accent-grad); color: white; font-family: var(--font);
    font-size: 13px; font-weight: 700; cursor: pointer; transition: opacity 0.15s;
    margin-top: 12px; letter-spacing: 0.02em;
  }
  .btn-find:hover { opacity: 0.88; }

  .sidebar-divider {
    height: 1px; background: var(--border); margin: 4px 0;
  }

  .sidebar-scroll { flex: 1; overflow-y: auto; padding: 16px 20px; }
  .sidebar-scroll::-webkit-scrollbar { width: 4px; }
  .sidebar-scroll::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 4px; }

  .sq-section-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--text-3); margin-bottom: 10px;
  }
  .sq-list { display: flex; flex-direction: column; gap: 6px; }
  .sq-item {
    padding: 10px 12px; background: var(--surface-2);
    border: 1px solid var(--border); border-radius: var(--r-sm);
    font-size: 12px; color: var(--text-2); cursor: pointer;
    line-height: 1.45; transition: all 0.15s; text-align: left; width: 100%;
    font-family: var(--font);
  }
  .sq-item:hover { border-color: var(--blue); color: var(--text-1); background: var(--blue-dim); }

  /* ── Main chat ── */
  .chat-main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

  /* Top banner — identity strip */
  .chat-identity-bar {
    display: flex; align-items: center; gap: 14px;
    padding: 10px 24px; background: var(--surface-1);
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
  }
  .identity-icon {
    width: 38px; height: 38px; border-radius: 10px; flex-shrink: 0;
    background: var(--accent-grad);
    display: flex; align-items: center; justify-content: center; font-size: 18px;
  }
  .identity-text { flex: 1; }
  .identity-title {
    font-family: var(--font-display); font-size: 15px; font-weight: 700;
    color: var(--text-1); line-height: 1.2;
  }
  .identity-sub { font-size: 11px; color: var(--text-3); margin-top: 2px; }
  .identity-actions { display: flex; align-items: center; gap: 8px; }
  .badge-live {
    display: flex; align-items: center; gap: 5px;
    background: rgba(15,155,142,0.15); border: 1px solid rgba(15,155,142,0.3);
    color: #4de8dc; border-radius: 99px; padding: 4px 10px; font-size: 11px; font-weight: 600;
  }
  .badge-live::before {
    content: ''; width: 5px; height: 5px; border-radius: 50%; background: #4de8dc;
    animation: pulse 2s infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.25} }
  .btn-reset {
    padding: 6px 14px; border-radius: 7px;
    border: 1px solid var(--border-bright);
    background: transparent; color: var(--text-2);
    font-size: 12px; font-family: var(--font); cursor: pointer;
    transition: all 0.15s; font-weight: 600;
  }
  .btn-reset:hover { border-color: rgba(255,255,255,0.3); color: var(--text-1); }

  /* Chat area */
  .chat-area {
    flex: 1; overflow-y: auto; padding: 28px 32px;
    display: flex; flex-direction: column; gap: 24px;
    scroll-behavior: smooth;
  }
  .chat-area::-webkit-scrollbar { width: 4px; }
  .chat-area::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 4px; }

  /* Welcome */
  .welcome {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 40px; gap: 0;
    min-height: 60vh;
  }
  .welcome-orbit {
    width: 80px; height: 80px; border-radius: 20px; margin-bottom: 24px;
    background: var(--accent-grad);
    display: flex; align-items: center; justify-content: center;
    font-size: 36px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.08), 0 8px 32px var(--blue-glow);
    position: relative;
  }
  .welcome-title {
    font-family: var(--font-display); font-size: 2rem; font-weight: 800;
    color: var(--text-1); line-height: 1.15; margin-bottom: 12px;
    letter-spacing: -0.02em;
  }
  .welcome-title span {
    background: var(--accent-grad); -webkit-background-clip: text;
    -webkit-text-fill-color: transparent; background-clip: text;
  }
  .welcome-sub {
    font-size: 14px; color: var(--text-2); max-width: 400px;
    line-height: 1.7; margin-bottom: 28px;
  }
  .welcome-tags { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
  .welcome-tag {
    padding: 8px 16px; border-radius: 99px;
    border: 1px solid var(--border-bright); background: var(--surface-2);
    font-size: 12px; color: var(--text-2); cursor: pointer; transition: all 0.15s;
    font-family: var(--font); font-weight: 500;
  }
  .welcome-tag:hover { border-color: var(--blue); color: var(--text-1); background: var(--blue-dim); }

  /* Coverage strip */
  .coverage-strip {
    display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin-top: 20px;
  }
  .cov-badge {
    padding: 4px 10px; border-radius: 6px;
    background: var(--surface-3); border: 1px solid var(--border);
    font-size: 10px; font-weight: 700; color: var(--text-3);
    letter-spacing: 0.05em; text-transform: uppercase;
  }
  .cov-badge.highlight {
    background: rgba(15,155,142,0.1); border-color: rgba(15,155,142,0.25);
    color: var(--teal);
  }

  /* Messages */
  .msg { display: flex; gap: 14px; animation: fadeUp 0.25s ease; }
  @keyframes fadeUp { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
  .msg.user { flex-direction: row-reverse; }

  .msg-avatar {
    width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700;
  }
  .msg.user .msg-avatar {
    background: var(--blue); color: white;
    box-shadow: 0 2px 8px var(--blue-glow);
  }
  .msg.bot .msg-avatar {
    background: var(--accent-grad);
    font-size: 16px;
  }

  .msg-body { max-width: 72%; display: flex; flex-direction: column; gap: 8px; }
  .msg.user .msg-body { align-items: flex-end; }

  .bubble {
    padding: 13px 17px; border-radius: var(--r-lg);
    font-size: 14px; line-height: 1.7;
  }
  .msg.user .bubble {
    background: var(--blue);
    color: white; border-bottom-right-radius: 4px;
    box-shadow: 0 2px 12px var(--blue-glow);
  }
  .msg.bot .bubble {
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-1); border-bottom-left-radius: 4px;
    white-space: pre-wrap;
  }
  .bubble ul, .bubble ol { padding-left: 18px; }
  .bubble li { margin: 4px 0; color: var(--text-2); }
  .bubble strong { color: var(--text-1); font-weight: 600; }

  /* Typing */
  .typing-row { display: flex; gap: 14px; align-items: flex-start; }
  .typing-bubble {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r-lg); border-bottom-left-radius: 4px;
    padding: 14px 18px; display: flex; align-items: center; gap: 10px;
  }
  .dots { display: flex; gap: 5px; }
  .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--blue); opacity: 0.4; animation: bounce 1.2s infinite;
  }
  .dot:nth-child(2) { animation-delay: 0.2s; }
  .dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce { 0%,80%,100%{opacity:0.4;transform:translateY(0)} 40%{opacity:1;transform:translateY(-3px)} }
  .typing-label { font-size: 12px; color: var(--text-3); }

  /* Sources */
  .sources { display: flex; flex-wrap: wrap; gap: 6px; }
  .source-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: var(--teal-dim); border: 1px solid rgba(15,155,142,0.2);
    color: var(--teal); border-radius: 6px; padding: 3px 9px;
    font-size: 10px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;
  }
  .source-badge::before { content: '◎'; font-size: 8px; }

  .meta-row { display: flex; align-items: center; gap: 6px; }
  .meta-pill {
    background: var(--surface-3); border: 1px solid var(--border);
    border-radius: 5px; padding: 2px 8px;
    font-size: 10px; color: var(--text-3); font-weight: 600;
    letter-spacing: 0.04em; text-transform: uppercase;
  }

  /* Input bar */
  .input-bar {
    padding: 16px 24px 20px;
    border-top: 1px solid var(--border);
    background: var(--surface-1); flex-shrink: 0;
  }
  .input-row { display: flex; gap: 10px; align-items: flex-end; }
  .input-wrap { flex: 1; position: relative; }
  .input-field {
    width: 100%; padding: 13px 48px 13px 18px;
    background: var(--surface-2); border: 1.5px solid var(--border);
    border-radius: var(--r); font-size: 14px; font-family: var(--font);
    color: var(--text-1); outline: none; resize: none; max-height: 120px;
    line-height: 1.5; transition: border-color 0.15s;
  }
  .input-field:focus { border-color: var(--blue); }
  .input-field::placeholder { color: var(--text-3); }
  .send-btn {
    position: absolute; right: 10px; bottom: 10px;
    width: 34px; height: 34px; border-radius: 9px; border: none;
    background: var(--accent-grad); color: white; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.15s; box-shadow: 0 2px 8px var(--blue-glow);
  }
  .send-btn:hover:not(:disabled) { opacity: 0.85; transform: scale(1.05); }
  .send-btn:disabled { background: var(--surface-3); box-shadow: none; cursor: not-allowed; }
  .send-btn svg { width: 15px; height: 15px; }
  .input-hint {
    font-size: 11px; color: var(--text-3); margin-top: 8px;
    text-align: center; letter-spacing: 0.02em;
  }
`;

const SUGGESTED = [
  "What is the float option in JoSAA counselling?",
  "Which NITs can I get with rank 25,000 General?",
  "How should I fill choices strategically?",
  "What documents are needed for online reporting?",
  "Explain CSAB Special Rounds — who should apply?",
  "OBC-NCL vs General quota cutoff difference?",
  "What happens if I don't respond in a JoSAA round?",
  "Best branches at NIT Patna for rank 60,000?",
];

const CATEGORY_OPTIONS = ["", "General", "OBC-NCL", "SC", "ST", "EWS"];
const INST_OPTIONS = ["", "IIT", "NIT", "IIIT", "GFTI"];
const QUOTA_OPTIONS = ["", "All India", "Home State", "Other State"];

function formatMessage(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/^- (.+)/gm, "<li>$1</li>")
    .replace(/(<li>.*<\/li>\n?)+/g, s => `<ul>${s}</ul>`)
    .replace(/^(\d+)\. (.+)/gm, "<li>$2</li>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br/>");
}

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({ rank: "", category: "", institute_type: "", quota: "" });
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const autoResize = () => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 120) + "px";
  };

  const buildQuestion = (q) => {
    let enriched = q;
    if (filters.rank) enriched += ` My JEE rank is ${filters.rank}.`;
    if (filters.category) enriched += ` I belong to ${filters.category} category.`;
    if (filters.quota) enriched += ` I am interested in ${filters.quota} quota.`;
    if (filters.institute_type) enriched += ` I am specifically interested in ${filters.institute_type}s.`;
    return enriched;
  };

  const send = useCallback(async (q = null) => {
    const question = (q || input).trim();
    if (!question || loading) return;
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";

    setMessages(prev => [...prev, { role: "user", content: question }]);
    setLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: buildQuestion(question) }),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setMessages(prev => [...prev, {
        role: "bot", content: data.answer, sources: data.sources,
        intent: data.intent, latency: data.latency_ms,
        cutoff_rows: data.cutoff_rows_used, doc_chunks: data.doc_chunks_used,
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "bot",
        content: `⚠️ Couldn't reach the backend. Make sure the server is running.\n\nError: ${err.message}`,
        sources: [], intent: "ERROR",
      }]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, filters]);

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
  };

  const reset = async () => {
    try { await fetch(`${API}/reset`, { method: "POST" }); } catch {}
    setMessages([]);
  };

  return (
    <>
      <style>{css}</style>
      <div className="chat-root">
        {/* Sidebar */}
        <aside className="chat-sidebar">
          <div className="sidebar-header">
            <div className="sidebar-header-title">Your Profile</div>
            <div className="context-card">
              <div className="context-label">Quick Filters</div>
              <div className="filter-row">
                <div className="filter-label">JEE Rank</div>
                <input
                  className="filter-input" type="number" placeholder="e.g. 25000"
                  value={filters.rank}
                  onChange={e => setFilters(f => ({ ...f, rank: e.target.value }))}
                />
              </div>
              <div className="filter-row">
                <div className="filter-label">Category</div>
                <select className="filter-select" value={filters.category}
                  onChange={e => setFilters(f => ({ ...f, category: e.target.value }))}>
                  {CATEGORY_OPTIONS.map(o => <option key={o} value={o}>{o || "Select category"}</option>)}
                </select>
              </div>
              <div className="filter-row">
                <div className="filter-label">Institute Type</div>
                <select className="filter-select" value={filters.institute_type}
                  onChange={e => setFilters(f => ({ ...f, institute_type: e.target.value }))}>
                  {INST_OPTIONS.map(o => <option key={o} value={o}>{o || "All institutes"}</option>)}
                </select>
              </div>
              <div className="filter-row">
                <div className="filter-label">Quota</div>
                <select className="filter-select" value={filters.quota}
                  onChange={e => setFilters(f => ({ ...f, quota: e.target.value }))}>
                  {QUOTA_OPTIONS.map(o => <option key={o} value={o}>{o || "Any quota"}</option>)}
                </select>
              </div>
              <button className="btn-find"
                onClick={() => filters.rank && send("Which colleges can I get?")}>
                Find My Colleges →
              </button>
            </div>
          </div>

          <div className="sidebar-scroll">
            <div className="sq-section-label">Ask anything</div>
            <div className="sq-list">
              {SUGGESTED.map(q => (
                <button key={q} className="sq-item" onClick={() => send(q)}>{q}</button>
              ))}
            </div>
          </div>
        </aside>

        {/* Main */}
        <main className="chat-main">
          {/* Identity bar */}
          <div className="chat-identity-bar">
            <div className="identity-icon">🎓</div>
            <div className="identity-text">
              <div className="identity-title">SeatWise AI Counsellor</div>
              <div className="identity-sub">JoSAA · CSAB · Cutoffs · Choice Filling · Strategy</div>
            </div>
            <div className="identity-actions">
              <div className="badge-live">Live</div>
              <button className="btn-reset" onClick={reset}>New chat</button>
            </div>
          </div>

          {/* Chat */}
          <div className="chat-area">
            {messages.length === 0 ? (
              <div className="welcome">
                <div className="welcome-orbit">🎓</div>
                <div className="welcome-title">
                  Your JEE counsellor,<br /><span>powered by AI</span>
                </div>
                <div className="welcome-sub">
                  Ask anything about JoSAA & CSAB — seat allotment, cutoffs,
                  float/freeze/slide strategy, category quotas, or choice filling.
                </div>
                <div className="coverage-strip">
                  {["JoSAA Rnd 1–6", "CSAB Special Rnd 1–2", "IIT · NIT · IIIT · GFTI", "2019–2025 Data"].map((t, i) => (
                    <span key={t} className={`cov-badge ${i >= 1 && i <= 1 ? "highlight" : ""}`}>{t}</span>
                  ))}
                </div>
                <div className="welcome-tags" style={{ marginTop: 24 }}>
                  {SUGGESTED.slice(0, 4).map(q => (
                    <button key={q} className="welcome-tag" onClick={() => send(q)}>{q}</button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((msg, i) => (
                <div key={i} className={`msg ${msg.role}`}>
                  <div className="msg-avatar">
                    {msg.role === "user" ? "U" : "🎓"}
                  </div>
                  <div className="msg-body">
                    <div
                      className="bubble"
                      dangerouslySetInnerHTML={{
                        __html: msg.role === "bot"
                          ? formatMessage(msg.content)
                          : msg.content
                      }}
                    />
                    {msg.role === "bot" && msg.sources?.length > 0 && (
                      <div className="sources">
                        {msg.sources.map((s, si) => (
                          <span key={si} className="source-badge">{s}</span>
                        ))}
                      </div>
                    )}
                    {msg.role === "bot" && msg.intent && msg.intent !== "ERROR" && (
                      <div className="meta-row">
                        <span className="meta-pill">{msg.intent}</span>
                        {msg.cutoff_rows > 0 && <span className="meta-pill">{msg.cutoff_rows} rows</span>}
                        {msg.doc_chunks > 0 && <span className="meta-pill">{msg.doc_chunks} chunks</span>}
                        {msg.latency && <span style={{fontSize:10,color:'var(--text-3)'}}>{(msg.latency/1000).toFixed(1)}s</span>}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}

            {loading && (
              <div className="typing-row">
                <div className="msg-avatar" style={{
                  width:34,height:34,borderRadius:10,flexShrink:0,
                  background:'linear-gradient(135deg,#1E4DFF,#0f9b8e)',
                  display:'flex',alignItems:'center',justifyContent:'center',fontSize:16
                }}>🎓</div>
                <div className="typing-bubble">
                  <div className="dots">
                    <div className="dot" /><div className="dot" /><div className="dot" />
                  </div>
                  <span className="typing-label">Searching cutoffs & guidelines…</span>
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="input-bar">
            <div className="input-row">
              <div className="input-wrap">
                <textarea
                  ref={textareaRef}
                  className="input-field"
                  rows={1}
                  placeholder="Ask about JoSAA, CSAB, cutoffs, strategy, choice filling…"
                  value={input}
                  onChange={e => { setInput(e.target.value); autoResize(); }}
                  onKeyDown={handleKey}
                  disabled={loading}
                />
                <button
                  className="send-btn"
                  onClick={() => send()}
                  disabled={!input.trim() || loading}
                  aria-label="Send"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="input-hint">Enter to send · Shift+Enter for new line · Profile filters auto-applied</div>
          </div>
        </main>
      </div>
    </>
  );
}
