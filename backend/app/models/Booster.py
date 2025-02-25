from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Card import CardBase,Card

booster_cards = Table(
    'booster_cards', Base.metadata,
    Column('booster_id', Integer, ForeignKey('boosters.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True)
)

class Booster(Base):
    __tablename__ = 'boosters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cards = relationship("Card", secondary=booster_cards, back_populates="boosters")


class BoosterBase(BaseModel):
    name: str
    cards: List[CardBase] = []

import random
from typing import List
from backend.app.models.Card import Card
from backend.app.models.Booster import Booster
from backend.app.models.Enums import Rarity

class BoosterBuilder:
    def __init__(self, available_cards: List[Card]):
        """
        Constructeur du builder avec la liste complète des cartes disponibles.
        """
        self.available_cards = available_cards
        self.selected_cards: List[Card] = []

    def with_random_cards(self, count: int) -> "BoosterBuilder":
        """
        Sélectionne aléatoirement 'count' cartes parmi les cartes disponibles.
        """
        if count > len(self.available_cards):
            raise ValueError("Pas assez de cartes disponibles pour sélectionner {} cartes.".format(count))
        self.selected_cards = random.sample(self.available_cards, count)
        return self

    def build(self) -> Booster:
        """
        Construit l'objet Booster en assignant la liste des cartes sélectionnées.
        """
        booster = Booster()
        booster.cards = self.selected_cards
        return booster


