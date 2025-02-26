import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "./Booster.css";
import img_booster from "../assets/Photos/booster.png";

function Booster() {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("token"); // Récupère le token JWT stocké

  const openBooster = async () => {
    setLoading(true);
    try {
      if (!token) {
        console.error("Token d'authentification manquant !");
        return;
      }

      const response = await axios.post(
        "http://localhost:8000/open_booster_and_add/",
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

      {cards.length > 0 && (
        <div className="cards-container">
          <h2>Cartes obtenues :</h2>
          <div className="cards-grid">
            {cards.map((card, index) => (
              <div key={index} className="card">
                console.log(card.image_url);
                <img src={card.image_url} alt={card.name} />
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
