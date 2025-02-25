import random
import time
from typing import List

from sqlalchemy.orm import Session

from backend.app.models.Card import Card
from backend.app.models.Enums import Rarity


class BoosterService:
    last_open_time = {}  # Dernier horaire d’ouverture de l'utilisateur

    @staticmethod
    def open_booster(user_id: str, card: Card, db: Session, size: int = 5) -> List[Card]:
        current_time = time.time()
        last_time = BoosterService.last_open_time.get(user_id, 0)

        # Vérifier si 2 heures se sont écoulées depuis la dernière ouverture
        if current_time - last_time < 2 * 3600:
            raise Exception("Vous devez attendre avant d'ouvrir un autre booster !")

        # Sélectionner des cartes en fonction de leur rareté
        selected_cards = random.choices(
            Card.cards,
            weights=[
                (1 if card.rarity == Rarity.COMMUNE else
                0.5 if card.rarity == Rarity.RARE else
                0.1 if card.rarity == Rarity.SUPER_RARE else
                0.05)  # Légendaire
                for card in Card.cards
            ],
            k=size,
        )

        # Mettre à jour l'horaire de la dernière ouverture
        BoosterService.last_open_time[user_id] = current_time

        return selected_cards
