import React from 'react';
import { Navigate } from 'react-router-dom';
import jwt_decode from 'jwt-decode';  // Import pour décoder le token JWT

const PrivateRoute = ({ children, adminOnly = false }) => {
  const token = localStorage.getItem('token');
  
  // Vérifie si le token est présent
  if (!token) {
    return <Navigate to="/login" />;
  }

  try {
    // Décode le token pour récupérer le rôle de l'utilisateur
    const decodedToken = jwt_decode(token);
    console.log("Token décodé dans PrivateRoute:", decodedToken);

    // 🔥 Correction : Nettoyer le rôle et le mettre en minuscules
    const userRole = decodedToken.role.replace("Role.", "").toLowerCase();
    console.log("Rôle normalisé dans PrivateRoute:", userRole);

    // Si l'utilisateur n'est pas un admin et que la route est réservée aux admin, on redirige
    if (adminOnly && userRole !== 'admin') {
      console.warn("Accès refusé : Non admin essayant d'accéder à une route admin.");
      return <Navigate to="/dashboard" />;  // Redirection vers le Dashboard si ce n'est pas un Admin
    }

  } catch (error) {
    console.error("Erreur de décodage du token", error);
    return <Navigate to="/login" />;  // Si le décodage échoue, redirige vers login
  }

  // Si l'utilisateur est authentifié et le rôle est correct (admin si nécessaire), on affiche le contenu
  return children;
};

export default PrivateRoute;
