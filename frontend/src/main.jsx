import { StrictMode, useState } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import Predictor from './Predictor.jsx'

const NAV_CSS = `
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Space Grotesk', system-ui, sans-serif; background: #080d1a; }

  .sw-shell { display: flex; flex-direction: column; min-height: 100vh; }

  .sw-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 32px; height: 60px;
    background: rgba(8, 13, 26, 0.95);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: sticky; top: 0; z-index: 200;
    backdrop-filter: blur(20px);
  }

  .sw-nav-brand {
    display: flex; align-items: center; gap: 10px; text-decoration: none;
  }
  .sw-nav-logo-img {
    height: 34px; width: auto; object-fit: contain;
  }

  .sw-nav-tabs { display: flex; gap: 4px; background: rgba(255,255,255,0.05); border-radius: 10px; padding: 4px; }

  .sw-nav-tab {
    padding: 7px 20px; border-radius: 7px; font-size: 13px; font-weight: 600;
    cursor: pointer; transition: all 0.18s; border: none; font-family: 'Space Grotesk', sans-serif;
    color: rgba(255,255,255,0.45); background: transparent; letter-spacing: 0.01em;
  }
  .sw-nav-tab.active {
    background: linear-gradient(135deg, #1E4DFF, #0f9b8e);
    color: white;
    box-shadow: 0 2px 12px rgba(30,77,255,0.4);
  }
  .sw-nav-tab:hover:not(.active) { color: rgba(255,255,255,0.8); background: rgba(255,255,255,0.08); }

  .sw-nav-tab-icon { margin-right: 6px; }

  .sw-page { flex: 1; }
`

// Inline logo using the uploaded logo image (base64 or url)
// We'll use the actual file path for local dev
const LOGO_URL = "/Logo_SeatWise.png";

function Root() {
  const [tab, setTab] = useState('chat')

  return (
    <div className="sw-shell">
      <style>{NAV_CSS}</style>
      <nav className="sw-nav">
        <a className="sw-nav-brand" onClick={() => setTab('chat')} style={{ cursor: 'pointer' }}>
          <img className="sw-nav-logo-img" src={LOGO_URL} alt="SeatWise" 
               onError={e => { e.target.style.display='none'; }} />
        </a>
        <div className="sw-nav-tabs">
          <button
            className={`sw-nav-tab ${tab === 'chat' ? 'active' : ''}`}
            onClick={() => setTab('chat')}
          >
            <span className="sw-nav-tab-icon">💬</span>AI Counsellor
          </button>
          <button
            className={`sw-nav-tab ${tab === 'predictor' ? 'active' : ''}`}
            onClick={() => setTab('predictor')}
          >
            <span className="sw-nav-tab-icon">🎯</span>College Predictor
          </button>
        </div>
      </nav>
      <div className="sw-page">
        {tab === 'chat' ? <App /> : <Predictor />}
      </div>
    </div>
  )
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Root />
  </StrictMode>
)
