from typing import List

from models.Card import Card


class Collection:
    def __init__(self, name: str, cards: List[Card]):
        self.name = name
        self.cards = cards
