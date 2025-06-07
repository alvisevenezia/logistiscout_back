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

@router.get("/tentes", response_model=List[schemas.Tente])
def list_tentes(groupeId: str = Query(...), db: Session = Depends(get_db)):
    return db.query(models.Tente).all()

@router.post("/tentes", response_model=schemas.Tente, status_code=201)
def create_tente(tente: schemas.TenteCreate, db: Session = Depends(get_db)):
    db_tente = models.Tente(**tente.dict())
    db.add(db_tente)
    db.commit()
    db.refresh(db_tente)
    return db_tente

@router.get("/tentes/{tente_id}", response_model=schemas.Tente)
def get_tente(tente_id: int, db: Session = Depends(get_db)):
    tente = db.query(models.Tente).filter(models.Tente.id == tente_id).first()
    if not tente:
        raise HTTPException(status_code=404, detail="Tente non trouvée")
    return tente

@router.put("/tentes/{tente_id}", response_model=schemas.Tente)
def update_tente(tente_id: int, tente: schemas.TenteUpdate, db: Session = Depends(get_db)):
    db_tente = db.query(models.Tente).filter(models.Tente.id == tente_id).first()
    if not db_tente:
        raise HTTPException(status_code=404, detail="Tente non trouvée")
    # Vérifie que le groupeId envoyé correspond à celui de la tente
    if hasattr(tente, 'groupeId') and tente.groupeId is not None and db_tente.groupeId != tente.groupeId:
        raise HTTPException(status_code=403, detail="Groupe non autorisé à modifier cette tente")
    for key, value in tente.dict(exclude_unset=True).items():
        setattr(db_tente, key, value)
    db.commit()
    db.refresh(db_tente)
    return db_tente

@router.delete("/tentes/{tente_id}", status_code=204)
def delete_tente(tente_id: int, db: Session = Depends(get_db)):
    db_tente = db.query(models.Tente).filter(models.Tente.id == tente_id).first()
    if not db_tente:
        raise HTTPException(status_code=404, detail="Tente non trouvée")
    # Supprimer tous les contrôles associés à la tente
    db.query(models.Controle).filter(models.Controle.tenteId == tente_id).delete()
    db.delete(db_tente)
    db.commit()
    return