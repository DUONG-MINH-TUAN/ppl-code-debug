import React, { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import '../styles/ChatContainer.css';

function ChatContainer({ onFirstMessage }) {
  // State to store all chat messages
  const [messages, setMessages] = React.useState([
    // Default welcome message is now optional
    // We'll add it when the first message is sent
  ]);
  
  // Ref for auto-scrolling
  const messagesEndRef = useRef(null);
  
  // Auto scroll to bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  // Function to handle sending new messages
  const handleSendMessage = (message) => {
    // If this is the first message, call onFirstMessage callback
    if (messages.length === 0) {
      // Add welcome message first
      setMessages([{ text: "Hi there! How can I help you today?", isUser: false }]);
      
      // Notify parent component that chat has started
      if (onFirstMessage) {
        onFirstMessage();
      }
    }
    
    // Add user message to chat
    setMessages(prevMessages => [...prevMessages, { text: message, isUser: true }]);
    
    // Simulate AI response (you can replace this with actual API calls later)
    setTimeout(() => {
      const responses = [
        "That's interesting! Tell me more.",
        "I understand. How can I assist further?",
        "Good question! Let me think about that.",
        "I see what you mean. Here's what I think...",
        "Thanks for sharing that information!"
      ];
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      setMessages(prevMessages => [...prevMessages, { text: randomResponse, isUser: false }]);
    }, 1000);
  };
  
  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <ChatMessage 
            key={index} 
            message={message.text} 
            isUser={message.isUser} 
          />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-wrapper">
        <ChatInput onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
}

export default ChatContainer;