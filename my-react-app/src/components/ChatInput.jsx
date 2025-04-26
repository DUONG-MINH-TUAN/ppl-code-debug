import React, { useRef } from 'react';
import '../styles/ChatInput.css';

function ChatInput() {
  // Create a ref to reference the hidden file input
  const fileInputRef = useRef(null);

  // Function to trigger the file input click when the attach button is clicked
  const handleAttachClick = () => {
    fileInputRef.current.click();
  };

  // Function to handle file selection
  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      console.log('Selected file(s):', files);
      // You can add further logic here, e.g., upload the file or process it
    }
  };

  return (
    <div className="chat-input-container">
      <input 
        type="text" 
        className="chat-input" 
        placeholder="Share your code for a quick fix" 
      />
      <div className="input-actions">
        <button className="action-btn attachment" onClick={handleAttachClick}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" />
          </svg>
        </button>
        {/* Hidden file input, triggered by the attach button */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }} // Hide the default file input
          multiple // Optional: Allow multiple file selection
        />
        <button className="send-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="19" x2="12" y2="5"></line>
            <polyline points="5 12 12 5 19 12"></polyline>
          </svg>
        </button>
      </div>
    </div>
  );
}

export default ChatInput;