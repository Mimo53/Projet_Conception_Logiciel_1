from backend.app.models.Enums import Rarity
from sqlalchemy.orm import Session # type: ignore
from backend.app.db.database import SessionLocal, engine, Base
from backend.app.models.Card import Card
# init

# Exemple de données : une liste de dictionnaires pour chaque carte
cards_data = [
    {"name": "Carte 1", "image_url": "https://drive.google.com/file/d/1GMpNng-_6gFJyuUAqRm3A-ftWqOQfi_a/view?usp=drive_link", "rarity": Rarity.COMMUNE},
    {"name": "Carte 2", "image_url": "https://drive.google.com/file/d/13TkP1XkDoGZY1mA5f9GE8DYVerVfTTfD/view", "rarity": Rarity.RARE},
    {"name": "Carte 3", "image_url": "https://drive.google.com/drive/u/1/folders/1GGl1EKo2j1Kq2W2PxqEm6j1NAXaOrU87", "rarity": Rarity.LEGENDAIRE},
    {"name": "Carte 4", "image_url": "https://drive.google.com/file/d/1f7ObQm4eKWZRIDkBvTJ7woYxbJnabJiD/view", "rarity": Rarity.LEGENDAIRE},
    {"name": "Carte 5", "image_url": "https://drive.google.com/file/d/1S3z2FkCnoeeNEn7RdLacGnPfmG1DCRnh/view?usp=drive_link", "rarity": Rarity.COMMUNE},
    {"name": "Carte 6", "image_url": "https://drive.google.com/file/d/1T9GWvvBd9DQCoTJuQjwuSsIjnclDpfZ6/view?usp=drive_link", "rarity": Rarity.COMMUNE}

]

def populate_cards():
    db: Session = SessionLocal()
    try:
        for card_info in cards_data:
            card = Card(
                name=card_info["name"],
                image_url=card_info["image_url"],
                rarity=card_info["rarity"]
            )
            print(f"Insertion de la carte : {card.name}")  
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
