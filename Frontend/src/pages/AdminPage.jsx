import React from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminPage.css';

function AdminPage() {
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="admin-page-container">
      <h2>Page d'administration</h2>
      <p>Bienvenue, administrateur ! Vous avez accès à cette page.</p>
      {/* Ajoute ici tout le contenu spécifique aux administrateurs */}

      {/* Bouton pour revenir au Dashboard */}
      <button onClick={handleGoBack} className="back-button">
        Retour au Dashboard
      </button>
    </div>
  );
}

export default AdminPage;
