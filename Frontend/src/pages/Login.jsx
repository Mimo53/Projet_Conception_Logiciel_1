import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import jwt_decode from 'jwt-decode';  // Importation correcte
import './Login.css';

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await axios.post("http://localhost:8000/auth/token", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      if (response.data.access_token) {
        const token = response.data.access_token;
        localStorage.setItem("token", token);

        const decodedToken = jwt_decode(token);  // Décodage du token avec la bonne méthode
        console.log("Decoded token:", decodedToken);

        localStorage.setItem("role", decodedToken.role);
        localStorage.setItem("user_id", decodedToken.user_id);

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
            <label>Nom d'utilisateur</label>
            <input
              type="text"
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

        {/* Bouton pour revenir à l'accueil */}
        <button onClick={() => navigate("/Accueil")} className="back-to-home-button">
          Retour à l'accueil
        </button>
      </div>
    </div>
  );
}

export default Login;
