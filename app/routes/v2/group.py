from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.routes.v2.deps import get_current_groupe

router = APIRouter()


def _to_group_profile(current_groupe: models.Groupe) -> dict:
    members_value = current_groupe.members
    if members_value is None and current_groupe.membres is not None:
        if isinstance(current_groupe.membres, list):
            members_value = ", ".join(current_groupe.membres)
        else:
            members_value = str(current_groupe.membres)

    return {
        "id": str(current_groupe.id),
        "name": current_groupe.nom,
        "email": current_groupe.email,
        "members": members_value,
        "login": current_groupe.userlogin,
        "type": current_groupe.type,
        "units": current_groupe.units or [],
    }


@router.get("/me", response_model=schemas.GroupeProfile)
def get_me(current_groupe: models.Groupe = Depends(get_current_groupe)):
    """
    Get the current authenticated user's information
    """
    return _to_group_profile(current_groupe)


@router.put("/me", response_model=schemas.GroupeProfile)
def update_me(
    payload: schemas.GroupeProfileUpdate,
    current_groupe: models.Groupe = Depends(get_current_groupe),
    db: Session = Depends(get_db),
):
    """
    Update current group profile fields
    """
    if payload.email is not None and payload.email != current_groupe.email:
        existing_email = db.query(models.Groupe).filter(
            models.Groupe.email == payload.email,
            models.Groupe.id != current_groupe.id,
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé",
            )

    if payload.login is not None and payload.login != current_groupe.userlogin:
        existing_login = db.query(models.Groupe).filter(
            models.Groupe.userlogin == payload.login,
            models.Groupe.id != current_groupe.id,
        ).first()
        if existing_login:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce login est déjà utilisé",
            )

    if payload.name is not None:
        current_groupe.nom = payload.name

    if payload.email is not None:
        current_groupe.email = payload.email

    if payload.members is not None:
        current_groupe.members = payload.members

    if payload.login is not None:
        current_groupe.userlogin = payload.login

    if payload.type is not None:
        current_groupe.type = payload.type

    if payload.units is not None:
        current_groupe.units = [
            unit.dict(exclude_none=True)
            for unit in payload.units
        ]

    db.commit()
    db.refresh(current_groupe)
    return _to_group_profile(current_groupe)


@router.patch("/me/email", response_model=schemas.Groupe)
def update_email(
    payload: schemas.GroupeEmailUpdate,
    current_groupe: models.Groupe = Depends(get_current_groupe),
    db: Session = Depends(get_db),
):
    """
    Update the email of the current authenticated user
    """
    # Check if email is already taken by another group
    existing_groupe = db.query(models.Groupe).filter(
        models.Groupe.email == payload.email,
        models.Groupe.id != current_groupe.id
    ).first()
    
    if existing_groupe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé"
        )
    
    current_groupe.email = payload.email
    db.commit()
    db.refresh(current_groupe)
    return current_groupe


@router.patch("/me/members", response_model=schemas.Groupe)
def update_members(
    payload: schemas.GroupeMembersUpdate,
    current_groupe: models.Groupe = Depends(get_current_groupe),
    db: Session = Depends(get_db),
):
    """
    Update the members list of the current authenticated user's group
    """
    current_groupe.membres = payload.membres
    db.commit()
    db.refresh(current_groupe)
    return current_groupe


@router.patch("/me/nom", response_model=schemas.Groupe)
def update_nom(
    payload: schemas.GroupeNomUpdate,
    current_groupe: models.Groupe = Depends(get_current_groupe),
    db: Session = Depends(get_db),
):
    """
    Update the name of the current authenticated user's group
    """
    current_groupe.nom = payload.nom
    db.commit()
    db.refresh(current_groupe)
    return current_groupe
