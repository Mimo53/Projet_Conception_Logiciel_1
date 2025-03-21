import React from 'react';
import { Link } from 'react-router-dom';
import './page2.css';
import videoFile from '../assets/andre.mp4';  // Importer la vidéo
import monImage from '../assets/photos/dorian.png'; // Importer l'image
import audioFile from '../assets/son_andre.ogg';

function Page2() {
  return (
    <div className="page2-container">
      <h1>Les développeurs de cette application sont : !</h1>
      <p>Le meilleur danceur tik tok, SOCARD Andréééééé </p>

      {/* Balise vidéo */}
      <video
        width="20%"
        autoPlay
        loop
        onError={(e) => console.error("Error loading video:", e)}
        onLoadedData={() => console.log("Video loaded successfully")}
      >
        <source src={videoFile} type="video/mp4" />
        Votre navigateur ne supporte pas la balise vidéo.
      </video>

      <p>Et voilà le meilleur pilote de l'ENSAI, BACHET Doriaaaaaaaaan </p>
      <img src={monImage} alt="Description de l'image" width="40%" />
      <p>(Et Momo évidemment, voir page de bienvenue)</p>
      {/* Bouton pour revenir à la page d'accueil */}
      <Link to="/Accueil">
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
