import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "./Booster.css";
import img_booster from "../assets/Photos/booster.png";

function Booster() {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null); // Ajout de l'état pour gérer les erreurs

  const token = localStorage.getItem("token"); // Récupère le token JWT stocké

  const openBooster = async () => {
    setLoading(true);
    setError(null); // Réinitialise l'erreur à chaque nouvelle tentative d'ouverture
    try {
      if (!token) {
        console.error("Token d'authentification manquant !");
        setError("Token d'authentification manquant !");
        return;
      }

      const response = await axios.post(
        "http://localhost:8000/open_booster_and_add/", // Assurez-vous que cette route existe dans votre backend
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          withCredentials: true,
        }
      );
      setCards(response.data.cards);
    } catch (error) {
      console.error("Erreur lors de l'ouverture du booster:", error);
      console.error("Réponse du serveur:", error.response ? error.response.data : "Pas de réponse");
      setError("Erreur lors de l'ouverture du booster. Veuillez réessayer plus tard.");
    }
    setLoading(false);
  };

  return (
    <div className="Booster-container">
      <img src={img_booster} alt="Booster" width="19%" />
      <h1>Ouvrir un booster</h1>
      <button onClick={openBooster} disabled={loading}>
        {loading ? "Ouverture..." : "Ouvrir un booster"}
      </button>

      {/* Affichage de l'erreur */}
      {error && <div className="error-message">{error}</div>}

      {cards.length > 0 && (
        <div className="cards-container">
          <h2>Cartes obtenues :</h2>
          <div className="cards-grid">
            {cards.map((card, index) => (
              <div key={index} className="card">
                {/* Modifie l'URL de l'image pour passer par le proxy */}
                <img 
                  src={`http://localhost:8000/proxy-image/?url=${encodeURIComponent(card.image_url)}`} 
                  alt={card.name}
                  onError={(e) => {
                    console.error(`Erreur lors du chargement de l'image: ${card.image_url}`);
                    e.target.src = "/path/to/default_image.png";  // Afficher une image par défaut en cas d'erreur
                  }} 
                />
                <p>{card.name} - {card.rarity}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <Link to="/dashboard">
        <button>Retour à l'accueil</button>
      </Link>
    </div>
  );
}

export default Booster;
