"""
Test utilsateur pour voir si les roles et la rareté
dans enums sont bien écrits
"""

from backend.app.models.enums import Role
from backend.app.models.enums import Rarity

def test_role_enum():
    """Test de l'énumération Role"""
    print(f"Role.ADMIN.value: {Role.ADMIN.value}")
    print(f"Role.USER.value: {Role.USER.value}")
    print(f"Role.CLOWN.value: {Role.CLOWN.value}")

    assert Role.ADMIN.value == "Admin"
    assert Role.USER.value == "User"
    assert Role.CLOWN.value == "Clown"

def test_rarity_enum():
    """Test de l'énumération Rarity"""
    print(f"Rarity.COMMUNE.value: {Rarity.COMMUNE.value}")
    print(f"Rarity.RARE.value: {Rarity.RARE.value}")
    print(f"Rarity.SUPER_RARE.value: {Rarity.SUPER_RARE.value}")
    print(f"Rarity.LEGENDAIRE.value: {Rarity.LEGENDAIRE.value}")

    assert Rarity.COMMUNE.value == "Commune"
    assert Rarity.RARE.value == "Rare"
    assert Rarity.SUPER_RARE.value == "Super Rare"
    assert Rarity.LEGENDAIRE.value == "Légendaire"
