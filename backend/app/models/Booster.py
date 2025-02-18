from typing import List

from models.Card import Card


class Booster:
    def __init__(self, cards: List[Card]):
        self.cards = cards
