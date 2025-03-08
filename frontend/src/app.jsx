import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/home_page';
import Page2 from './pages/page2';
import Accueil from './pages/accueil';
import Boosters from './pages/booster';
import Collection from './pages/collection';
import Login from './pages/login';
import Register from './pages/register';
import Dashboard from './pages/dashboard';
import AdminPage from './pages/admin_page';
import AddCardPage from './pages/add_card_page';  // <-- Ajout ici
import PrivateRoute from './components/private_route';

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
