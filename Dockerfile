FROM ubuntu:22.04

# Mettre à jour et installer Python et pip
RUN apt-get update && apt-get install -y python3 python3-pip && ln -s /usr/bin/python3 /usr/bin/python

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de notre projet dans l'environnement
COPY . .

# Installer les dépendances
RUN python -m pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'application
EXPOSE 8000

# Créer un utilisateur sans privilèges root
RUN useradd -m myuser
USER myuser

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
