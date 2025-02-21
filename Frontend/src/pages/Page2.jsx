import React from 'react';
import { Link } from 'react-router-dom';
import './Page2.css';  // Assure-toi d'avoir le fichier CSS pour cette page
import videoFile from '../assets/video.mp4';  // Importer la vidéo

function Page2() {
  return (
    <div className="page2-container">
      <h1>Bienvenue sur la page 2 !</h1>
      <p>Voici une vidéo que nous avons ajoutée à cette page.</p>
      
      {/* Balise vidéo */}
      <video width="80%" controls>
        <source src={videoFile} type="video/mp4" />
        Votre navigateur ne supporte pas la balise vidéo.
      </video>

      {/* Bouton pour revenir à la page d'accueil */}
      <Link to="/">
        <button>Retour à l'accueil</button>
      </Link>
    </div>
  );
}

export default Page2;
