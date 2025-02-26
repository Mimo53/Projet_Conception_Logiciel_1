import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import './Register.css';  // Assurez-vous que le fichier CSS est bien importé

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState(""); // Ajout de la confirmation de mot de passe
  const [email, setEmail] = useState("");
  const [role] = useState("User"); // Rôle par défaut
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Vérifie que les mots de passe correspondent
    if (password !== confirmPassword) {
      setError("Les mots de passe ne correspondent pas.");
      setLoading(false);
      return;
    }

    try {
      // Envoie la requête pour créer un nouvel utilisateur
      await axios.post("http://localhost:8000/auth/register", {
        username,
        password,
        e_mail: email,  // Assurez-vous que le backend attend bien 'e_mail'
        role,
      });

      // Redirige l'utilisateur vers la page de connexion après l'inscription
      navigate("/login");
    } catch (err) {
      // Si l'erreur est un 422, affiche les détails
      if (err.response && err.response.status === 422) {
        console.error("Détails de l'erreur 422:", err.response.data);
        setError("Erreur de validation des données : " + JSON.stringify(err.response.data));
      } else {
        setError("Erreur lors de la création de votre compte");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2>Créer un compte</h2>
        <form onSubmit={handleRegister} className="form-container">
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
            <label>Confirmation du mot de passe</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <div className="button-container">
            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? "Inscription en cours..." : "S'inscrire"}
            </button>
            <button
              type="button"
              onClick={() => navigate("/login")}
              className="link-button"
            >
              Se connecter
            </button>
          </div>
        </form>

        {/* Bouton pour revenir à l'accueil */}
        <button onClick={() => navigate("/Accueil")} className="back-to-home-button">
          Retour à l'accueil
        </button>
      </div>
    </div>
  );
}

export default Register;
