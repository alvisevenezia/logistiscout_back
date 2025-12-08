from .routes.v1 import menus
from fastapi import FastAPI, HTTPException, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, database
from .routes.v1 import tentes, evenements, reservations, controles, auth
from .routes.v2 import auth_v2, tents_v2, events_v2, controls_v2, menus_v2
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
V1_PREFIXES = (
    "/tentes",
    "/evenements",
    "/reservations",
    "/controles",
    "/menus",
)

@app.middleware("http")
async def block_v1_routes(request: Request, call_next):
    path = request.url.path

    # ✅ Always allow v2 + docs
    if (
        path.startswith("/v2")
        or path.startswith("/docs")
        or path.startswith("/openapi.json")
        or path.startswith("/redoc")
    ):
        return await call_next(request)

    # ❌ Block legacy v1 routes
    if path.startswith(V1_PREFIXES):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This API version is no longer supported. Please upgrade to v2.",
        )

    return await call_next(request)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info("🟢 Middleware actif : interception d'une requête")
    logging.info(f"➡️ {request.method} {request.url}")
    logging.info(f"Headers: {request.headers}")
    if request.method == "POST" or request.method == "PUT":
        body = await request.body()
        logging.info(f"Body: {body.decode('utf-8')}")
    else:
        logging.info("Pas de corps pour cette requête")
    response = await call_next(request)
    logging.info(f"⬅️ Réponse status: {response.status_code}")
    return response

# Include routers for all endpoints
app.include_router(auth_v2.router, prefix="/v2")
app.include_router(tents_v2.router, prefix="/v2")
app.include_router(events_v2.router, prefix="/v2")
app.include_router(controls_v2.router, prefix="/v2")
app.include_router(menus_v2.router, prefix="/v2")