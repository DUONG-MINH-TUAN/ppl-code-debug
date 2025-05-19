import React, { useState, useEffect } from 'react';
import '../styles/Navbar.css';
import myLogo from '../assets/debug.png'; 
import Avatar from '../assets/Dune.jpg';

function Navbar({ onDarkModeToggle, isDarkMode }) {
  const [isAvatarMenuOpen, setIsAvatarMenuOpen] = useState(false);
  
  // Apply dark mode class to body element
  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [isDarkMode]);
  
  const toggleAvatarMenu = () => {
    setIsAvatarMenuOpen(!isAvatarMenuOpen);
  };

  return (
    <nav className={`navbar ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="navbar-container">
        <div className="logo">
          <img src={myLogo} alt="Custom Logo" className="logo-icon" />
          <span className="logo-text">HookScope</span>
        </div>
        
        <div className="nav-actions">
          <button className="action-button notification-btn">
            <span className="icon">📬</span>
            <span className="notification-badge">1</span>
          </button>
          
          <button className="action-button dark-mode-toggle" onClick={onDarkModeToggle}>
            <span className="icon">{isDarkMode ? '💡' : '🌚'}</span>
          </button>
          
          <div className="user-avatar-container">
            <div className="user-avatar" onClick={toggleAvatarMenu}>
              <img src={Avatar} alt="User avatar" />
            </div>
            
            {isAvatarMenuOpen && (
              <div className="avatar-dropdown">
                <div className="dropdown-item">
                  <span className="dropdown-icon">🧑‍💼</span>
                  <span>Account</span>
                </div>
                <div className="dropdown-item">
                  <span className="dropdown-icon">⚙️</span>
                  <span>Settings</span>
                </div>
                <div className="dropdown-divider"></div>
                <div className="dropdown-item logout">
                  <span className="dropdown-icon">🚪</span>
                  <span>Log out</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;