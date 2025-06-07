from sqlalchemy import Column, Integer, String, Date, DateTime, Text, JSON, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base

class Tente(Base):
    __tablename__ = "tentes"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    uniteId = Column(Integer)
    etat = Column(String)
    remarques = Column(Text)
    nbPlaces = Column(Integer)
    typeTente = Column(String)
    unitePreferee = Column(String)
    couleurs = Column(ARRAY(String))
    groupeId = Column(String)
    estIntegree = Column(Boolean, default=False)  # 0 = False, 1 = True

class Evenement(Base):
    __tablename__ = "evenements"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    date = Column(DateTime)
    dateFin = Column(DateTime)
    type = Column(String)
    tentesAssociees = Column(ARRAY(Integer))
    unites = Column(ARRAY(Integer))
    groupeId = Column(String)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    tenteId = Column(Integer)
    evenementId = Column(Integer)
    debut = Column(Date)
    fin = Column(Date)

class Controle(Base):
    __tablename__ = "controles"
    id = Column(Integer, primary_key=True, index=True)
    tenteId = Column(Integer)
    userId = Column(Integer)
    date = Column(DateTime)
    checklist = Column(JSON)
    remarques = Column(Text)

class Groupe(Base):
    __tablename__ = "groupes"
    id = Column(String, primary_key=True, index=True)
    nom = Column(String)
    membres = Column(ARRAY(String))
    mdp = Column(String)  # mot de passe du groupe