// src/pages/Dashboard.jsx
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
      <h2>Bienvenue sur votre tableau de bord !</h2>
      <p>Vous êtes connecté avec succès.</p>
      <button onClick={handleLogout} className="logout-button">
        Se déconnecter
      </button>
    </div>
  );
}

export default Dashboard;
