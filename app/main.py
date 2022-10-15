from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import global_init
from app.routers import stone, frame

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # WARN: development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stone.router, prefix="/stone", tags=["stones"])
app.include_router(frame.router, prefix="/frame", tags=["frames"])


@app.on_event("startup")
async def init_database_on_startup():
    global_init()


@app.get("/")
async def healthcheck_index():
    return {"success": True}
