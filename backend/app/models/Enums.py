from enum import Enum


class Role(Enum):
    ADMIN = "Admin"
    USER = "User"
    clown = "clown"


class Rarity(Enum):
    COMMUNE = "Commune"
    RARE = "Rare"
    SUPER_RARE = "Super Rare"
    LEGENDAIRE = "Légendaire"