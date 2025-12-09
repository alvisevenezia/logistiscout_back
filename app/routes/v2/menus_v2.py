# app/routes/v2/event_menus_v2.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/menus", response_model=List[schemas.Menu])
def list_menus(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()

@router.post("/menus", response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    # Validation ingrédients (doit être une liste de dicts avec nom, quantite, unite)
    if menu.ingredients:
        for ing in menu.ingredients:
            if not all(k in ing for k in ("nom", "quantite", "unite")):
                raise HTTPException(status_code=400, detail="Chaque ingrédient doit avoir nom, quantite, unite")
    db_menu = models.Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.get("/menus/{menu_id}", response_model=schemas.Menu)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return menu

@router.put("/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(menu_id: int, menu: schemas.MenuUpdate, db: Session = Depends(get_db)):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    if menu.ingredients:
        for ing in menu.ingredients:
            if not all(k in ing for k in ("nom", "quantite", "unite")):
                raise HTTPException(status_code=400, detail="Chaque ingrédient doit avoir nom, quantite, unite")
    for key, value in menu.dict(exclude_unset=True).items():
        setattr(db_menu, key, value)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.delete("/menus/{menu_id}", status_code=204)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    db.delete(menu)
    db.commit()
    return

@router.get("/event_menus", response_model=List[schemas.EventMenu])
def list_event_menus(
    event_id: int = Query(...),
    day_number: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Retourne les EventMenu pour un événement donné,
    optionnellement filtrés par numéro de jour.
    """
    query = db.query(models.EventMenu).filter(models.EventMenu.event_id == event_id)

    if day_number is not None:
        query = query.filter(models.EventMenu.day_number == day_number)

    return query.all()

@router.post("/event_menus", response_model=schemas.EventMenu, status_code=201)
def create_event_menu(
    event_menu: schemas.EventMenuCreate,
    db: Session = Depends(get_db),
):
    db_event_menu = models.EventMenu(**event_menu.dict())
    db.add(db_event_menu)
    db.commit()
    db.refresh(db_event_menu)
    return db_event_menu

@router.get("/event_menus/{event_menu_id}", response_model=schemas.EventMenu)
def get_event_menu(event_menu_id: int, db: Session = Depends(get_db)):
    event_menu = (
        db.query(models.EventMenu)
        .filter(models.EventMenu.id == event_menu_id)
        .first()
    )
    if not event_menu:
        raise HTTPException(status_code=404, detail="EventMenu non trouvé")
    return event_menu

@router.put("/event_menus/{event_menu_id}", response_model=schemas.EventMenu)
def update_event_menu(
    event_menu_id: int,
    event_menu: schemas.EventMenuUpdate,
    db: Session = Depends(get_db),
):
    db_event_menu = (
        db.query(models.EventMenu)
        .filter(models.EventMenu.id == event_menu_id)
        .first()
    )
    if not db_event_menu:
        raise HTTPException(status_code=404, detail="EventMenu non trouvé")

    for key, value in event_menu.dict(exclude_unset=True).items():
        setattr(db_event_menu, key, value)

    db.commit()
    db.refresh(db_event_menu)
    return db_event_menu

@router.delete("/event_menus/{event_menu_id}", status_code=204)
def delete_event_menu(event_menu_id: int, db: Session = Depends(get_db)):
    event_menu = (
        db.query(models.EventMenu)
        .filter(models.EventMenu.id == event_menu_id)
        .first()
    )
    if not event_menu:
        raise HTTPException(status_code=404, detail="EventMenu non trouvé")
    db.delete(event_menu)
    db.commit()
    return
