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
  const [animationKey, setAnimationKey] = useState(0);

  const token = localStorage.getItem("token");

  const openBooster = async () => {
    if (!token) {
      console.error("Token d'authentification manquant !");
      setError("Token d'authentification manquant !");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        "http://localhost:8000/booster/open_booster_and_add/",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          withCredentials: true,
        }
      );

      if (response.status === 200) {
        setCards(response.data.cards);
        setIsBoosterOpened(true);
      } else {
        setError("Erreur inattendue du serveur.");
      }
    } catch (error) {
      setError("Erreur lors de l'ouverture du booster. Vérifie ton token.");
    }

    setLoading(false);
  };

  const handleImageError = (e, card) => {
    e.target.src = "/path/to/default_image.png";
  };

  const showNextCard = () => {
    if (currentCardIndex < cards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1);
      setAnimationKey((prevKey) => prevKey + 1);
    } else {
      setShowAllCards(true);
    }
  };

  return (
    <div className="Booster-container">
      {!isBoosterOpened && (
        <div className="booster-container">
          <p className="booster-message">Clique sur le booster pour l'ouvrir !</p>
          <img
            src={img_booster}
            alt="Booster"
            className="booster-button"
            onClick={openBooster}
            style={{ width: "250px", height: "auto" }}
          />
          <Link to="/dashboard">
            <button className="home-button">Retour à l'accueil</button>
          </Link>
        </div>
      )}


      {isBoosterOpened && !showAllCards && cards.length > 0 && (
        <div
          key={animationKey}
          className={`card-display single-card ${cards[currentCardIndex].rarity.toLowerCase().replace(" ", "_")}`}
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

      {showAllCards && cards.length > 0 && (
        <div className="cards-grid">
          {cards.map((card, index) => (
            <div
              key={index}
              className={`card-display multiple-cards ${card.rarity.toLowerCase().replace(" ", "_")}`}
            >
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

      {error && <div className="error-message">{error}</div>}

      {showAllCards && (
        <Link to="/dashboard">
          <button className="home-button">Retour à l'accueil</button>
        </Link>
      )}
    </div>
  );
}

export default Booster;
