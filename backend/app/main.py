from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, interfaces, networks, virtual_machines
from app.database.init_db import init_db


app = FastAPI(
    title="VM Control Test Task API",
    description="Backend for a junior fullstack test task.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(virtual_machines.router)
app.include_router(interfaces.router)
app.include_router(networks.router)


@app.on_event("startup")
async def on_startup() -> None:
    # Подготавливает схему БД и стартовые данные перед приемом запросов.
    await init_db()


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    # Нужен для быстрой проверки, что API поднят и отвечает.
    return {"status": "ok"}
