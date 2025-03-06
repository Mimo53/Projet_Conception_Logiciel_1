"""
Module d'initialisation de l'API backend.

Ce module contient les configurations et les routes principales pour l'API.
"""

from .routes import auth_router, booster_router, cards_router, proxy_router

__all__ = ["auth_router", "booster_router", "cards_router", "proxy_router"]
