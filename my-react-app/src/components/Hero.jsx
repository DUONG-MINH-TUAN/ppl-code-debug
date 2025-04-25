import React from 'react';
import '../styles/Hero.css';
import heroImage from '../assets/robot.png'; // Replace with your actual image file name

function Hero() {
  const currentHour = new Date().getHours();

  let greetingMessage;
  if (currentHour >= 4 && currentHour < 12) {
    greetingMessage = "Coffee in hand, code in mind — good morning, coding buddy!";
  } else if (currentHour >= 12 && currentHour < 20) {
    greetingMessage = "Half the day’s done, let’s smash some code!";
  } else {
    greetingMessage = "Winding down or still coding, buddy? Good evening!";
  }

  return (
    <div className="hero">
      <img src={heroImage} alt="Hero" className="robot" />
      <h1>{greetingMessage}</h1>
      <p>Need help debugging your JavaScript code today?</p>
    </div>
  );
}

export default Hero;