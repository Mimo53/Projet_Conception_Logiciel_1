import random
from typing import List
from sqlalchemy.orm import Session
from backend.app.models.Card import Card,CardBase
from backend.app.models.Enums import Rarity
from pydantic import BaseModel


class BoosterBase(BaseModel):
    name: str
    cards: List[CardBase] = []


class Booster(BaseModel):  #
    name: str
    cards: List[CardBase] = []

class BoosterBuilder:
    def __init__(self, db: Session):
        """
        Initialise le builder avec une session de base de données.
        """
        self.db = db
        self.selected_cards: List[Card] = []

    def with_random_cards(self, count: int = 5) -> "BoosterBuilder":
        """
        Sélectionne aléatoirement 'count' cartes avec des poids selon leur rareté.
        """
        all_cards = self.db.query(Card).all()
        if len(all_cards) < count:
            raise ValueError("Pas assez de cartes disponibles pour générer un booster.")

        self.selected_cards = random.choices(
            all_cards,
            weights=[
                (1 if card.rarity == Rarity.COMMUNE else
                 0.5 if card.rarity == Rarity.RARE else
                 0.1 if card.rarity == Rarity.SUPER_RARE else
                 0.05)  # Légendaire
                for card in all_cards
            ],
            k=count,
        )
        return self

    def build(self) -> List[Card]:
        """
        Retourne les cartes du booster.
        """
        return self.selected_cards
