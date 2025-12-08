from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ... import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/controles", response_model=List[schemas.Controle])
def list_controles(tenteId: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Controle)
    if tenteId is not None:
        query = query.filter(models.Controle.tenteId == tenteId)
    return query.all()

@router.post("/controles", response_model=schemas.Controle, status_code=201)
def create_controle(controle: schemas.ControleCreate, db: Session = Depends(get_db)):
    db_controle = models.Controle(**controle.dict())
    db.add(db_controle)
    db.commit()
    db.refresh(db_controle)
    return db_controle

@router.get("/controles/{controle_id}", response_model=schemas.Controle)
def get_controle(controle_id: int, db: Session = Depends(get_db)):
    controle = db.query(models.Controle).filter(models.Controle.id == controle_id).first()
    if not controle:
        raise HTTPException(status_code=404, detail="Contrôle non trouvé")
    return controle

@router.put("/controles/{controle_id}", response_model=schemas.Controle)
def update_controle(controle_id: int, controle: schemas.ControleUpdate, db: Session = Depends(get_db)):
    db_controle = db.query(models.Controle).filter(models.Controle.id == controle_id).first()
    if not db_controle:
        raise HTTPException(status_code=404, detail="Contrôle non trouvé")
    for key, value in controle.dict(exclude_unset=True).items():
        setattr(db_controle, key, value)
    db.commit()
    db.refresh(db_controle)
    return db_controle

@router.delete("/controles/{controle_id}", status_code=204)
def delete_controle(controle_id: int, db: Session = Depends(get_db)):
    controle = db.query(models.Controle).filter(models.Controle.id == controle_id).first()
    if not controle:
        raise HTTPException(status_code=404, detail="Contrôle non trouvé")
    db.delete(controle)
    db.commit()
    return