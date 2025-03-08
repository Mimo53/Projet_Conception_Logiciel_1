import React, { useState, useEffect } from 'react';  // Ajout des imports de useState et useEffect
import { Link } from 'react-router-dom';
import './accueil.css';  // Importe le fichier CSS
import img_Accueil from '../assets/photos/accueil.jpeg';

function Accueil() {
  const [message, setMessage] = useState('');  // Crée un state pour le message

  useEffect(() => {
    // Effectue la requête GET vers ton backend FastAPI
    fetch('/api/hello')  // Remplace par ton endpoint si nécessaire
      .then((response) => {
        if (!response.ok) {
          throw new Error('Erreur de connexion');
        }
        return response.json();  // On suppose que ton API renvoie un JSON
      })
      .then((data) => setMessage(data.message))  // On met à jour le message avec la réponse de l'API
      .catch((err) => console.error('Erreur de fetch :', err));
  }, []);  // [] garantit que l'appel se fait une seule fois au montage du composant

  return (
    <div className="accueil-container">
      {/* Image d'accueil */}
      <img src={img_Accueil} alt="Accueil" className="accueil-image" />

      {/* Texte d'accueil */}
      <p className="accueil-texte">
        Bienvenue dans ENSAI TCG ! Que souhaitez-vous faire ?
      </p>

      {/* Texte provenant de l'API */}
      <p className="accueil-texte">
        {message || "Chargement du message..."}
      </p>

      {/* Boutons */}
      <div className="button-container">
        <Link to="/page2">
          <button className="credits-button">Crédits</button>
        </Link>

        <Link to="/">
          <button className="bienvenue-button">La magnifique page de bienvenue</button>
        </Link>


        {/* Nouveau bouton "Se connecter" */}
        <Link to="/login">
          <button className="login-button">Se connecter</button>
        </Link>

        {/* Nouveau bouton "S'inscrire" */}
        <Link to="/register">
          <button className="register-button">S'inscrire</button>
        </Link>
      </div>
    </div>
  );
}

export default Accueil;
