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
