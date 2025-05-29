import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ChatContainer from './components/ChatContainer';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  // New state to track if chat is active
  const [isChatActive, setIsChatActive] = useState(false);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  // Function to activate chat and hide hero
  const activateChat = () => {
    setIsChatActive(true);
  };

  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [isDarkMode]);

  return (
    <div className="app-container">
      <Navbar 
        onDarkModeToggle={toggleDarkMode} 
        isDarkMode={isDarkMode} 
      />
      <main className="main-content">
        {/* Show Hero only when chat is not active */}
        {!isChatActive && <Hero />}
        
        {/* Always render ChatContainer but with conditional styling */}
        <div className={`chat-section ${isChatActive ? 'active' : ''}`}>
          <ChatContainer onFirstMessage={activateChat} />
        </div>
      </main>
    </div>
  );
}

export default App;