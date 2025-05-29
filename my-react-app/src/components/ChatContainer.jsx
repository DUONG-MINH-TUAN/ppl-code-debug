
import React, { useRef, useEffect, useState } from 'react';
import axios from 'axios';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import '../styles/ChatContainer.css';

function ChatContainer({ onFirstMessage }) {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle sending new messages
  const handleSendMessage = async (message, grammarCallback) => {
    // If this is the first message, add welcome message and notify parent
    if (messages.length === 0) {
      setMessages([{ text: "Hi there! How can I help you today?", isUser: false }]);
      if (onFirstMessage) {
        onFirstMessage();
      }
    }

    // Add user message to chat
    setMessages(prevMessages => [...prevMessages, { text: message, isUser: true }]);

    // Call grammar check API only
    try {
      const grammarResponse = await axios.post("http://localhost:3000/check-grammar", {
        input: message,
      });

      let grammarMessage = '';
      let isError = false;

      if (!grammarResponse.data.success) {
        grammarMessage = grammarResponse.data.error;
        isError = true;
      } else if (!grammarResponse.data.result.success) {
        grammarMessage = grammarResponse.data.result.errors.join(', ');
        isError = true;
      } else {
        grammarMessage = grammarResponse.data.result.message;
        isError = false;
      }

      // Add only grammar check result to chat
      setMessages(prevMessages => [...prevMessages, { 
        text: grammarMessage, 
        isUser: false,
        isError: isError 
      }]);

    } catch (grammarError) {
      console.error('Error calling grammar check API:', grammarError.message);
      const errorMessage = 'Server error: ' + grammarError.message;
      setMessages(prevMessages => [
        ...prevMessages,
        { text: errorMessage, isUser: false, isError: true },
      ]);
    }
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
            isError={message.isError}
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