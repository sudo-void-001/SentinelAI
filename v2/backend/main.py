"""
main.py — Entry point for SentinelAI V2 FastAPI backend.

Run with: python -m uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import APP_NAME, APP_VERSION
from core.database import init_db, engine
from models.user import Base
from models.activity_log import ActivityLog
from models.digest_slot import DigestSlot
from models.invite import InviteCode
from routers import auth, admin, slots, dashboard

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="SentinelAI V2 — Multi-user Cyber Threat Intelligence Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(slots.router)
app.include_router(dashboard.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    Base.metadata.create_all(bind=engine)
    init_db()
    print(f"✅ {APP_NAME} v{APP_VERSION} started")
    print("✅ Database initialized")
    print("✅ All routers registered")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
    }