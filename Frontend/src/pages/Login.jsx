// src/pages/Login.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import './Login.css'; // Assurez-vous que le fichier CSS est bien importé

function Login() {
  const [username, setUsername] = useState("");  // Utilisation de username
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Utilisation de URLSearchParams pour formater les données
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      // Envoie la requête pour se connecter à FastAPI
      const response = await axios.post("http://localhost:8000/auth/token", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"  // Obligatoire pour FastAPI
        }
      });

      // Vérifie si le token est présent dans la réponse
      if (response.data.access_token) {
        // Stocke le token dans le localStorage
        localStorage.setItem("token", response.data.access_token);
        
        // Récupérer le username de l'utilisateur après connexion
        try {
          const userResponse = await axios.get("http://localhost:8000/auth/user_id", {
            headers: { Authorization: `Bearer ${response.data.access_token}` }
          });
          console.log("Username récupéré : ", userResponse.data.user_id);
          localStorage.setItem("user_id", userResponse.data.user_id);  // Stocke le username de l'utilisateur
        } catch (err) {
          console.error("Erreur lors de la récupération du username de l'utilisateur :", err);
        }

        // Redirige l'utilisateur vers le Dashboard après la connexion
        navigate("/dashboard");
      } else {
        setError("Erreur lors de la connexion. Réessayez.");
      }
    } catch (err) {
      setError("Identifiants incorrects. Essayez à nouveau.");
    }
  };


  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Connexion</h2>
        <form onSubmit={handleLogin}>
          <div className="input-container">
            <label>Nom d'utilisateur</label> {/* Changement de label */}
            <input
              type="text" // Utilisation de "text" au lieu de "email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="input-container">
            <label>Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="submit-button">Se connecter</button>
        </form>
        <div className="link-container">
          <span>Pas encore de compte ? </span>
          <button onClick={() => navigate("/register")}>S'inscrire</button>
        </div>
      </div>
    </div>
  );
}

export default Login;
