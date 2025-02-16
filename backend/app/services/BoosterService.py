import random
import time

from Metiers.Booster import Booster
from Metiers.Collection import Collection
from Metiers.Enums import Rarity


class BoosterService:
    last_open_time = {}  # Dernier horaire d’ouverture de l'utilisateur

    @staticmethod
    def open_booster(user_id: str, collection: Collection,
                     size: int = 5) -> Booster:
        """Simule l'ouverture d'un booster dans une collection
        avec un délai de 2h par utilisateur"""
        current_time = time.time()
        last_time = BoosterService.last_open_time.get(user_id, 0)

        if current_time - last_time < 2 * 3600:
            raise Exception("Vous devez attendre avant d'ouvrir "
                            "un autre booster !")

        selected_cards = random.choices(
            collection.list_cards(),
            weights=[
                (
                    1
                    if card.rarity == Rarity.COMMUNE
                    else (
                        0.5
                        if card.rarity == Rarity.RARE
                        else 0.2 if card.rarity == Rarity.SUPER_RARE else 0.05
                    )
                )  # Légendaire
                for card in collection.list_cards()
            ],
            k=size,
        )

        BoosterService.last_open_time[user_id] = (
            current_time  # Met à jour le dernier horaire  d’ouverture
        )
        return Booster(selected_cards)
