import React from 'react';
import { Link } from 'react-router-dom';
import './Accueil.css';  // Importe le fichier CSS
import img_Accueil from '../assets/Photos/Accueil.jpeg';

function Accueil() {
  return (
    <div className="accueil-container">
      {/* Image d'accueil */}
      <img src={img_Accueil} alt="Accueil" className="accueil-image" />

      {/* Texte sous l'image */}
      <p className="accueil-texte">Bienvenue dans ENSAI TCG ! Que souhaitez-vous faire ?</p>

      {/* Boutons */}
      <div className="button-container">
        <Link to="/page2">
          <button className="credits-button">Crédits</button>
        </Link>

        <Link to="/">
          <button className="bienvenue-button">La magnifique page de bienvenue</button>
        </Link>

        <Link to="/Booster">
          <button>Ouvrir booster</button>
        </Link>

        <Link to="/Collection">
          <button>Collection</button>
        </Link>
      </div>
    </div>
  );
}

export default Accueil;