from Metiers.Enums import Rarity


class Card:
    def __init__(self, name: str, image_url: str, rarity: Rarity):
        self.name = name
        self.image_url = image_url
        self.rarity = rarity
