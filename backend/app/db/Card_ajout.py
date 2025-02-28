from backend.app.models.Enums import Rarity
from sqlalchemy.orm import Session  # type: ignore
from backend.app.db.database import SessionLocal
from backend.app.models.Card import Card
import re

# Exemple de données : une liste de dictionnaires pour chaque carte
cards_data = [
    {"name": "Carte 1", "image_url": "https://drive.google.com/uc?export=view&id=1GMpNng-_6gFJyuUAqRm3A-ftWqOQfi_a", "rarity": Rarity.COMMUNE},
    {"name": "Carte 2", "image_url": "https://drive.google.com/uc?export=view&id=13TkP1XkDoGZY1mA5f9GE8DYVerVfTTfD", "rarity": Rarity.RARE},
    {"name": "Carte 3", "image_url": "https://drive.google.com/uc?export=view&id=1ko369U4VrUVUU5Rj_9EjhwDXGCAFhPMh", "rarity": Rarity.LEGENDAIRE},
    {"name": "Carte 4", "image_url": "https://drive.google.com/uc?export=view&id=1f7ObQm4eKWZRIDkBvTJ7woYxbJnabJiD", "rarity": Rarity.LEGENDAIRE},
    {"name": "Carte 5", "image_url": "https://drive.google.com/uc?export=view&id=1S3z2FkCnoeeNEn7RdLacGnPfmG1DCRnh", "rarity": Rarity.COMMUNE},
    {"name": "Carte 6", "image_url": "https://drive.google.com/uc?export=view&id=1T9GWvvBd9DQCoTJuQjwuSsIjnclDpfZ6", "rarity": Rarity.COMMUNE}
]

def extract_drive_id(url):
    """
    Extrait l'ID du fichier Google Drive à partir de l'URL.
    """
    pattern = r"https://drive\.google\.com/(?:file/d|uc\?export=view&id)=([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        print(f"URL invalide ou non compatible : {url}")
        return None

def convert_to_direct_url(image_url):
    """
    Convertit l'URL en une URL directe utilisable dans une balise <img>.
    """
    file_id = extract_drive_id(image_url)
    if file_id:
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    else:
        return image_url

def populate_cards():
    db: Session = SessionLocal()
    try:
        for card_info in cards_data:
            # Conversion de l'URL avant insertion
            direct_url = convert_to_direct_url(card_info["image_url"])
            
            card = Card(
                name=card_info["name"],
                image_url=direct_url,  # Utilisation de l'URL directe
                rarity=card_info["rarity"]
            )
            print(f"Insertion de la carte : {card.name} avec URL : {direct_url}")
            db.add(card)
        db.commit()
        print("Cartes insérées avec succès dans la base.")
    except Exception as e:
        db.rollback()
        print("Erreur lors de l'insertion des cartes:", e)
    finally:
        db.close()

if __name__ == "__main__":
    populate_cards()
