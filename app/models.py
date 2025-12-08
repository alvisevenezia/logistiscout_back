from sqlalchemy import Column, Integer, String, Date, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base

class Tente(Base):
    __tablename__ = "tentes"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    etat = Column(String)
    remarques = Column(Text)
    nbPlaces = Column(Integer)
    typeTente = Column(String)
    unitePreferee = Column(String)
    couleurs = Column(ARRAY(String))
    groupeId = Column(Integer, ForeignKey("groupes.id"), index=True)
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
    groupeId = Column(Integer, ForeignKey("groupes.id"), index=True)

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
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # id auto-incrémenté
    userlogin = Column(String, unique=True, nullable=False)  # identifiant de connexion du groupe
    mdp = Column(String, nullable=False)  # mot de passe du groupe
    nom = Column(String, nullable=False)  # nom du groupe
    email = Column(String, unique=True, nullable=True)  # email du groupe
    membres = Column(ARRAY(String))  # optionnel, liste des membres

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # anciennement nom
    description = Column(Text)  # court
    instructions = Column(Text)  # texte complet de préparation
    category = Column(String)  # ex: 'plat', 'dessert', etc.
    ingredients = Column(JSON)  # [{"nom": ..., "quantite": ..., "unite": ...}]
    allergens = Column(ARRAY(String))  # set d'allergènes
    tags = Column(ARRAY(String))  # set de tags

class EventMenu(Base):
    __tablename__ = "event_menus"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("evenements.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    date = Column(Date, nullable=False)
    type_repas = Column(String, nullable=False)
    quantite_personnes = Column(Integer)  # optionnel, pour override