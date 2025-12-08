# app/routes/v2/evenements_v2.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.routes.v2.deps import get_current_groupe  # 🔑 récupère le groupe depuis le JWT

router = APIRouter()


@router.get("/evenements", response_model=List[schemas.Evenement])
def list_evenements(
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    """
    Ne retourne que les événements du groupe lié au token.
    Le client n'envoie plus de groupeId.
    """
    return (
        db.query(models.Evenement)
        .filter(models.Evenement.groupeId == current_groupe.id)
        .all()
    )


@router.post("/evenements", response_model=schemas.Evenement, status_code=201)
def create_evenement(
    evenement: schemas.EvenementCreate,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    """
    Crée un événement pour le groupe du token.
    On force le groupeId côté serveur.
    """
    data = evenement.dict()
    data["groupeId"] = current_groupe.id  # 🔒 on impose le groupe

    db_evenement = models.Evenement(**data)
    db.add(db_evenement)
    db.commit()
    db.refresh(db_evenement)
    return db_evenement


def _get_evenement_for_current_groupe(
    evenement_id: int,
    db: Session,
    current_groupe: models.Groupe,
) -> models.Evenement:
    """
    Helper interne : récupère l'événement si il appartient au groupe courant,
    sinon 404.
    """
    evenement = (
        db.query(models.Evenement)
        .filter(
            models.Evenement.id == evenement_id,
            models.Evenement.groupeId == current_groupe.id,
        )
        .first()
    )
    if not evenement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Événement non trouvé ou accès refusé",
        )
    return evenement


@router.get("/evenements/{evenement_id}", response_model=schemas.Evenement)
def get_evenement(
    evenement_id: int,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    return _get_evenement_for_current_groupe(evenement_id, db, current_groupe)


@router.put("/evenements/{evenement_id}", response_model=schemas.Evenement)
def update_evenement(
    evenement_id: int,
    evenement: schemas.EvenementUpdate,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    db_evenement = _get_evenement_for_current_groupe(evenement_id, db, current_groupe)

    for key, value in evenement.dict(exclude_unset=True).items():
        # On évite qu'un client ne change le groupeId
        if key == "groupeId":
            continue
        setattr(db_evenement, key, value)

    db.commit()
    db.refresh(db_evenement)
    return db_evenement


@router.delete("/evenements/{evenement_id}", status_code=204)
def delete_evenement(
    evenement_id: int,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    db_evenement = _get_evenement_for_current_groupe(evenement_id, db, current_groupe)

    db.delete(db_evenement)
    db.commit()
    return
