// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import Page2 from './pages/Page2';
import Accueil from './pages/Accueil';
import Boosters from './pages/Booster';
import Collection from './pages/Collection';

function App() {
  return (
    <Router>
      <Routes>
        {/* Route pour la page d'accueil */}
        <Route path="/" element={<HomePage />} />

        {/* Route pour la page des boosters */}
        <Route path="/Booster" element={<Boosters />} />

        {/* Route pour la page d'Accueil */}
        <Route path="/Accueil" element={<Accueil />} />

        {/* Route pour la page 2 */}
        <Route path="/page2" element={<Page2 />} />

        {/* Route pour la page de Collection */}
        <Route path="/Collection" element={<Collection />} />
      </Routes>
    </Router>
  );
}

export default App;
