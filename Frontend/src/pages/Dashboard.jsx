import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();

  // Fonction de déconnexion
  const handleLogout = () => {
    localStorage.removeItem('token'); // Supprime le token de connexion
    navigate('/login'); // Redirige vers la page de connexion
  };

  return (
    <div className="dashboard-container">
      <h2>Bienvenue sur EnsaiTCG !</h2>
      <p>Vous êtes connecté avec succès.</p>

      {/* Conteneur des boutons */}
      <div className="button-container">
        <button onClick={() => navigate('/Collection')} className="collection-button">
          Collection
        </button>

        <button onClick={() => navigate('/Booster')} className="booster-button">
          Ouvrir un booster
        </button>

        <button onClick={handleLogout} className="logout-button">
          Se déconnecter
        </button>
      </div>

    </div>
  );
}

export default Dashboard;