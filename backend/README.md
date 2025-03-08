## Description des routes API

### 🔑 Authentification
| Méthode | Route                | Description                         | Authentification |
|---------|----------------------|-------------------------------------|------------------|
| **POST** | `/auth/register`      | Inscription utilisateur            | ❌               |
| **POST** | `/auth/token`         | Connexion & génération de token JWT | ❌               |
| **GET**  | `/auth/verify-email/{username}` | Vérification de l'email d'un utilisateur | ❌         |
| **PUT**  | `/auth/update_user/{username}` | Mise à jour des informations utilisateur | ✅ Token |

### 👤 Utilisateur
| Méthode | Route         | Description                         | Authentification |
|---------|--------------|-------------------------------------|------------------|
| **GET**  | `/users/me`   | Récupérer son profil               | ✅ Token         |
| **PUT**  | `/users/me`   | Modifier son profil                | ✅ Token         |

### 🎴 Cartes & Boosters
| Méthode | Route                        | Description                         | Authentification |
|---------|------------------------------|-------------------------------------|------------------|
| **GET**  | `/cards/`                    | Récupérer une liste de cartes       | ✅ Token         |
| **POST** | `/cards/`                    | Créer une nouvelle carte           | ✅ Token         |
| **POST** | `/booster/open_booster_and_add/` | Ouvrir un booster et ajouter des cartes | ✅ Token |
| **GET**  | `/booster/view_collections`  | Voir sa collection de cartes        | ✅ Token         |

### 🔧 Administration
| Méthode | Route           | Description                    | Authentification |
|---------|-----------------|--------------------------------|------------------|
| **GET**  | `/admin/users`   | Liste des utilisateurs         | 🔒 Admin         |

### 🌐 Proxy
| Méthode | Route                    | Description                               | Authentification |
|---------|--------------------------|-------------------------------------------|------------------|
| **GET**  | `/proxy/proxy-image/`     | Récupérer une image depuis une URL       | ❌               |


## Pour lancer le serveur Fastapi:
   ```bash
   uvicorn backend.main:app --reload
   ```

## Technologies utilisées:

- 🔹 **FastAPI** pour l'API comme son nom l'indique.
- 🔹 **PostgreSQL** pour la gestion de la base de données.
- 🔹 **JWT** pour l'authentification et la gestion des tokens.