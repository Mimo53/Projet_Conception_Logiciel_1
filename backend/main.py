from fastapi import FastAPI

from backend.app.api.routes import router,router_auth
from backend.app.db.database import Base, engine
from backend.app.models.User import User,UserBase
from backend.app.models.Booster_Cards_asso import booster_cards, collection_cards
from backend.app.models import Card, Booster  # Importe tous les modèles nécessaires
import backend.app.api.routes


app = FastAPI()

app.include_router(router)
app.include_router(router_auth)
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
