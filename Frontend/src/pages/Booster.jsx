import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "./Booster.css";
import img_booster from "../assets/Photos/booster.png";

function Booster() {
  const [collections, setCollections] = useState([]);
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState(null); // État pour gérer l'ID utilisateur

  useEffect(() => {
    const storedUserId = localStorage.getItem("user_id"); // Récupère le username
    if (storedUserId) {
      setUserId(storedUserId);  // Sauvegarde le username dans l'état
      console.log("Username bien reçu", storedUserId);
    } else {
      console.error("user_id non défini dans localStorage");
    }
  }, []); // Se lance une seule fois au montage du composant

  const openBooster = async () => {
    setLoading(true);
    try {
      // Utilisation de l'état userId (username) plutôt que de refaire appel à localStorage
      if (!userId) {
        console.error("user_id non défini !");
        return;
      }
  
      const response = await axios.post("http://localhost:8000/open_booster_and_add/", {
        user_id: userId,  // Assure-toi que cette clé correspond à ce que l'API attend
      });
  
      console.log(response.data);  // Vérifie la réponse complète du serveur
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
