import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ChatInput from './components/ChatInput';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
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
        <Hero />
        <ChatInput />
      </main>
    </div>
  );
}

export default App;