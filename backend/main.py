from fastapi import FastAPI

from backend.app.api.routes import router
from backend.app.db.database import Base, engine

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
