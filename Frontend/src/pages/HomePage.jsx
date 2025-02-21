import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';  // Importe le fichier CSS
import monImage from '../assets/Photos/Momo.png';

function HomePage() {
  return (
    <div className="home-container">
      <img src={monImage} alt="Momo" className="home-image" />
      <h1>Bienvenue sur ENSAI TCG</h1>
      <Link to="/page2">
        <button>Surprise</button>
      </Link>
    </div>
  );
}

export default HomePage;
