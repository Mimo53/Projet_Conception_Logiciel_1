"""
Ce module définit les énumérations utilisées dans l'application.
"""

from enum import Enum

class Role(Enum):
    """Rôles disponibles dans l'application."""
    ADMIN = "Admin"
    USER = "User"
    CLOWN = "Clown"

class Rarity(Enum):
    """Niveaux de rareté des cartes."""
    COMMUNE = "Commune"
    RARE = "Rare"
    SUPER_RARE = "Super Rare"
    LEGENDAIRE = "Légendaire"
