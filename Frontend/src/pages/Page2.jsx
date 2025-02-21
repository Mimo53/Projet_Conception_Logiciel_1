import React from 'react';
import { Link } from 'react-router-dom';
import './Page2.css';  // Assure-toi d'avoir le fichier CSS pour cette page
import videoFile from '../assets/Andre.mp4';  // Importer la vidéo
import monImage from '../assets/Photos/Dorian.png'; // Importer l'image
import audioFile from '../assets/Son_Andre.ogg';

function Page2() {
  return (
    <div className="page2-container">
      <h1>Les dévellopeur de cette apllication sont : !</h1>
      <p>Le meilleur danceur tik tok, SOCARD Andréééééé </p>
      
      {/* Balise vidéo */}
      <video
        width="60%"
        controls
        autoPlay
        loop
        onError={(e) => console.error("Error loading video:", e)}
        onLoadedData={() => console.log("Video loaded successfully")}
      >
        <source src={videoFile} type="Andre/mp4" />
        Votre navigateur ne supporte pas la balise vidéo.
      </video>

      <p>Et voilà le meilleur pilote de l'ENSAI, BACHET Doriaaaaaaaaan </p>
      <img src={monImage} alt="Description de l'image" width="40%" />
      {/* Bouton pour revenir à la page d'accueil */}
      <Link to="/">
        <button>Retour à l'accueil</button>
      </Link>
      <audio autoPlay loop>
        <source src={audioFile} type="audio/mp3" />
        Votre navigateur ne supporte pas la balise audio.
      </audio>
    </div>
  );
}

export default Page2;
