from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class TenteBase(BaseModel):
    nom: str
    uniteId: Optional[int]
    etat: str
    remarques: Optional[str]
    nbPlaces: Optional[int]
    typeTente: Optional[str]
    unitePreferee: Optional[str]

class TenteCreate(TenteBase):
    pass

class TenteUpdate(TenteBase):
    pass

class Tente(TenteBase):
    id: int
    class Config:
        orm_mode = True