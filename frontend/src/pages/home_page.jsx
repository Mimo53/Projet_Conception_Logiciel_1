import React from 'react';
import { Link } from 'react-router-dom';
import './home_page.css';  // Importe le fichier CSS
import monImage from '../assets/photos/momo.png';

function HomePage() {
  return (
    <div className="home-container">
      <img src={monImage} alt="Momo" className="home-image" />
      <h1>Bienvenue sur ENSAI TCG</h1>
      <Link to="/Accueil">
        <button>Commencer</button>
      </Link>
    </div>
  );
}

export default HomePage;
