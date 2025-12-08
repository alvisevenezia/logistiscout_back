deps.py# app/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v2/auth/login")


def get_current_groupe(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.Groupe:
    """
    - Récupère le token dans Authorization: Bearer <token>
    - Décode le JWT
    - Charge le Groupe dans la BDD
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Jeton invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Décodage du JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        groupe_id: str | None = payload.get("sub")
        if groupe_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Récupération du groupe en BDD
    groupe = db.query(models.Groupe).filter(models.Groupe.id == int(groupe_id)).first()
    if groupe is None:
        raise credentials_exception

    return groupe
