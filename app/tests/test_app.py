from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_tente():
    response = client.post("/tentes", json={
        "nom": "Tente Test",
        "uniteId": 1,
        "etat": "neuve",
        "remarques": "Aucune",
        "nbPlaces": 4,
        "typeTente": "dôme",
        "unitePreferee": "A",
        "couleurs": ["bleu", "vert"],
        "groupeId": "groupe-test"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == "Tente Test"
    assert data["etat"] == "neuve"
    assert data["couleurs"] == ["bleu", "vert"]
    assert data["groupeId"] == "groupe-test"

def test_list_tentes():
    response = client.get("/tentes", params={"groupeId": "test"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tente_not_found():
    response = client.get("/tentes/99999")
    assert response.status_code == 404

def test_update_tente():
    # Crée une tente d'abord
    create_resp = client.post("/tentes", json={
        "nom": "Tente Update",
        "uniteId": 2,
        "etat": "usée",
        "remarques": "",
        "nbPlaces": 2,
        "typeTente": "tunnel",
        "unitePreferee": "B",
        "couleurs": ["rouge"],
        "groupeId": "groupe-update"
    })
    tente_id = create_resp.json()["id"]
    # Met à jour la tente
    update_resp = client.put(f"/tentes/{tente_id}", json={
        "nom": "Tente Modifiée",
        "uniteId": 2,
        "etat": "réparée",
        "remarques": "Réparée récemment",
        "nbPlaces": 2,
        "typeTente": "tunnel",
        "unitePreferee": "B",
        "couleurs": ["jaune", "bleu"],
        "groupeId": "groupe-update"
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["nom"] == "Tente Modifiée"
    assert update_resp.json()["couleurs"] == ["jaune", "bleu"]
    assert update_resp.json()["groupeId"] == "groupe-update"

def test_delete_tente():
    # Crée une tente à supprimer
    create_resp = client.post("/tentes", json={
        "nom": "Tente Delete",
        "uniteId": 3,
        "etat": "bonne",
        "remarques": "",
        "nbPlaces": 3,
        "typeTente": "igloo",
        "unitePreferee": "C",
        "couleurs": ["noir"],
        "groupeId": "groupe-delete"
    })
    tente_id = create_resp.json()["id"]
    delete_resp = client.delete(f"/tentes/{tente_id}")
    assert delete_resp.status_code == 204
    # Vérifie qu'elle n'existe plus
    get_resp = client.get(f"/tentes/{tente_id}")
    assert get_resp.status_code == 404