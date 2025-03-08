"""
Module pour la gestion des boosters de cartes.

Ce module définit des classes pour créer et gérer des boosters de cartes,
ainsi que des fonctionnalités pour sélectionner des cartes aléatoires selon leur rareté.
"""
import random
from typing import List
from pydantic import BaseModel # type: ignore
from sqlalchemy.orm import Session # type: ignore
from backend.app.models.card_model import Card, CardBase
from backend.app.models.enums import Rarity

poids = {
    "commune": 1,
    "legendaire": 0.01,
    "rare": 0.3,
    "super_rare": 0.06
}

class BoosterBase(BaseModel):
    """
    Classe de base pour définir un booster de cartes.

    Attributs :
        name : str : Le nom du booster.
        cards : List[CardBase] : Liste des cartes incluses dans le booster.
    """
    name: str
    cards: List[CardBase] = []


class Booster(BaseModel):
    """
    Classe représentant un booster contenant des cartes.

    Attributs :
        name : str : Le nom du booster.
        cards : List[CardBase] : Liste des cartes contenues dans le booster.
    """
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
                (poids["commune"]if card.rarity == Rarity.COMMUNE else
                poids["rare"] if card.rarity == Rarity.RARE else
                poids["super_rare"] if card.rarity == Rarity.SUPER_RARE else
                poids["legendaire"])
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
