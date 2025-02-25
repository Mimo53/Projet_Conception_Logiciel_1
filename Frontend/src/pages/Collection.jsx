import React from 'react';
import { Link } from 'react-router-dom';
import './Collection.css';  
import img_collection from '../assets/Photos/Collection.jpeg';

function Collection() {
  return (
    <div className="Collection-container">
      <img src={img_collection} alt="Cursed" width="30%" />
      <h1>Ta collection vide mwahaha</h1>
      {/* Bouton pour revenir à la page d'Accueil */}
      <Link to="/dashboard">
        <button>Retour à l'accueil</button>
      </Link>
    </div>
  );
}

export default Collection;