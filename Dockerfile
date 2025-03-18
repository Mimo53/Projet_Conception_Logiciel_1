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
