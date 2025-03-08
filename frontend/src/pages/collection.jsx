import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './collection.css';

function Collection() {
  const [collection, setCollection] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchCollection = async () => {
      try {
        const response = await axios.get("http://localhost:8000/booster/view_collections", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          withCredentials: true,
        });
        const uniqueCards = Array.from(new Set(response.data.collection.map(card => card.card_name)))
          .map(name => response.data.collection.find(card => card.card_name === name));
        setCollection(uniqueCards);
      } catch (error) {
        console.error("Erreur lors de la récupération de la collection:", error);
        setError("Erreur lors de la récupération de la collection. Veuillez réessayer plus tard.");
      } finally {
        setLoading(false);
      }
    };

    fetchCollection();
  }, [token]);

  const handleImageError = (e, card) => {
    console.error(`Erreur lors du chargement de l'image pour la carte : ${card.card_name}`);
    e.target.src = "/path/to/default_image.png";
  };

  if (loading) {
    return <div className="Collection-container">Chargement en cours...</div>;
  }

  if (error) {
    return <div className="Collection-container">{error}</div>;
  }

  return (
    <div className="Collection-container">
      {collection.length > 0 ? (
        <div className="cards-grid">
          {collection.map((card, index) => (
            <div key={index} className={`card ${card.rarity.toLowerCase().replace(' ', '_')}`}>
              <img
                src={`http://localhost:8000/proxy/proxy-image/?url=${encodeURIComponent(card.image_url)}`}
                alt={card.card_name}
                loading="lazy"
                onError={(e) => handleImageError(e, card)}
              />
              <p className={`rarity-text ${card.rarity.toLowerCase().replace(' ', '_')}`}>
                {card.rarity}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <h1>Ta collection est vide</h1>
      )}
      <Link to="/dashboard">
        <button className="home-button">Retour à l'accueil</button>
      </Link>
    </div>
  );
}

export default Collection;
