import React from 'react';
import '../styles/Navbar.css';
import myLogo from '../assets/debug.png'; 
import Avatar from '../assets/Dune.jpg'; // Imported image for avatar

function Navbar({ onDarkModeToggle, isDarkMode }) {
  return (
    <nav className="navbar">
      <div className="logo">
        <img src={myLogo} alt="Custom Logo" className="logo-icon" />
        <span className="logo-text">CodeDebug</span>
      </div>
      <div className="nav-actions">
        <button className="action-icon">
          <span>📬  </span>
        </button>
        <button className="dark-mode-toggle" onClick={onDarkModeToggle}>
          <span>{isDarkMode ? '🌅' : '🌚'}</span>
        </button>
        <div className="user-avatar">
          <img src={Avatar} alt="User avatar" /> {/* Updated src to use imported Avatar */}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;