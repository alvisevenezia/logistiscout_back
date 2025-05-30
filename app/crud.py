from sqlalchemy.orm import Session
from . import models, schemas

def get_tentes(db: Session, groupeId: str):
    return db.query(models.Tente).all()

def get_tente(db: Session, tente_id: int):
    return db.query(models.Tente).filter(models.Tente.id == tente_id).first()

def create_tente(db: Session, tente: schemas.TenteCreate):
    db_tente = models.Tente(**tente.dict())
    db.add(db_tente)
    db.commit()
    db.refresh(db_tente)
    return db_tente

def update_tente(db: Session, tente_id: int, tente: schemas.TenteUpdate):
    db_tente = get_tente(db, tente_id)
    if not db_tente:
        return None
    for key, value in tente.dict(exclude_unset=True).items():
        setattr(db_tente, key, value)
    db.commit()
    db.refresh(db_tente)
    return db_tente

def delete_tente(db: Session, tente_id: int):
    db_tente = get_tente(db, tente_id)
    if db_tente:
        db.delete(db_tente)
        db.commit()