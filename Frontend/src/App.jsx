// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import Page2 from './pages/Page2';
import Accueil from './pages/Accueil';
import Boosters from './pages/Booster';
import Collection from './pages/Collection';
import Login from './pages/Login';
import Register from './pages/Register';

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
      </Routes>
    </Router>
  );
}

export default App;
