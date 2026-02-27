from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.routes.v2.deps import get_current_groupe

router = APIRouter()


@router.get("/me", response_model=schemas.Groupe)
def get_me(current_groupe: models.Groupe = Depends(get_current_groupe)):
    """
    Get the current authenticated user's information
    """
    return current_groupe


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
