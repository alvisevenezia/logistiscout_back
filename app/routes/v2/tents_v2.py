# app/routes/v2/tentes_v2.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.deps import get_current_groupe  # 🔑 pour récupérer le groupe depuis le token

router = APIRouter()


@router.get("/tentes", response_model=List[schemas.Tente])
def list_tentes(
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    """
    Retourne uniquement les tentes du groupe lié au token.
    Le client n'a plus besoin d'envoyer groupeId.
    """
    return (
        db.query(models.Tente)
        .filter(models.Tente.groupeId == current_groupe.id)
        .all()
    )


@router.post("/tentes", response_model=schemas.Tente, status_code=201)
def create_tente(
    tente: schemas.TenteCreate,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    """
    Crée une tente pour le groupe du token.
    On ignore un éventuel groupeId envoyé dans le body.
    """
    data = tente.dict()
    data["groupeId"] = current_groupe.id  # 🔒 force le groupe côté serveur

    db_tente = models.Tente(**data)
    db.add(db_tente)
    db.commit()
    db.refresh(db_tente)
    return db_tente


def _get_tente_for_current_groupe(
    tente_id: int,
    db: Session,
    current_groupe: models.Groupe,
) -> models.Tente:
    """
    Helper interne : récupère la tente si elle appartient au groupe courant,
    sinon lève une 404.
    """
    tente = (
        db.query(models.Tente)
        .filter(
            models.Tente.id == tente_id,
            models.Tente.groupeId == current_groupe.id,
        )
        .first()
    )
    if not tente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tente non trouvée ou accès refusé",
        )
    return tente


@router.get("/tentes/{tente_id}", response_model=schemas.Tente)
def get_tente(
    tente_id: int,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    return _get_tente_for_current_groupe(tente_id, db, current_groupe)


@router.put("/tentes/{tente_id}", response_model=schemas.Tente)
def update_tente(
    tente_id: int,
    tente: schemas.TenteUpdate,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    db_tente = _get_tente_for_current_groupe(tente_id, db, current_groupe)

    for key, value in tente.dict(exclude_unset=True).items():
        # On s'assure que groupeId ne soit pas modifiable
        if key == "groupeId":
            continue
        setattr(db_tente, key, value)

    db.commit()
    db.refresh(db_tente)
    return db_tente


@router.delete("/tentes/{tente_id}", status_code=204)
def delete_tente(
    tente_id: int,
    db: Session = Depends(get_db),
    current_groupe: models.Groupe = Depends(get_current_groupe),
):
    db_tente = _get_tente_for_current_groupe(tente_id, db, current_groupe)

    # On supprime aussi les contrôles liés à cette tente
    db.query(models.Controle).filter(models.Controle.tenteId == tente_id).delete()
    db.delete(db_tente)
    db.commit()
    return
