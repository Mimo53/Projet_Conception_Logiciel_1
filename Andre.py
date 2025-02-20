from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

#necessite pip install unicorn pip install "fastapi[standard]"
    


def update_user(user: UserBase, db: Session = Depends(get_db)):
    # Recherche l'utilisateur dans la base de données par ID
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Met à jour le nom d'utilisateur et/ou le mot de passe si fourni
    if user.username:
        db_user.username = user.username
    if user.password:
        db_user.password = user.password