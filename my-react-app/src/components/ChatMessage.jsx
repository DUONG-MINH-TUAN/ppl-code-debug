import React from 'react';
import '../styles/ChatMessage.css';
// Import your avatar images
import userAvatar from '../assets/Dune.jpg';
import assistantAvatar from '../assets/robot.png';

function ChatMessage({ message, isUser }) {
  return (
    <div className={`chat-message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-avatar">
        <img 
          src={isUser ? userAvatar : assistantAvatar} 
          alt={isUser ? 'User' : 'Assistant'}   
          className={isUser ? 'user-avatar' : 'assistant-avatar'} 
        />
      </div>
      <div className="message-content">
        <div className="message-text">{message}</div>
      </div>
    </div>
  );
}

export default ChatMessage;