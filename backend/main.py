from app.api.routes import router
from app.db.database import Base, engine
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
