"""Ce module est un exemple de test pour démonstration."""

# Code du fichier test.py
print("Pitié")

# Une seule ligne vide à la fin du fichier
from dotenv import load_dotenv
import os

# Charger le fichier .env
load_dotenv()
if os.path.exists('.env'):
    print(".env file found!")
else:
    print(".env file not found!")
# Vérifier les variables
print(f"Loaded DATABASE_USER: {os.getenv('DATABASE_USER')}")
print(f"Loaded DATABASE_PASSWORD: {os.getenv('DATABASE_PASSWORD')}")
print(f"Loaded DATABASE_HOST: {os.getenv('DATABASE_HOST')}")
print(f"Loaded DATABASE_PORT: {os.getenv('DATABASE_PORT')}")
print(f"Loaded DATABASE_NAME: {os.getenv('DATABASE_NAME')}")
