import React, { useState, useEffect } from 'react';
import '../styles/Hero.css';
import heroImage from '../assets/robot.png';

function Hero() {
  const [animated, setAnimated] = useState(false);
  const [hovering, setHovering] = useState(false);
  
  const currentHour = new Date().getHours();
  
  let greetingMessage;
  if (currentHour >= 4 && currentHour < 12) {
    greetingMessage = "Good morning, coding buddy!";
  } else if (currentHour >= 12 && currentHour < 20) {
    greetingMessage = "Half the day's done, let's smash some code!";
  } else {
    greetingMessage = "Winding down or still coding, buddy?";
  }

  useEffect(() => {
    setAnimated(true);
    
    const blinkInterval = setInterval(() => {
      const robotEyes = document.querySelector('.robot-eyes');
      if (robotEyes) {
        robotEyes.classList.add('blink');
        setTimeout(() => {
          robotEyes.classList.remove('blink');
        }, 200);
      }
    }, Math.random() * 3000 + 2000);
    
    return () => clearInterval(blinkInterval);
  }, []);

  return (
    <div className="hero">
      <div 
        className={`robot-container ${animated ? 'animated' : ''} ${hovering ? 'hovering' : ''}`}
        onMouseEnter={() => setHovering(true)}
        onMouseLeave={() => setHovering(false)}
      >
        <div className="robot-background">
          <div className="circuit-line line1"></div>
          <div className="circuit-line line2"></div>
          <div className="circuit-line line3"></div>
          <div className="circuit-dot dot1"></div>
          <div className="circuit-dot dot2"></div>
          <div className="circuit-dot dot3"></div>
        </div>
        
        <div className="robot-glow"></div>
        
        <div className="robot-wrapper">
          <img 
            src={heroImage} 
            alt="Robot Assistant" 
            className="robot" 
          />
          <div className="robot-eyes"></div>
          <div className="robot-antenna"></div>
        </div>
        
        <div className="particles">
          <div className="particle p1"></div>
          <div className="particle p2"></div>
          <div className="particle p3"></div>
          <div className="particle p4"></div>
          <div className="particle p5"></div>
          <div className="particle p6"></div>
        </div>
        
      </div>
      <h1 className={animated ? 'fade-in' : ''}>{greetingMessage}</h1>
      <p className={animated ? 'fade-in-delay' : ''}>Need help debugging your JavaScript code today?</p>
    </div>
  );
}

export default Hero;