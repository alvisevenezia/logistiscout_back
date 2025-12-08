from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# Groupe schemas
class GroupeBase(BaseModel):
    userlogin: str
    mdp: str
    nom: str
    membres: Optional[List[str]] = None
    email: Optional[str] = None

class GroupeCreate(GroupeBase):
    pass

class GroupeUpdate(GroupeBase):
    pass

class Groupe(GroupeBase):
    id: int
    class Config:
        from_attributes = True

# Tente schemas
class TenteBase(BaseModel):
    nom: str
    etat: str
    remarques: Optional[str]
    nbPlaces: Optional[int]
    typeTente: Optional[str]
    unitePreferee: Optional[str]
    couleurs: Optional[List[str]] = None
    groupeId: int
    estIntegree: bool = False

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
    date: datetime
    dateFin: datetime
    tentesAssociees: Optional[List[int]] = None
    unites: Optional[List[int]] = None
    groupeId: int
    

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

# Menu schemas adaptés à la structure Recipe Flutter
class MenuBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    category: Optional[str] = None
    ingredients: Optional[List[dict]] = None  # [{nom, quantite, unite}]
    allergens: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuBase):
    pass

class Menu(MenuBase):
    id: int
    class Config:
        from_attributes = True

# EventMenu schemas
class EventMenuBase(BaseModel):
    event_id: int
    menu_id: int
    date: date
    type_repas: str
    quantite_personnes: Optional[int] = None

class EventMenuCreate(EventMenuBase):
    pass

class EventMenuUpdate(EventMenuBase):
    pass

class EventMenu(EventMenuBase):
    id: int
    class Config:
        from_attributes = True