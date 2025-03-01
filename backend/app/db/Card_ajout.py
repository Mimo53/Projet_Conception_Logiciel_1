import re

from sqlalchemy.orm import Session  # type: ignore

from backend.app.db.database import Base, SessionLocal, engine
from backend.app.models.Card import Card
from backend.app.models.Enums import Rarity

Base.metadata.create_all(bind=engine)

# Exemple de données : une liste de dictionnaires pour chaque carte
cards_data = [
    {"name": "Carte 1", "image_url": "https://drive.google.com/uc?export=view&id=1GMpNng-_6gFJyuUAqRm3A-ftWqOQfi_a", "rarity": Rarity.COMMUNE},
    {"name": "Carte 2", "image_url": "https://drive.google.com/uc?export=view&id=13TkP1XkDoGZY1mA5f9GE8DYVerVfTTfD", "rarity": Rarity.RARE},
    {"name": "Carte 3", "image_url": "https://drive.google.com/uc?export=view&id=1ko369U4VrUVUU5Rj_9EjhwDXGCAFhPMh", "rarity": Rarity.LEGENDAIRE},
    {"name": "Carte 4", "image_url": "https://drive.google.com/uc?export=view&id=1f7ObQm4eKWZRIDkBvTJ7woYxbJnabJiD", "rarity": Rarity.LEGENDAIRE},
    {"name": "Carte 5", "image_url": "https://drive.google.com/uc?export=view&id=1S3z2FkCnoeeNEn7RdLacGnPfmG1DCRnh", "rarity": Rarity.COMMUNE},
    {"name": "Carte 6", "image_url": "https://drive.google.com/uc?export=view&id=1T9GWvvBd9DQCoTJuQjwuSsIjnclDpfZ6", "rarity": Rarity.COMMUNE},
    {"name": "Carte 9", "image_url": "https://drive.google.com/uc?export=view&id=1c4UcSwN9iw7Poc2YDKIUwR9tlNWhSCLC", "rarity": Rarity.COMMUNE},
    {"name": "Carte 10", "image_url": "https://drive.google.com/uc?export=view&id=1ouppM2sN6sJPXtxKKg5WP1tFw9D1PpC9", "rarity": Rarity.RARE},
    {"name": "Carte 11", "image_url": "https://drive.google.com/uc?export=view&id=1lzT7rYEPQLuPQnJcK1gBVKdrgdyod7KO", "rarity": Rarity.RARE},
    {"name": "Carte 12", "image_url": "https://drive.google.com/uc?export=view&id=1xox8ShG6lAOquRfuMjmx1lRPxtKLykww", "rarity": Rarity.COMMUNE},
    {"name": "Carte 13", "image_url": "https://drive.google.com/uc?export=view&id=16HDEfb63vD3igNnGM_H6AavVxSV-DfLf", "rarity": Rarity.COMMUNE},
    {"name": "Carte 14", "image_url": "https://drive.google.com/uc?export=view&id=1-nR6YOVDtxtpVHat_rTypICD_NI4cx0t", "rarity": Rarity.COMMUNE},
    {"name": "Carte 15", "image_url": "https://drive.google.com/uc?export=view&id=18eLD6Vs0OPh9UPxkFYLxrfYsrfHnXP1j", "rarity": Rarity.RARE},
    {"name": "Carte 16", "image_url": "https://drive.google.com/uc?export=view&id=14xRs5Y3ZFfPW6wGnLr2kXA_sruuqmqKm", "rarity": Rarity.COMMUNE},
    {"name": "Carte 17", "image_url": "https://drive.google.com/uc?export=view&id=1GfS0vyfn-XR5oZM2dMCEosn1g10xbImm", "rarity": Rarity.COMMUNE},
    {"name": "Carte 18", "image_url": "https://drive.google.com/uc?export=view&id=13TzQYCqjlfFki8NyCsbUlYBLXBJQ0PXp", "rarity": Rarity.COMMUNE},
    {"name": "Carte 19", "image_url": "https://drive.google.com/uc?export=view&id=1YVemrmP-6AvmssBKsMApnREmSBgXPaXL", "rarity": Rarity.RARE},
    {"name": "Carte 20", "image_url": "https://drive.google.com/uc?export=view&id=1lI8M8LOdga8WGsZVEepfh-KFDw9be2qV", "rarity": Rarity.COMMUNE},
    {"name": "Carte 21", "image_url": "https://drive.google.com/uc?export=view&id=1t6zHDEHSYV6zMDMWLNWXseajBEy1K6q2", "rarity": Rarity.LEGENDAIRE},
    {"name": "Carte 22", "image_url": "https://drive.google.com/uc?export=view&id=1qInvREMPEoXRjflVxTjOvHE5TcTn17AP", "rarity": Rarity.LEGENDAIRE},
    {"name": "Carte 23", "image_url": "https://drive.google.com/uc?export=view&id=16hMKcCkpWvZ6I5fNCUDuaed7HAZ9U2MU", "rarity": Rarity.COMMUNE},
    {"name": "Carte 24", "image_url": "https://drive.google.com/uc?export=view&id=1UTDM01K8QX532wmJfCoRBmAled5tVly4", "rarity": Rarity.COMMUNE},
    {"name": "1.18", "image_url": "https://drive.google.com/uc?export=view&id=1FDr4XR9ifvMpxd0UQXAhAn9-78CAWBgW", "rarity": Rarity.COMMUNE},
    {"name": "Alban_Ex", "image_url": "https://drive.google.com/uc?export=view&id=1gefXK74DV80uA-ssvOcLOpnQcZJzA_hX", "rarity": Rarity.LEGENDAIRE},
    {"name": "Alban", "image_url": "https://drive.google.com/uc?export=view&id=1Axn058492gTc6s1jN7xis6L-BqYr0gmB", "rarity": Rarity.COMMUNE},
    {"name": "Andre", "image_url": "https://drive.google.com/uc?export=view&id=1iQZZXoQFucNcVZ4TrkQZfFc47sJV39d2", "rarity": Rarity.COMMUNE},
    {"name": "Axel_Ex", "image_url": "https://drive.google.com/uc?export=view&id=1-ANT7wIDAfkH_etCmJFx--MhMWnCfPfz", "rarity": Rarity.SUPER_RARE},
    {"name": "Axel", "image_url": "https://drive.google.com/uc?export=view&id=1aZLcHdpi0ADMELtYi2YMtA1IuWNJ0gp4", "rarity": Rarity.COMMUNE},
    {"name": "Camille_Ex", "image_url": "https://drive.google.com/uc?export=view&id=1O0H02owmyUkxDw2OxmdBk8VWRXixe0mg", "rarity": Rarity.SUPER_RARE},
    {"name": "Camille", "image_url": "https://drive.google.com/uc?export=view&id=1aJi7B5LyKwVmxDr-3JWIvrkkHVZQu2ra", "rarity": Rarity.COMMUNE},
    {"name": "AX", "image_url": "https://drive.google.com/uc?export=view&id=1-oNDk4HT7p0D3cxjWPC_uA9SP6nJ_HBJ", "rarity": Rarity.RARE},
    {"name": "Clementine", "image_url": "https://drive.google.com/uc?export=view&id=1M7GJoL-qh3lgk_Y8lZnpFYmP8jOI_zYa", "rarity": Rarity.COMMUNE},
    {"name": "Dorian", "image_url": "https://drive.google.com/uc?export=view&id=1y3YrNrP-351NjxVjYXYbVWAvM-vnhfCg", "rarity": Rarity.RARE},
    {"name": "Florian", "image_url": "https://drive.google.com/uc?export=view&id=1B7cr3c1izOIMtFdtZsSjoXJfX3zOgjNE", "rarity": Rarity.COMMUNE},
    {"name": "Jolan", "image_url": "https://drive.google.com/uc?export=view&id=1-xmzBUxdewoUFBLYzQVHcNvbGp-v-j6_", "rarity": Rarity.RARE},
    {"name": "Jules", "image_url": "https://drive.google.com/uc?export=view&id=1c3uMFLZP3mifRy2erbx-fl8RKdo6g2sa", "rarity": Rarity.RARE},
    {"name": "Lorane", "image_url": "https://drive.google.com/uc?export=view&id=1qrYayRzfPa2ObuzvuKGTuTPN8mSJ1hHl", "rarity": Rarity.COMMUNE},
    {"name": "Mathieu_Ex", "image_url": "https://drive.google.com/uc?export=view&id=1wPSGs6wJZBgchU5Hu8KUqKJ_i5VTjOGy", "rarity": Rarity.SUPER_RARE},
    {"name": "Mathieu", "image_url": "https://drive.google.com/uc?export=view&id=1zvxiI3LRMaxnbSgd6wIzHlGlQua5RM6c", "rarity": Rarity.RARE},
    {"name": "Matteo", "image_url": "https://drive.google.com/uc?export=view&id=1hHte8n_TVaGzKI4VFAWkR_KqZrXM14ok", "rarity": Rarity.RARE},
    {"name": "Maxence_Ex", "image_url": "https://drive.google.com/uc?export=view&id=180VeHGpFG5nwFX2UQypUSzb_AIkHH-n_", "rarity": Rarity.SUPER_RARE},
    {"name": "Maxence", "image_url": "https://drive.google.com/uc?export=view&id=1YM6nhxXFMJhAjhNCheF8qf0UAe7MAaxL", "rarity": Rarity.RARE},
    {"name": "Momo", "image_url": "https://drive.google.com/uc?export=view&id=1-Ippys8ZdarFKapyIe7lpFbfz2wVEBRW", "rarity": Rarity.COMMUNE},
    {"name": "Nathan_Ex", "image_url": "https://drive.google.com/uc?export=view&id=13hmcufvedi1xe65BKPqFtNOwAsj3ogV2", "rarity": Rarity.SUPER_RARE},
    {"name": "Nathan", "image_url": "https://drive.google.com/uc?export=view&id=13tkgqxaBM8UD7hz8YsfF1vXRAJriXAxd", "rarity": Rarity.SUPER_RARE},
    {"name": "Souk_Ex", "image_url": "https://drive.google.com/uc?export=view&id=16m4XWXJCufd5h3s1gEy5UG0UjuAoT3ij", "rarity": Rarity.SUPER_RARE},
    {"name": "Souk", "image_url": "https://drive.google.com/uc?export=view&id=1cvPfb0UJWj5aXMcw5azkxK6rEmbFzvt4", "rarity": Rarity.RARE},
    {"name": "Vito_Ex", "image_url": "https://drive.google.com/uc?export=view&id=1jOXyL7EymIn5Xw3QiB3TNqS3SzXYAbks", "rarity": Rarity.SUPER_RARE},
    {"name": "Vito", "image_url": "https://drive.google.com/uc?export=view&id=17I_lS0i8JxSIQiqLC7aYZF3VLye7unRg", "rarity": Rarity.COMMUNE},
    {"name": "Paulin_Gx", "image_url": "https://drive.google.com/uc?export=view&id=1xCt86USG-7cv2WeBScx5DgD311Ve-r4T", "rarity": Rarity.SUPER_RARE},

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
