from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import actions, health, incidents, telemetry
from app.database.db import init_db

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield

app = FastAPI(title="Agentic Shadow", version="0.1.0", lifespan=lifespan)
for router in (health.router, telemetry.router, incidents.router, actions.router): app.include_router(router)
