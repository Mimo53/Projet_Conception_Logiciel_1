# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le backend dans le conteneur
COPY . .

# Exposer le port FastAPI
EXPOSE 8000

# Lancer l'application avec Uvicorn
CMD ["fastapi", "dev", "backend/main.py"]

# docker run --name fastapi_backend --env-file .env -p 8000:8000 fastapi_app

