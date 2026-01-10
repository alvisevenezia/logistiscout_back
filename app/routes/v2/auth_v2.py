from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import models, schemas, database
from app.security import verify_password, create_access_token, create_refresh_token, hash_password, decode_token, ACCESS_TOKEN_EXPIRE_MINUTES

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
class LoginRequest(BaseModel):
    userlogin: str
    mdp: str


@router.post("/auth/login")
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

    refresh_token = create_refresh_token(
        data={"sub": str(groupe.id), "userlogin": groupe.userlogin}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "id": groupe.id,
        "nom": groupe.nom,
        "userlogin": groupe.userlogin,
    }


@router.post("/auth/create_group", response_model=schemas.Groupe, status_code=201)
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


class RefreshIn(BaseModel):
    refresh_token: str

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

@router.post("/auth/refresh", response_model=TokenOut)
def refresh(payload: RefreshIn):
    try:
        claims = decode_token(payload.refresh_token)
    except JWTError:
        # expired or invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    if claims.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong token type",
        )

    subject = claims.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # Optional: check user still exists / active in DB

    new_access = create_access_token({"sub": subject})

    new_refresh = create_refresh_token({"sub": subject})
    return TokenOut(access_token=new_access, refresh_token=new_refresh)
