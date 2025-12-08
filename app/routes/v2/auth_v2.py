from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import verify_password, create_access_token, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/v2/auth/login")
def login(payload: LoginRequest = Body(...), db: Session = Depends(get_db)):
    groupe = (
        db.query(models.Groupe)
        .filter(models.Groupe.userlogin == payload.userlogin)
        .first()
    )

    if not groupe or not verify_password(payload.mdp, groupe.mdp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )

    # Contenu du token : par ex. ID et userlogin
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(groupe.id), "userlogin": groupe.userlogin},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": groupe.id,
        "nom": groupe.nom,
        "userlogin": groupe.userlogin,
    }


@router.post("/v2/auth/create_group", response_model=schemas.Groupe, status_code=201)
def create_group(groupe: schemas.GroupeCreate, db: Session = Depends(get_db)):

    if db.query(models.Groupe).filter(models.Groupe.userlogin == groupe.userlogin).first():
        raise HTTPException(status_code=400, detail="userlogin déjà utilisé")
    data = groupe.dict()
    plain_password = data.pop("mdp")
    hashed_password = hash_password(plain_password)
    db_groupe = models.Groupe(**data, mdp=hashed_password)

    db.add(db_groupe)
    db.commit()
    db.refresh(db_groupe)

    return db_groupe
