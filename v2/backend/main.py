"""
main.py — Entry point for SentinelAI V2 FastAPI backend.
Run with: python -m uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.config import APP_NAME, APP_VERSION
from core.database import init_db, engine
from models.user import Base, User
from models.activity_log import ActivityLog
from models.digest_slot import DigestSlot
from models.invite import InviteCode
from routers import auth, admin, slots, dashboard
import secrets as sec


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and start scheduler on startup."""
    Base.metadata.create_all(bind=engine)
    init_db()

    from core.scheduler_v2 import start_v2_scheduler
    scheduler = start_v2_scheduler()

    print(f"✅ {APP_NAME} v{APP_VERSION} started")
    print("✅ Database initialized")
    print("✅ Email scheduler running")

    yield

    scheduler.shutdown()
    print("✅ Scheduler stopped")


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="SentinelAI V2 — Multi-user Cyber Threat Intelligence Platform",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "https://sentinelai-frontend.onrender.com",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(slots.router)
app.include_router(dashboard.router)


@app.get("/")
async def root():
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "connected",
    }


@app.post("/setup/init-admin")
async def init_admin(secret: str):
    """
    One-time admin setup route.
    Remove this route after first use.
    """
    if secret != "sentinelai-setup-2026":
        raise HTTPException(status_code=403, detail="Invalid setup key.")

    from core.database import SessionLocal
    from core.security import hash_password

    db = SessionLocal()

    existing = db.query(User).filter(User.role == "admin").first()
    if existing:
        db.close()
        return {"message": "Admin already exists.", "username": existing.username}

    admin_user = User(
        username="rajesh",
        email="rajeshpattan585@gmail.com",
        hashed_password=hash_password("SentinelAI@2026"),
        role="admin",
        is_active=True,
        digest_slot=9,
        notify_email=True,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    codes = []
    for i in range(10):
        code = sec.token_urlsafe(8)
        invite = InviteCode(code=code, created_by=admin_user.id)
        db.add(invite)
        codes.append(code)

    db.commit()
    db.close()

    return {
        "message": "Admin created successfully.",
        "username": "rajesh",
        "password": "SentinelAI@2026",
        "invite_codes": codes,
    }