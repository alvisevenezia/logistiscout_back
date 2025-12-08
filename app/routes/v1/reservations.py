from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/reservations", response_model=List[schemas.Reservation])
def list_reservations(tenteId: Optional[int] = Query(None), evenementId: Optional[int] = Query(None), groupeId: str = Query(...), db: Session = Depends(get_db)):
    query = db.query(models.Reservation)
    if tenteId is not None:
        query = query.filter(models.Reservation.tenteId == tenteId)
    if evenementId is not None:
        query = query.filter(models.Reservation.evenementId == evenementId)
    # Filtre par groupeId via la tente liée
    query = query.join(models.Tente, models.Reservation.tenteId == models.Tente.id).filter(models.Tente.groupeId == groupeId)
    return query.all()

@router.post("/reservations", response_model=schemas.Reservation, status_code=201)
def create_reservation(reservation: schemas.ReservationCreate, groupeId: str = Query(...), db: Session = Depends(get_db)):
    # Vérifie que la tente appartient bien au groupe
    tente = db.query(models.Tente).filter(models.Tente.id == reservation.tenteId, models.Tente.groupeId == groupeId).first()
    if not tente:
        raise HTTPException(status_code=403, detail="Tente non trouvée ou n'appartient pas à ce groupe")
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.get("/reservations/{reservation_id}", response_model=schemas.Reservation)
def get_reservation(reservation_id: int, groupeId: str = Query(...), db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).join(models.Tente, models.Reservation.tenteId == models.Tente.id).filter(models.Reservation.id == reservation_id, models.Tente.groupeId == groupeId).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée ou accès refusé")
    return reservation

@router.put("/reservations/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: int, reservation: schemas.ReservationUpdate, groupeId: str = Query(...), db: Session = Depends(get_db)):
    db_reservation = db.query(models.Reservation).join(models.Tente, models.Reservation.tenteId == models.Tente.id).filter(models.Reservation.id == reservation_id, models.Tente.groupeId == groupeId).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée ou accès refusé")
    for key, value in reservation.dict(exclude_unset=True).items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.delete("/reservations/{reservation_id}", status_code=204)
def delete_reservation(reservation_id: int, groupeId: str = Query(...), db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).join(models.Tente, models.Reservation.tenteId == models.Tente.id).filter(models.Reservation.id == reservation_id, models.Tente.groupeId == groupeId).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée ou accès refusé")
    db.delete(reservation)
    db.commit()
    return