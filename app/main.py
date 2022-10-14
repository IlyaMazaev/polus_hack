from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import global_init
from app.routers import auth, profile, project, yandex, industry, vacancy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # WARN: development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(project.router, prefix="/project", tags=["project"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(yandex.router, prefix="/yandex", tags=["oauth", "yandex"])
app.include_router(industry.router, prefix="/industry", tags=["industry"])
app.include_router(vacancy.router, prefix="/vacancy", tags=["vacancy"])


@app.on_event("startup")
async def init_database_on_startup():
    global_init()


@app.get("/")
async def healthcheck_index():
    return {"success": True}
