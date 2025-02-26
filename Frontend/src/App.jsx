import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import Page2 from './pages/Page2';
import Accueil from './pages/Accueil';
import Boosters from './pages/Booster';
import Collection from './pages/Collection';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AdminPage from './pages/AdminPage';
import AddCardPage from './pages/AddCardPage';  // <-- Ajout ici
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/Booster" element={<Boosters />} />
        <Route path="/Accueil" element={<Accueil />} />
        <Route path="/page2" element={<Page2 />} />
        <Route path="/Collection" element={<Collection />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />

        <Route
          path="/admin"
          element={
            <PrivateRoute adminOnly={true}>
              <AdminPage />
            </PrivateRoute>
          }
        />

        {/* Route protégée pour Ajouter une carte */}
        <Route
          path="/AddCard"
          element={
            <PrivateRoute adminOnly={true}>
              <AddCardPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
