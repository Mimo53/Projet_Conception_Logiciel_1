// src/pages/Login.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import './Login.css';  // Assurez-vous que le fichier CSS est bien importé

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Envoie la requête pour se connecter
      await axios.post("/api/auth/login", { email, password });

      // Redirige l'utilisateur vers la page d'accueil après la connexion
      navigate("/Accueil");
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
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
