import React, { useRef, useState, useEffect } from 'react';
import '../styles/ChatInput.css';

function ChatInput() {
  // Create refs for file input and textarea
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);
  
  // State to manage the input value
  const [inputValue, setInputValue] = useState('');

  // Function to adjust textarea height based on content
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      // Reset height to minimum
      textarea.style.height = 'auto';
      
      // Set a max height to prevent excessive expansion
      const maxHeight = 200; // pixels
      
      // Calculate new height (includes padding)
      const newHeight = Math.min(textarea.scrollHeight, maxHeight);
      
      // Set height
      textarea.style.height = newHeight + 'px';
    }
  };

  // Adjust height whenever input value changes
  useEffect(() => {
    adjustTextareaHeight();
  }, [inputValue]);

  // Function to trigger the file input click
  const handleAttachClick = () => {
    fileInputRef.current.click();
  };

  // Function to handle file selection
  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      console.log('Selected file(s):', files);
      // Additional file processing logic here
    }
  };

  // Function to handle input change
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  // Function to handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    if (inputValue.trim()) {
      console.log('Sending message:', inputValue);
      // Add logic to send the message
      setInputValue(''); // Clear input after sending
      
      // Reset height after clearing
      setTimeout(adjustTextareaHeight, 0);
    }
  };

  // Handle Enter key press to submit, Shift+Enter for new line
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  return (
    <form className="chat-input-container" onSubmit={handleSubmit}>
      <textarea
        ref={textareaRef}
        className="chat-input"
        placeholder="Share your code for a quick fix"
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        rows={1} // Start with 1 row
      />
      <div className="input-actions">
        <button 
          type="button" 
          className="action-btn attachment" 
          onClick={handleAttachClick}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" />
          </svg>
        </button>
        {/* Hidden file input */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }}
          multiple
        />
        <button 
          type="submit" 
          className="send-btn"
          disabled={!inputValue.trim()}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="send-icon">
            <path d="M22 2L11 13"></path>
            <path d="M22 2l-7 20-4-9-9-4 20-7z"></path>
          </svg>
        </button>
      </div>
    </form>
  );
}

export default ChatInput;