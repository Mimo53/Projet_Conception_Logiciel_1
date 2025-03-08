import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './add_card_page.css';

function AddCardPage() {
  const [name, setName] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [rarity, setRarity] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); // Pour la navigation

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/cartes_ajout',
        {
          name,
          image_url: imageUrl,
          rarity
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setMessage(response.data.message);
      setName('');
      setImageUrl('');
      setRarity('');
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la carte :', error);
      setMessage('Erreur lors de l\'ajout de la carte.');
    }
  };

  return (
    <div className="add-card-container">
      <h2>Ajouter une carte à la collection</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nom de la carte"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="URL de l'image"
          value={imageUrl}
          onChange={(e) => setImageUrl(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Rareté (ex: Commun, Rare, Légendaire)"
          value={rarity}
          onChange={(e) => setRarity(e.target.value)}
          required
        />
        <button type="submit" className="add-card-button">Ajouter la carte</button>
      </form>
      {message && <p>{message}</p>}

      {/* Bouton pour revenir au dashboard */}
      <button onClick={() => navigate('/dashboard')} className="back-to-dashboard-button">
        Retour au Dashboard
      </button>
    </div>
  );
}

export default AddCardPage;
