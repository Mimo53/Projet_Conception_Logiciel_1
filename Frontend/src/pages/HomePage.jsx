import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';  // Importe le fichier CSS

function HomePage() {
  return (
    <div className="home-container">
      <h1>Bienvenue sur ENSAI TCG</h1>
      <Link to="/page2">
        <button>Surprise</button>
      </Link>
    </div>
  );
}

export default HomePage;
