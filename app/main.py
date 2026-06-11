from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.quests import router as quests_router
from app.api.rewards import router as rewards_router
from app.api.users import router as users_router
from app.core.database import Base, engine

# Buat tabel database jika belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Questify API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(quests_router, prefix="/api/quests", tags=["quests"])
app.include_router(rewards_router, prefix="/api/rewards", tags=["rewards"])


@app.get("/")
def root():
    return {"message": "Welcome to Questify API"}
