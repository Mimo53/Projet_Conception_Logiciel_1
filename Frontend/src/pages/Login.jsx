import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';  // Assurez-vous que le fichier CSS est bien importé

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    // Simulation de la logique d'authentification
    if (email === "user@example.com" && password === "password") {
      navigate('/Accueil'); // Redirection après une connexion réussie
    } else {
      setError("Identifiants incorrects");
    }
  };

  return (
    <div className="login-container">
      <h2>Connexion</h2>
      <form onSubmit={handleLogin}>
        {error && <div className="error-message">{error}</div>}
        
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        
        <label htmlFor="password">Mot de passe</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Se connecter</button>
      </form>

      <div className="link-container">
        <p>Pas encore inscrit ? <a href="/register">Créer un compte</a></p>
      </div>
    </div>
  );
}

export default Login;
