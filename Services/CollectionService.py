from typing import List

from Metiers.Card import Card
from Metiers.Collection import Collection


class CollectionService:
    """Service pour gérer les collections"""

    @staticmethod
    def add_card_to_collection(collection: Collection, card: Card):
        """Ajoute une carte à la collection"""
        if card not in collection.cards:
            collection.cards.append(card)

    @staticmethod
    def remove_card_from_collection(collection: Collection, card: Card):
        """Supprime une carte de la collection"""
        if card in collection.cards:
            collection.cards.remove(card)

    @staticmethod
    def get_all_cards(collection: Collection) -> List[Card]:
        """Retourne toutes les cartes d'une collection"""
        return collection.cards
