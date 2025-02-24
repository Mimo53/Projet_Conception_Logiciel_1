import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('token'); // Ou ton propre mécanisme d'authentification

  // Si l'utilisateur n'est pas authentifié, redirige vers la page de connexion
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  // Sinon, affiche les enfants (la page protégée)
  return children;
};

export default PrivateRoute;
