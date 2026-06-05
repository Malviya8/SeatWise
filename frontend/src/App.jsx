import { useState, useRef, useEffect, useCallback } from "react";

const API = "http://localhost:8000";

const SAFFRON = "#FF6B35";
const NAVY = "#1a2744";
const TEAL = "#0f9b8e";

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --saffron: #FF6B35;
    --saffron-light: #fff2ed;
    --saffron-mid: #ffe0d0;
    --navy: #1a2744;
    --navy-mid: #2a3d6e;
    --teal: #0f9b8e;
    --teal-light: #e0f5f4;
    --cream: #fdfaf6;
    --surface: #ffffff;
    --border: rgba(26,39,68,0.1);
    --border-strong: rgba(26,39,68,0.2);
    --text-primary: #1a2744;
    --text-secondary: #5a6a8a;
    --text-muted: #9aaac0;
    --shadow-sm: 0 1px 3px rgba(26,39,68,0.08);
    --shadow-md: 0 4px 16px rgba(26,39,68,0.1);
    --shadow-lg: 0 8px 32px rgba(26,39,68,0.12);
    --r: 12px;
    --r-sm: 8px;
    --r-lg: 18px;
    --font-display: 'Playfair Display', Georgia, serif;
    --font-body: 'DM Sans', system-ui, sans-serif;
  }

  body { font-family: var(--font-body); background: var(--cream); color: var(--text-primary); min-height: 100vh; }

  .app { display: flex; flex-direction: column; height: 100vh; max-width: 1100px; margin: 0 auto; }

  /* ── Header ── */
  .header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 24px; background: var(--navy);
    border-bottom: 3px solid var(--saffron);
    flex-shrink: 0;
  }
  .header-brand { display: flex; align-items: center; gap: 12px; }
  .header-logo {
    width: 36px; height: 36px; border-radius: 50%;
    background: var(--saffron); display: flex; align-items: center; justify-content: center;
    font-family: var(--font-display); color: white; font-size: 16px; font-weight: 700;
    flex-shrink: 0;
  }
  .header-title { font-family: var(--font-display); color: white; font-size: 1.2rem; font-weight: 700; line-height: 1.1; }
  .header-sub { color: rgba(255,255,255,0.55); font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px; }
  .header-actions { display: flex; align-items: center; gap: 10px; }
  .badge-live {
    display: flex; align-items: center; gap: 5px;
    background: rgba(15,155,142,0.2); border: 1px solid rgba(15,155,142,0.4);
    color: #5eeee6; border-radius: 99px; padding: 4px 10px; font-size: 11px; font-weight: 500;
  }
  .badge-live::before {
    content: ''; width: 6px; height: 6px; border-radius: 50%; background: #5eeee6;
    animation: pulse 2s infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
  .btn-ghost {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.7); border-radius: var(--r-sm); padding: 6px 12px;
    font-size: 12px; font-family: var(--font-body); cursor: pointer; transition: all 0.15s;
  }
  .btn-ghost:hover { background: rgba(255,255,255,0.14); color: white; }

  /* ── Layout ── */
  .layout { display: flex; flex: 1; overflow: hidden; }
  .sidebar {
    width: 280px; flex-shrink: 0; background: var(--surface);
    border-right: 1px solid var(--border); overflow-y: auto; padding: 20px 16px;
    display: flex; flex-direction: column; gap: 16px;
  }
  .main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

  /* ── Sidebar ── */
  .sidebar-section-label {
    font-size: 10px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--text-muted); padding: 0 4px; margin-bottom: 6px;
  }
  .filter-group { display: flex; flex-direction: column; gap: 6px; }
  .filter-label { font-size: 12px; color: var(--text-secondary); padding: 0 2px; font-weight: 500; }
  .filter-input {
    width: 100%; padding: 8px 10px; border: 1px solid var(--border);
    border-radius: var(--r-sm); font-size: 13px; font-family: var(--font-body);
    background: var(--cream); color: var(--text-primary); outline: none; transition: border 0.15s;
  }
  .filter-input:focus { border-color: var(--saffron); background: white; }
  .filter-select {
    width: 100%; padding: 8px 10px; border: 1px solid var(--border);
    border-radius: var(--r-sm); font-size: 13px; font-family: var(--font-body);
    background: var(--cream); color: var(--text-primary); outline: none; cursor: pointer;
    appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%235a6a8a' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 10px center;
    padding-right: 28px; transition: border 0.15s;
  }
  .filter-select:focus { border-color: var(--saffron); background-color: white; }
  .btn-apply {
    width: 100%; padding: 9px; border-radius: var(--r-sm); border: none;
    background: var(--saffron); color: white; font-family: var(--font-body);
    font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s;
  }
  .btn-apply:hover { background: #e05520; }
  .btn-apply:active { transform: scale(0.98); }

  /* Divider */
  .divider { border: none; border-top: 1px solid var(--border); margin: 4px 0; }

  /* Suggested questions */
  .sq-item {
    background: var(--cream); border: 1px solid var(--border); border-radius: var(--r-sm);
    padding: 9px 11px; font-size: 12px; color: var(--text-secondary);
    cursor: pointer; line-height: 1.4; transition: all 0.15s; width: 100%; text-align: left;
  }
  .sq-item:hover { border-color: var(--saffron); color: var(--saffron); background: var(--saffron-light); }
  .sq-list { display: flex; flex-direction: column; gap: 6px; }

  /* ── Chat area ── */
  .chat-area { flex: 1; overflow-y: auto; padding: 24px 28px; display: flex; flex-direction: column; gap: 20px; }

  /* Welcome state */
  .welcome {
    flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 20px; text-align: center; padding: 40px;
  }
  .welcome-icon {
    width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, var(--saffron) 0%, #ff9f1c 100%);
    display: flex; align-items: center; justify-content: center; font-family: var(--font-display);
    color: white; font-size: 28px; font-weight: 700; box-shadow: 0 8px 24px rgba(255,107,53,0.3);
  }
  .welcome-title { font-family: var(--font-display); font-size: 1.8rem; color: var(--navy); }
  .welcome-sub { font-size: 14px; color: var(--text-secondary); max-width: 420px; line-height: 1.6; }
  .welcome-chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 8px; }
  .chip {
    background: white; border: 1px solid var(--border); border-radius: 99px;
    padding: 7px 14px; font-size: 12px; color: var(--text-secondary);
    cursor: pointer; transition: all 0.15s;
  }
  .chip:hover { border-color: var(--saffron); color: var(--saffron); background: var(--saffron-light); }

  /* Message bubbles */
  .msg { display: flex; gap: 12px; animation: fadeUp 0.3s ease; }
  @keyframes fadeUp { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
  .msg.user { flex-direction: row-reverse; }
  .msg-avatar {
    width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600;
  }
  .msg.user .msg-avatar { background: var(--navy); color: white; }
  .msg.bot .msg-avatar { background: var(--saffron-light); color: var(--saffron); border: 1px solid var(--saffron-mid); }
  .msg-body { max-width: 76%; display: flex; flex-direction: column; gap: 6px; }
  .msg.user .msg-body { align-items: flex-end; }
  .bubble {
    padding: 12px 16px; border-radius: var(--r-lg); font-size: 14px; line-height: 1.65;
    box-shadow: var(--shadow-sm);
  }
  .msg.user .bubble {
    background: var(--navy); color: white; border-bottom-right-radius: 4px;
  }
  .msg.bot .bubble {
    background: white; color: var(--text-primary); border: 1px solid var(--border);
    border-bottom-left-radius: 4px; white-space: pre-wrap;
  }
  .bubble ul, .bubble ol { padding-left: 18px; }
  .bubble li { margin: 3px 0; }
  .bubble strong { color: var(--navy); font-weight: 600; }

  /* Streaming cursor */
  .cursor { display: inline-block; width: 2px; height: 14px; background: var(--saffron); border-radius: 1px; margin-left: 2px; vertical-align: middle; animation: blink 0.8s infinite; }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

  /* Sources */
  .sources { display: flex; flex-wrap: wrap; gap: 6px; }
  .source-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: var(--teal-light); border: 1px solid rgba(15,155,142,0.2);
    color: var(--teal); border-radius: 99px; padding: 3px 10px; font-size: 11px; font-weight: 500;
  }
  .source-badge::before { content: '◎'; font-size: 9px; }

  /* Meta row */
  .meta-row { display: flex; align-items: center; gap: 8px; font-size: 11px; color: var(--text-muted); }
  .meta-pill {
    background: var(--cream); border: 1px solid var(--border);
    border-radius: 99px; padding: 2px 8px;
  }

  /* Thinking indicator */
  .thinking { display: flex; gap: 12px; align-items: flex-start; }
  .thinking-bubble {
    background: white; border: 1px solid var(--border); border-radius: var(--r-lg);
    border-bottom-left-radius: 4px; padding: 14px 16px;
    display: flex; align-items: center; gap: 8px; box-shadow: var(--shadow-sm);
  }
  .dots { display: flex; gap: 5px; }
  .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--saffron); opacity: 0.4; animation: bounce 1.2s infinite; }
  .dot:nth-child(2) { animation-delay: 0.2s; }
  .dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce { 0%,80%,100%{opacity:0.4;transform:translateY(0)} 40%{opacity:1;transform:translateY(-4px)} }

  /* ── Input bar ── */
  .input-bar {
    padding: 16px 24px 18px; border-top: 1px solid var(--border);
    background: white; flex-shrink: 0;
  }
  .input-row { display: flex; gap: 10px; align-items: flex-end; }
  .input-wrap { flex: 1; position: relative; }
  .input-field {
    width: 100%; padding: 12px 44px 12px 16px; border: 1.5px solid var(--border);
    border-radius: var(--r); font-size: 14px; font-family: var(--font-body);
    background: var(--cream); color: var(--text-primary); outline: none;
    resize: none; max-height: 120px; line-height: 1.5; transition: border 0.15s;
  }
  .input-field:focus { border-color: var(--saffron); background: white; }
  .input-field::placeholder { color: var(--text-muted); }
  .send-btn {
    position: absolute; right: 10px; bottom: 10px;
    width: 32px; height: 32px; border-radius: 8px; border: none;
    background: var(--saffron); color: white; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.15s; flex-shrink: 0;
  }
  .send-btn:hover:not(:disabled) { background: #e05520; transform: scale(1.05); }
  .send-btn:disabled { background: var(--border); cursor: not-allowed; }
  .send-btn svg { width: 15px; height: 15px; }
  .input-hint { font-size: 11px; color: var(--text-muted); margin-top: 6px; text-align: center; }
`;

const SUGGESTED = [
  "What is the float option in JoSAA?",
  "Which IITs can I get with rank 2000 General?",
  "How should I fill choices strategically?",
  "What documents are needed for reporting?",
  "Explain CSAB special rounds",
  "OBC-NCL vs General quota cutoff difference?",
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
  const [streaming, setStreaming] = useState(false);
  const [filters, setFilters] = useState({ rank: "", category: "", institute_type: "", quota: "" });
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);
  const abortRef = useRef(null);

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

    const userMsg = { role: "user", content: question };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    const enriched = buildQuestion(question);

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: enriched }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();

      setMessages(prev => [...prev, {
        role: "bot",
        content: data.answer,
        sources: data.sources,
        intent: data.intent,
        latency: data.latency_ms,
        cutoff_rows: data.cutoff_rows_used,
        doc_chunks: data.doc_chunks_used,
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "bot",
        content: `⚠️ Could not connect to the backend. Make sure the FastAPI server is running on port 8000.\n\nError: ${err.message}`,
        sources: [],
        intent: "ERROR",
      }]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, filters]);

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  const reset = async () => {
    try { await fetch(`${API}/reset`, { method: "POST" }); } catch {}
    setMessages([]);
  };

  return (
    <>
      <style>{css}</style>
      <div className="app">
        {/* Header */}
        <header className="header">
          <div className="header-brand">
            <div className="header-logo">J</div>
            <div>
              <div className="header-title">SeatWise</div>
              <div className="header-sub">SeatWise · IIT · NIT · IIIT · GFTI guidance</div>
            </div>
          </div>
          <div className="header-actions">
            <div className="badge-live">Live</div>
            <button className="btn-ghost" onClick={reset}>New chat</button>
          </div>
        </header>

        <div className="layout">
          {/* Sidebar */}
          <aside className="sidebar">
            <div>
              <div className="sidebar-section-label">Quick filters</div>
              <div className="filter-group">
                <div className="filter-label">Your JEE rank</div>
                <input
                  className="filter-input"
                  type="number" placeholder="e.g. 5000"
                  value={filters.rank}
                  onChange={e => setFilters(f => ({ ...f, rank: e.target.value }))}
                />
              </div>
              <div className="filter-group" style={{ marginTop: 10 }}>
                <div className="filter-label">Category</div>
                <select className="filter-select" value={filters.category}
                  onChange={e => setFilters(f => ({ ...f, category: e.target.value }))}>
                  {CATEGORY_OPTIONS.map(o => <option key={o} value={o}>{o || "Select category"}</option>)}
                </select>
              </div>
              <div className="filter-group" style={{ marginTop: 10 }}>
                <div className="filter-label">Institute type</div>
                <select className="filter-select" value={filters.institute_type}
                  onChange={e => setFilters(f => ({ ...f, institute_type: e.target.value }))}>
                  {INST_OPTIONS.map(o => <option key={o} value={o}>{o || "All institutes"}</option>)}
                </select>
              </div>
              <div className="filter-group" style={{ marginTop: 10 }}>
                <div className="filter-label">Quota</div>
                <select className="filter-select" value={filters.quota}
                  onChange={e => setFilters(f => ({ ...f, quota: e.target.value }))}>
                  {QUOTA_OPTIONS.map(o => <option key={o} value={o}>{o || "Any quota"}</option>)}
                </select>
              </div>
              <button className="btn-apply" style={{ marginTop: 12 }}
                onClick={() => filters.rank && send(`Which colleges can I get?`)}>
                Find colleges →
              </button>
            </div>

            <hr className="divider" />

            <div>
              <div className="sidebar-section-label">Try asking</div>
              <div className="sq-list">
                {SUGGESTED.map(q => (
                  <button key={q} className="sq-item" onClick={() => send(q)}>{q}</button>
                ))}
              </div>
            </div>
          </aside>

          {/* Main chat */}
          <main className="main">
            <div className="chat-area">
              {messages.length === 0 ? (
                <div className="welcome">
                  <div className="welcome-icon">J</div>
                  <div className="welcome-title">Your JEE seat counsellor, powered by AI</div>
                  <div className="welcome-sub">
                    Ask anything about seat allotment, cutoffs, float/freeze/slide,
                    category reservations, CSAB rounds, or choice filling strategy.
                  </div>
                  <div className="welcome-chips">
                    {SUGGESTED.slice(0, 4).map(q => (
                      <button key={q} className="chip" onClick={() => send(q)}>{q}</button>
                    ))}
                  </div>
                </div>
              ) : (
                messages.map((msg, i) => (
                  <div key={i} className={`msg ${msg.role}`}>
                    <div className="msg-avatar">
                      {msg.role === "user" ? "U" : "J"}
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
                          {msg.cutoff_rows > 0 && <span className="meta-pill">{msg.cutoff_rows} cutoff rows</span>}
                          {msg.doc_chunks > 0 && <span className="meta-pill">{msg.doc_chunks} doc chunks</span>}
                          {msg.latency && <span>{(msg.latency / 1000).toFixed(1)}s</span>}
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}

              {loading && (
                <div className="thinking">
                  <div className="msg-avatar" style={{
                    width: 32, height: 32, borderRadius: "50%",
                    background: "var(--saffron-light)", color: "var(--saffron)",
                    border: "1px solid var(--saffron-mid)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 13, fontWeight: 600, flexShrink: 0
                  }}>J</div>
                  <div className="thinking-bubble">
                    <div className="dots">
                      <div className="dot" />
                      <div className="dot" />
                      <div className="dot" />
                    </div>
                    <span style={{ fontSize: 13, color: "var(--text-muted)" }}>Searching cutoffs &amp; guidelines…</span>
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
                    placeholder="Ask about JoSAA cutoffs, process, CSAB, strategy…"
                    value={input}
                    onChange={e => { setInput(e.target.value); autoResize(); }}
                    onKeyDown={handleKey}
                    disabled={loading}
                  />
                  <button
                    className="send-btn"
                    onClick={() => send()}
                    disabled={!input.trim() || loading}
                    aria-label="Send message"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z" />
                    </svg>
                  </button>
                </div>
              </div>
              <div className="input-hint">
                Enter to send · Shift+Enter for new line · Filters auto-applied to queries
              </div>
            </div>
          </main>
        </div>
      </div>
    </>
  );
}
