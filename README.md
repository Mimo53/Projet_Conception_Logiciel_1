# Projet Info 2A : ENSAI TCG

Bienvenue sur **ENSAI TCG**, un projet inspiré du célèbre Pokémon TCG ! 🚀

Ce projet vous permet d’ouvrir des boosters pour découvrir des cartes humoristiques basées sur les élèves de l’ENSAI. Toutes les photos utilisées ont été validées avec l'accord des personnes concernées.

---

## 📌 Fonctionnalités

- 🔹 **Inscription et connexion sécurisée** avec vérification par email.
- 🔹 **Ouverture de boosters ENSAI** pour collectionner des cartes.
- 🔹 **Affichage de sa collection personnelle**.
- 🔹 **Ajout de cartes personnalisées** (format PNG ou PDF) via une demande validée par les administrateurs.
- 🔹 Peut-être des améliorations futures si on en a la foi ! (Non) 🚧

---

## 🚀 Quickstart

### 📦 Prérequis
Avant de commencer, assurez-vous d’avoir installé :
- Python 3.10
- Node.js & npm

### 🛠️ Installation
1. **Cloner le projet**
   ```bash
   Clonez le dépot git quoi (feur)
   ```
2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   npm install axios
   npm install react react-dom
   npm install react-router-dom
   ```

3. **Créer le fichier `.env`**

   Créez un fichier `.env` à la racine du projet et copiez-collez le contenu du fichier `.env.template`
   Faisable facilement avec la commande suivante:
   ```bash
   cp .env.example .env
   ```
   Modifiez ensuite les informations selon votre installation.




### ▶️ Lancer l’application
1. **Télécharger les premières cartes**
   ```bash
   python3 -m backend.app.db.Card_ajout
   ```

2. **Démarrer le backend**
   ```bash
   uvicorn backend.main:app --reload
   ```
3. **Démarrer le frontend**
   ```bash
   cd Frontend
   npm run dev
   ```

---

## 🎨 Aperçu
![image](https://github.com/user-attachments/assets/5a357f7d-0bf1-469a-8c6f-fb2740109814)

---

## 📬 Crédits
Ce projet a été créé par Mohamed, André et Dorian, vos fidèles serviteurs, sur une idée originale (on a les droits si on le crédite) de Florian !
