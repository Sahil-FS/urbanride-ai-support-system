import type { Message } from '../types';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: Message;
}

function fmtTime(d: Date) {
  return d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true });
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  return (
    <div className={`msg-row ${isUser ? 'msg-row--user' : 'msg-row--bot'}`}>
      {/* Bot avatar */}
      {!isUser && (
        <div className="msg-avatar msg-avatar--bot">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="1" y="3" width="15" height="13" rx="2"/>
            <path d="M16 8h4l3 5v3h-7V8z"/>
            <circle cx="5.5" cy="18.5" r="2.5"/>
            <circle cx="18.5" cy="18.5" r="2.5"/>
          </svg>
        </div>
      )}

      {/* Content */}
      <div className="msg-content">
        {!isUser && <span className="msg-sender">Urban Taxi Support</span>}
        <div className={`msg-bubble ${isUser ? 'msg-bubble--user' : 'msg-bubble--bot'}`}>
          <p className="msg-text">{message.text}</p>
        </div>
        <span className="msg-time">{fmtTime(message.timestamp)}</span>
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="msg-avatar msg-avatar--user">AK</div>
      )}
    </div>
  );
}
