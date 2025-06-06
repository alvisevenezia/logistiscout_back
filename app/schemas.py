from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# Groupe schemas
class GroupeBase(BaseModel):
    nom: str
    membres: Optional[List[str]] = None

class GroupeCreate(GroupeBase):
    pass

class GroupeUpdate(GroupeBase):
    pass

class Groupe(GroupeBase):
    id: str
    class Config:
        from_attributes = True

# Tente schemas
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
        from_attributes = True

# Evenement schemas
class EvenementBase(BaseModel):
    nom: str
    type: str
    date: date
    dateFin: date
    tentesAssociees: Optional[List[int]] = None

class EvenementCreate(EvenementBase):
    pass

class EvenementUpdate(EvenementBase):
    pass

class Evenement(EvenementBase):
    id: int
    class Config:
        from_attributes = True

# Reservation schemas
class ReservationBase(BaseModel):
    tenteId: int
    evenementId: int
    debut: date
    fin: date

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    class Config:
        from_attributes = True

# Controle schemas
class ControleBase(BaseModel):
    tenteId: int
    userId: int
    date: datetime
    checklist: dict
    remarques: Optional[str]

class ControleCreate(ControleBase):
    pass

class ControleUpdate(ControleBase):
    pass

class Controle(ControleBase):
    id: int
    class Config:
        from_attributes = True