from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import database, models

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    groupe_id: str
    groupe_mdp: str

@router.post("/auth/login")
def login(payload: LoginRequest = Body(...), db: Session = Depends(get_db)):
    # Vérification du groupe et du mot de passe dans la BDD
    groupe = db.query(models.Groupe).filter(models.Groupe.id == payload.groupe_id).first()
    if groupe and hasattr(groupe, "mdp") and groupe.mdp == payload.groupe_mdp:
        return {"token": "fake-token"}
    else:
        raise HTTPException(status_code=401, detail="Identifiants invalides")