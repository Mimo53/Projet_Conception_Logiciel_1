import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "./Booster.css";
import img_booster from "../assets/Photos/booster.png";

function Booster() {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isBoosterOpened, setIsBoosterOpened] = useState(false);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [showAllCards, setShowAllCards] = useState(false);
  const [animationKey, setAnimationKey] = useState(0); // Clé pour forcer le re-rendu

  const token = localStorage.getItem("token");

  const openBooster = async () => {
    setLoading(true);
    setError(null);
    try {
      if (!token) {
        console.error("Token d'authentification manquant !");
        setError("Token d'authentification manquant !");
        return;
      }

      const response = await axios.post(
        "http://localhost:8000/booster/open_booster_and_add/",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          withCredentials: true,
        }
      );
      setCards(response.data.cards);
      setIsBoosterOpened(true); // On ouvre le booster après avoir récupéré les cartes
    } catch (error) {
      console.error("Erreur lors de l'ouverture du booster:", error);
      setError("Erreur lors de l'ouverture du booster. Veuillez réessayer plus tard.");
    }
    setLoading(false);
  };

  const handleImageError = (e, card) => {
    console.error(`Erreur lors du chargement de l'image pour la carte : ${card.name}`);
    e.target.src = "/path/to/default_image.png";
  };

  const showNextCard = () => {
    if (currentCardIndex < cards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1);
      setAnimationKey(prevKey => prevKey + 1); // Mettre à jour la clé pour forcer le re-rendu
    } else {
      setShowAllCards(true); // Si on est sur la dernière carte, on montre toutes les cartes
    }
  };

  return (
    <div className="Booster-container">
      {/* Si le booster n'est pas ouvert, on affiche l'image comme bouton */}
      {!isBoosterOpened && (
        <>
          <img
            src={img_booster}
            alt="Booster"
            className="booster-button"
            onClick={openBooster}
          />
          <Link to="/dashboard">
            <button className="home-button">Retour à l'accueil</button>
          </Link>
        </>
      )}

      {/* Si le booster est ouvert et qu'il y a des cartes, on affiche les cartes une par une */}
      {isBoosterOpened && !showAllCards && cards.length > 0 && (
        <div
          key={animationKey} // Utiliser la clé pour forcer le re-rendu
          className={`card-display ${cards[currentCardIndex].rarity.toLowerCase().replace(' ', '_')}`}
          onClick={showNextCard}
        >
          <img
            src={`http://localhost:8000/proxy/proxy-image/?url=${encodeURIComponent(cards[currentCardIndex].image_url)}`}
            alt={cards[currentCardIndex].name}
            onError={(e) => handleImageError(e, cards[currentCardIndex])}
          />
          <p>{cards[currentCardIndex].rarity}</p>
        </div>
      )}

      {/* Si l'utilisateur a cliqué sur la dernière carte, on affiche toutes les cartes */}
      {showAllCards && cards.length > 0 && (
        <div className="cards-grid">
          {cards.map((card, index) => (
            <div key={index} className={`card ${card.rarity.toLowerCase().replace(' ', '_')}`}>
              <img
                src={`http://localhost:8000/proxy/proxy-image/?url=${encodeURIComponent(card.image_url)}`}
                alt={card.name}
                onError={(e) => handleImageError(e, card)}
              />
              <p>{card.name} - {card.rarity}</p>
            </div>
          ))}
        </div>
      )}

      {/* Affichage de l'erreur */}
      {error && <div className="error-message">{error}</div>}

      {/* Affichage du bouton de retour au dashboard quand toutes les cartes sont affichées */}
      {showAllCards && (
        <Link to="/dashboard">
          <button className="home-button">Retour à l'accueil</button>
        </Link>
      )}
    </div>
  );
}

export default Booster;
