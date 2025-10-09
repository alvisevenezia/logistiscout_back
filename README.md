# Logistiscout Back

Backend API for the Logistiscout mobile app, built with FastAPI and PostgreSQL.

---

## 🚀 Features

- RESTful API for tents, events, reservations, controls, and authentication
- PostgreSQL database support
- Pydantic models for validation
- Modular code structure
- Ready for deployment

---

## 🛠️ Requirements

- Python 3.12+
- PostgreSQL
- (Recommended) [WSL](https://learn.microsoft.com/en-us/windows/wsl/) or Linux

---

## ⚡ Quickstart

### 1. Clone the repository

```bash
git clone <repo-url>
cd logistiscout_back
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
or, if using `pyproject.toml`:
```bash
pip install .
```

### 4. Configure PostgreSQL

- Make sure PostgreSQL is running.
- Create a database and user if needed.
- Update `app/database.py` with your credentials:
  ```
  SQLALCHEMY_DATABASE_URL = "postgresql://<user>:<password>@localhost/logistiscout"
  ```

### 5. Initialize the database

```bash
python -m app.init_db
```

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📁 Project Structure

```
logistiscout_back/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── routes/
│   │   ├── tentes.py
│   │   ├── evenements.py
│   │   ├── reservations.py
│   │   ├── controles.py
│   │   └── auth.py
│   └── init_db.py
│
├── tests/
│   └── test_tentes.py
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 📚 API Documentation

Once the server is running, access the OpenAPI/Swagger docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🤝 Contributing

Pull requests and issues are welcome!

---

## 📝 License

MIT License

---

# Gestion des menus et planification des repas

## Concepts

- **Menu** : une recette générique (nom, description, ingrédients avec quantité par personne, instructions, type de repas)
- **EventMenu** : un menu planifié pour un événement, un jour et un type de repas (ex : déjeuner du 2025-10-12)

## Structure des données

### Menu
- `id` : int, auto
- `nom` : str
- `description` : str (optionnel)
- `ingredients` : List[dict] (ex : `[{'nom': 'pâtes', 'quantite': 100, 'unite': 'g'}]`)
- `instructions` : str (optionnel)
- `type_repas` : str (ex : 'déjeuner', 'dîner', ...)

### EventMenu
- `id` : int, auto
- `event_id` : int (id de l'événement)
- `menu_id` : int (id du menu/recette)
- `date` : date (jour du repas)
- `type_repas` : str
- `quantite_personnes` : int (optionnel, sinon nb_personnes de l'événement)

## Endpoints principaux

### Menus (recettes)
- `GET /menus` : liste tous les menus
- `POST /menus` : crée un menu (body = MenuCreate)
- `GET /menus/{menu_id}` : récupère un menu
- `PUT /menus/{menu_id}` : modifie un menu
- `DELETE /menus/{menu_id}` : supprime un menu

### EventMenus (planification)
- `GET /event_menus?event_id=...` : menus d'un événement
- `POST /event_menus` : planifie un menu pour un jour/repas
- `GET /event_menus/{event_menu_id}` : récupère un menu planifié
- `PUT /event_menus/{event_menu_id}` : modifie un menu planifié
- `DELETE /event_menus/{event_menu_id}` : supprime un menu planifié

## Exemple d'ingrédient dans une recette
```json
{
  "nom": "pâtes",
  "quantite": 100,
  "unite": "g"
}
```

## Bonnes pratiques
- Crée d'abord les recettes dans `/menus`.
- Planifie les repas d'un événement avec `/event_menus`.
- Pour calculer les quantités totales, multiplie chaque `quantite` d'ingrédient par le nombre de personnes de l'événement.
- Les validations côté API garantissent que chaque ingrédient a bien `nom`, `quantite`, `unite`.

## Pour aller plus loin
- Ajouter un endpoint pour calculer automatiquement la liste de courses d'un événement.
- Ajouter des tags/allergènes sur les menus.
- Gérer les quantités spécifiques par repas ou par groupe.
