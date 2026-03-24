import './ChatHeader.css';

export function ChatHeader() {
  return (
    <header className="chat-header">
      <div className="chat-header__left">
        <div className="chat-header__bot-avatar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7H3a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z"/>
            <path d="M9 14a1 1 0 0 1-2 0v-1a1 1 0 0 1 2 0v1z"/>
            <path d="M17 14a1 1 0 0 1-2 0v-1a1 1 0 0 1 2 0v1z"/>
            <path d="M3 21h18"/>
            <path d="M5 18v3M19 18v3"/>
          </svg>
        </div>
        <div className="chat-header__bot-info">
          <div className="chat-header__bot-name-row">
            <h1 className="chat-header__title">Urban Taxi Support</h1>
            <span className="chat-header__online-dot" title="Online" />
          </div>
          <p className="chat-header__subtitle">Typically replies instantly</p>
        </div>
      </div>

      <div className="chat-header__center">
        <span className="chat-header__label">AI SUPPORT CHAT</span>
      </div>

      <div className="chat-header__right">
        <span className="chat-header__badge">
          <span className="chat-header__badge-dot" />
          AI-POWERED
        </span>
        <button className="chat-header__action" aria-label="Search chat">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="18" height="18">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </button>
        <button className="chat-header__action" aria-label="More options">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="18" height="18">
            <circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>
          </svg>
        </button>
      </div>
    </header>
  );
}
