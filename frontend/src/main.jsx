import { StrictMode, useState } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import Predictor from './Predictor.jsx'

const NAV_CSS = `
  .sw-nav {
    display:flex; align-items:center; justify-content:space-between;
    padding:10px 24px; background:#1a2744; border-bottom:2px solid #FF6B35;
    position:sticky; top:0; z-index:100;
  }
  .sw-nav-brand { display:flex; align-items:center; gap:10px; }
  .sw-nav-logo {
    width:32px; height:32px; border-radius:50%; background:#FF6B35;
    display:flex; align-items:center; justify-content:center;
    font-family:'Playfair Display',serif; color:white; font-size:14px; font-weight:700;
  }
  .sw-nav-title { color:white; font-weight:700; font-size:1rem; font-family:'Playfair Display',Georgia,serif; }
  .sw-nav-tabs { display:flex; gap:4px; }
  .sw-nav-tab {
    padding:7px 18px; border-radius:8px; font-size:13px; font-weight:600;
    cursor:pointer; transition:all 0.15s; border:none; font-family:'DM Sans',sans-serif;
    color:rgba(255,255,255,0.6); background:transparent;
  }
  .sw-nav-tab.active { background:#FF6B35; color:white; }
  .sw-nav-tab:hover:not(.active) { background:rgba(255,255,255,0.1); color:white; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { font-family:'DM Sans',system-ui,sans-serif; }
`

function Root() {
  const [tab, setTab] = useState('chat')

  return (
    <>
      <style>{NAV_CSS}</style>
      <nav className="sw-nav">
        <div className="sw-nav-brand">
          <div className="sw-nav-logo">S</div>
          <span className="sw-nav-title">SeatWise</span>
        </div>
        <div className="sw-nav-tabs">
          <button className={`sw-nav-tab ${tab === 'predictor' ? 'active' : ''}`}
            onClick={() => setTab('predictor')}>
            🎯 College Predictor
          </button>
          <button className={`sw-nav-tab ${tab === 'chat' ? 'active' : ''}`}
            onClick={() => setTab('chat')}>
            💬 AI Counsellor
          </button>
        </div>
      </nav>
      {tab === 'chat' ? <App /> : <Predictor />}
    </>
  )
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Root />
  </StrictMode>
)
