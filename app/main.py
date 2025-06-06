from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, database
from .routes import tentes, evenements, reservations, controles, auth
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info("🟢 Middleware actif : interception d'une requête")
    logging.info(f"➡️ {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"⬅️ Réponse status: {response.status_code}")
    return response

# Include routers for all endpoints
app.include_router(auth.router)
app.include_router(tentes.router)
app.include_router(evenements.router)
app.include_router(reservations.router)
app.include_router(controles.router)