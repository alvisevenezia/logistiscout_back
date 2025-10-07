from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    userlogin: str
    mdp: str

@router.post("/auth/login")
def login(payload: LoginRequest = Body(...), db: Session = Depends(get_db)):
    # Vérification du userlogin et du mot de passe dans la BDD
    groupe = db.query(models.Groupe).filter(models.Groupe.userlogin == payload.userlogin).first()
    if groupe and groupe.mdp == payload.mdp:
        return {"token": "fake-token", "id": groupe.id, "nom": groupe.nom, "userlogin": groupe.userlogin}
    else:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

@router.post("/auth/create_group", response_model=schemas.Groupe, status_code=201)
def create_group(groupe: schemas.GroupeCreate, db: Session = Depends(get_db)):
    # Vérifie unicité du userlogin
    if db.query(models.Groupe).filter(models.Groupe.userlogin == groupe.userlogin).first():
        raise HTTPException(status_code=400, detail="userlogin déjà utilisé")
    db_groupe = models.Groupe(**groupe.dict())
    db.add(db_groupe)
    db.commit()
    db.refresh(db_groupe)
    return db_groupe