from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud, database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tentes", response_model=List[schemas.Tente])
def list_tentes(groupeId: str = Query(...), db: Session = Depends(get_db)):
    return crud.get_tentes(db, groupeId)

@app.post("/tentes", response_model=schemas.Tente, status_code=201)
def create_tente(tente: schemas.TenteCreate, db: Session = Depends(get_db)):
    return crud.create_tente(db, tente)

@app.get("/tentes/{tente_id}", response_model=schemas.Tente)
def get_tente(tente_id: int, db: Session = Depends(get_db)):
    tente = crud.get_tente(db, tente_id)
    if not tente:
        raise HTTPException(status_code=404, detail="Tente not found")
    return tente

@app.put("/tentes/{tente_id}", response_model=schemas.Tente)
def update_tente(tente_id: int, tente: schemas.TenteUpdate, db: Session = Depends(get_db)):
    return crud.update_tente(db, tente_id, tente)

@app.delete("/tentes/{tente_id}", status_code=204)
def delete_tente(tente_id: int, db: Session = Depends(get_db)):
    crud.delete_tente(db, tente_id)
    return