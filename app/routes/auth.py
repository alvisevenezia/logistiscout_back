from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/auth/login")
def login(groupe_id: str, groupe_mdp: str):
    # À compléter : vérification du groupe et du mot de passe
    if groupe_id == "demo" and groupe_mdp == "demo":
        return {"token": "fake-token"}
    raise HTTPException(status_code=401, detail="Identifiants invalides")