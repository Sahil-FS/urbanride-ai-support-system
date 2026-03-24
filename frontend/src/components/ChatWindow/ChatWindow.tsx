import { useEffect, useRef } from 'react';
import type { Message } from '../../types';
import { MessageBubble } from '../MessageBubble/MessageBubble';
import './ChatWindow.css';

interface TypingIndicatorProps {}

function TypingIndicator(_props: TypingIndicatorProps) {
  return (
    <div className="bubble-row bubble-row--bot">
      <div className="bubble-avatar bubble-avatar--bot">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7H3a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z"/>
          <path d="M9 14a1 1 0 0 1-2 0v-1a1 1 0 0 1 2 0v1z"/>
          <path d="M17 14a1 1 0 0 1-2 0v-1a1 1 0 0 1 2 0v1z"/>
          <path d="M3 21h18"/><path d="M5 18v3M19 18v3"/>
        </svg>
      </div>
      <div className="bubble-content">
        <span className="bubble-sender">Urban Taxi Support</span>
        <div className="bubble bubble--bot typing-bubble">
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
        </div>
      </div>
    </div>
  );
}

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
  showQuickReplies?: boolean;
  onQuickReply?: (text: string) => void;
  onSubOptionClick: (text: string) => void;
  onCallClick: () => void;
  onResolved?: () => void;
}

export function ChatWindow({
  messages,
  isLoading,
  onSubOptionClick,
  onCallClick,
}: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="chat-window">
      {/* Date pill */}
      <div className="chat-window__date-pill">
        <span>Today</span>
      </div>

      {/* Messages */}
      {messages.map((msg) => (
        <MessageBubble
          key={msg.id}
          message={msg}
          onSubOptionClick={onSubOptionClick}
          onCallClick={onCallClick}
        />
      ))}

      {/* Typing indicator */}
      {isLoading && <TypingIndicator />}

      <div ref={bottomRef} />
    </div>
  );
}
