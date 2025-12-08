from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/evenements", response_model=List[schemas.Evenement])
def list_evenements(groupeId: str = Query(...), db: Session = Depends(get_db)):
    # Ne retourne que les événements du groupe demandé
    return db.query(models.Evenement).filter(models.Evenement.groupeId == groupeId).all()

@router.post("/evenements", response_model=schemas.Evenement, status_code=201)
def create_evenement(evenement: schemas.EvenementCreate, db: Session = Depends(get_db)):
    # Vérifie que le groupeId est bien présent
    if not evenement.groupeId:
        raise HTTPException(status_code=400, detail="groupeId requis")
    db_evenement = models.Evenement(**evenement.dict())
    db.add(db_evenement)
    db.commit()
    db.refresh(db_evenement)
    return db_evenement

@router.get("/evenements/{evenement_id}", response_model=schemas.Evenement)
def get_evenement(evenement_id: int, groupeId: str = Query(...), db: Session = Depends(get_db)):
    evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id, models.Evenement.groupeId == groupeId).first()
    if not evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé ou accès refusé")
    return evenement

@router.put("/evenements/{evenement_id}", response_model=schemas.Evenement)
def update_evenement(evenement_id: int, evenement: schemas.EvenementUpdate, groupeId: str = Query(...), db: Session = Depends(get_db)):
    db_evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id, models.Evenement.groupeId == groupeId).first()
    if not db_evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé ou accès refusé")
    for key, value in evenement.dict(exclude_unset=True).items():
        setattr(db_evenement, key, value)
    db.commit()
    db.refresh(db_evenement)
    return db_evenement

@router.delete("/evenements/{evenement_id}", status_code=204)
def delete_evenement(evenement_id: int, groupeId: str = Query(...), db: Session = Depends(get_db)):
    evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id, models.Evenement.groupeId == groupeId).first()
    if not evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé ou accès refusé")
    db.delete(evenement)
    db.commit()
    return