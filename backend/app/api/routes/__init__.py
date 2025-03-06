"""
Module d'initialisation des routes
"""

from .auth import router as auth_router
from .booster import router as booster_router
from .cards import router as cards_router
from .proxy import router as proxy_router

__all__ = ["auth_router", "booster_router", "cards_router", "proxy_router"]
