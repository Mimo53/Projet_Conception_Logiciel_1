// src/pages/Register.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import './Inscription.css';  // Assurez-vous que le fichier CSS est bien importé

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("user");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      // Envoie la requête pour créer un nouvel utilisateur
      await axios.post("/api/auth/register", {
        username,
        password,
        e_mail: email,
        role,
      });

      // Redirige l'utilisateur vers la page de connexion après l'inscription
      navigate("/login");
    } catch (err) {
      setError("Erreur lors de la création de votre compte");
    }
  };

  return (
    <div className="inscription-container">
      <h2>S'inscrire</h2>
      <form onSubmit={handleRegister}>
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
        <div className="input-container">
          <label>Rôle</label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="user">Utilisateur</option>
            <option value="admin">Administrateur</option>
          </select>
        </div>
        {error && <div className="error-message">{error}</div>}
        <button type="submit">S'inscrire</button>
      </form>
      <div className="link-container">
        <span>Déjà un compte ? </span>
        <button onClick={() => navigate("/login")}>Se connecter</button>
      </div>
    </div>
  );
}

export default Register;
