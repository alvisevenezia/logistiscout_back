from fastapi import APIRouter, HTTPException, Depends
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
def list_evenements(db: Session = Depends(get_db)):
    return db.query(models.Evenement).all()

@router.post("/evenements", response_model=schemas.Evenement, status_code=201)
def create_evenement(evenement: schemas.Evenement, db: Session = Depends(get_db)):
    db_evenement = models.Evenement(**evenement.dict(exclude={"tentesAssociees"}))
    db.add(db_evenement)
    db.commit()
    db.refresh(db_evenement)
    # À compléter : gestion de l'association des tentes à l'événement si besoin
    return db_evenement

@router.get("/evenements/{evenement_id}", response_model=schemas.Evenement)
def get_evenement(evenement_id: int, db: Session = Depends(get_db)):
    evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id).first()
    if not evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    return evenement

@router.delete("/evenements/{evenement_id}", status_code=204)
def delete_evenement(evenement_id: int, db: Session = Depends(get_db)):
    evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id).first()
    if not evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    db.delete(evenement)
    db.commit()
    return