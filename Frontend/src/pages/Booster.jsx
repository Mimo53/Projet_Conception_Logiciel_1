import React from 'react';
import { Link } from 'react-router-dom';
import './Booster.css';  
import img_booster from '../assets/Photos/Booster_rd.jpeg';

function Booster() {
  return (
    <div className="Booster-container">
      <img src={img_booster} alt="Jsp" width="19%" />
      <h1>Il est l'heure d'ouvrir un booster !</h1>
      <h1>C'est faux on peut pas encore</h1>
      {/* Bouton pour revenir à la page d'Accueil */}
      <Link to="/Accueil">
        <button>Retour à l'accueil</button>
      </Link>
    </div>
  );
}

export default Booster;