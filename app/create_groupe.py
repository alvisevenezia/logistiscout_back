import argparse
from app.database import SessionLocal
from app.models import Groupe

def main():
    parser = argparse.ArgumentParser(description="Créer un groupe dans la base de données.")
    parser.add_argument("--id", required=True, help="ID du groupe (unique)")
    parser.add_argument("--nom", required=True, help="Nom du groupe")
    parser.add_argument("--mdp", required=True, help="Mot de passe du groupe")
    parser.add_argument("--membres", nargs="*", default=[], help="Liste des membres (séparés par un espace)")
    args = parser.parse_args()

    db = SessionLocal()
    if db.query(Groupe).filter(Groupe.id == args.id).first():
        print(f"Groupe avec id '{args.id}' existe déjà.")
        return
    groupe = Groupe(id=args.id, nom=args.nom, mdp=args.mdp, membres=args.membres)
    db.add(groupe)
    db.commit()
    print(f"Groupe '{args.nom}' créé avec succès !")
    db.close()

if __name__ == "__main__":
    main()
