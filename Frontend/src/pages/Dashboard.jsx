import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import jwt_decode from 'jwt-decode';  // Importation correcte
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const [isAdmin, setIsAdmin] = useState(false);
  const [role, setRole] = useState('');  // État pour stocker le rôle

  useEffect(() => {
    const token = localStorage.getItem("token");

    console.log("Token brut:", token);

    if (token) {
      try {
        const decodedToken = jwt_decode(token);

        console.log("Token décodé:", decodedToken);

        if (decodedToken.role) {
          // 🔥 Correction : Supprimer "Role." et mettre en minuscules
          const userRole = decodedToken.role.replace("Role.", "").toLowerCase();
          setRole(userRole);

          console.log("Rôle normalisé de l'utilisateur:", userRole);

          if (userRole === 'admin') {
            setIsAdmin(true);
          }
        } else {
          console.error("Le rôle n'est pas présent dans le token.");
          navigate("/login");
        }
      } catch (error) {
        console.error("Erreur de décodage du token", error);
        localStorage.removeItem('token');
        navigate("/login");
      }
    } else {
      console.warn("Token absent, redirection vers login.");
      navigate("/login");
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <h2>Bienvenue sur EnsaiTCG !</h2>
      <p>Vous êtes connecté en tant que : <strong>{role || "Inconnu"}</strong></p> {/* Affichage du rôle avec valeur par défaut */}

      <div className="button-container">
        <button onClick={() => navigate('/Collection')} className="collection-button">
          Collection
        </button>

        <button onClick={() => navigate('/Booster')} className="booster-button">
          Ouvrir un booster
        </button>

        {isAdmin && (
          <button onClick={() => navigate('/AddCard')} className="add-card-button">
            Ajouter une carte à la collection
          </button>
        )}

        {isAdmin && (
          <button onClick={() => navigate('/admin')} className="admin-button">
            Page d'administration
          </button>
        )}

        <button onClick={handleLogout} className="logout-button">
          Se déconnecter
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
