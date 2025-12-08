from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.database import get_db
from app.routes.v2.deps import get_current_groupe  # 🔑 groupe courant via JWT

router = APIRouter()


@router.get("/controles", response_model=List[schemas.Controle])
def list_controles(
    tenteId: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    """
    Liste les contrôles des tentes appartenant au groupe courant,
    optionnellement filtrés par tenteId.
    """
    query = (
        db.query(models.Controle)
        .join(models.Tente, models.Controle.tenteId == models.Tente.id)
        .filter(models.Tente.groupeId == current_groupe.id)
    )

    if tenteId is not None:
        query = query.filter(models.Controle.tenteId == tenteId)

    return query.all()


def _get_controle_for_current_groupe(
    controle_id: int,
    db: Session,
    current_groupe: models.Groupe,
) -> models.Controle:
    """
    Helper : récupère un contrôle si la tente associée
    appartient au groupe courant, sinon 404.
    """
    controle = (
        db.query(models.Controle)
        .join(models.Tente, models.Controle.tenteId == models.Tente.id)
        .filter(
            models.Controle.id == controle_id,
            models.Tente.groupeId == current_groupe.id,
        )
        .first()
    )
    if not controle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrôle non trouvé ou accès refusé",
        )
    return controle


@router.post("/controles", response_model=schemas.Controle, status_code=201)
def create_controle(
    controle: schemas.ControleCreate,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    """
    Crée un contrôle uniquement si la tente liée
    appartient au groupe courant.
    """
    tente = (
        db.query(models.Tente)
        .filter(
            models.Tente.id == controle.tenteId,
            models.Tente.groupeId == current_groupe.id,
        )
        .first()
    )
    if not tente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tente non trouvée ou n'appartient pas à ce groupe",
        )

    db_controle = models.Controle(**controle.dict())
    db.add(db_controle)
    db.commit()
    db.refresh(db_controle)
    return db_controle


@router.get("/controles/{controle_id}", response_model=schemas.Controle)
def get_controle(
    controle_id: int,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    return _get_controle_for_current_groupe(controle_id, db, current_groupe)


@router.put("/controles/{controle_id}", response_model=schemas.Controle)
def update_controle(
    controle_id: int,
    controle: schemas.ControleUpdate,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    db_controle = _get_controle_for_current_groupe(controle_id, db, current_groupe)

    for key, value in controle.dict(exclude_unset=True).items():
        if key == "tenteId" and value is not None:
            # Vérifier que la nouvelle tente appartient toujours au groupe
            tente = (
                db.query(models.Tente)
                .filter(
                    models.Tente.id == value,
                    models.Tente.groupeId == current_groupe.id,
                )
                .first()
            )
            if not tente:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Nouvelle tente non trouvée ou n'appartient pas à ce groupe",
                )
        setattr(db_controle, key, value)

    db.commit()
    db.refresh(db_controle)
    return db_controle


@router.delete("/controles/{controle_id}", status_code=204)
def delete_controle(
    controle_id: int,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    controle = _get_controle_for_current_groupe(controle_id, db, current_groupe)
    db.delete(controle)
    db.commit()
    return
