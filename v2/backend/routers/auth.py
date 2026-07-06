"""
routers/auth.py — Authentication routes for SentinelAI V2.
Handles user registration, login, and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from core.database import get_db
from core.security import hash_password, verify_password, create_access_token
from models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ─── REQUEST SCHEMAS ──────────────────────────────

class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    invite_code: str = Field(min_length=6, max_length=20)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=1, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str


# ─── ROUTES ───────────────────────────────────────

@router.post("/signup", response_model=TokenResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Register a new user with an invite code.

    Args:
        request: Signup form data including invite code.
        db: Database session.

    Returns:
        JWT token and user info on success.

    Raises:
        HTTPException 400 if username/email taken or invite invalid.
    """
    from models.invite import InviteCode

    invite = db.query(InviteCode).filter(
        InviteCode.code == request.invite_code,
        InviteCode.is_used == False
    ).first()

    if not invite:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired invite code."
        )

    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username already taken."
        )

    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    user = User(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password),
        role="user",
    )
    db.add(user)
    db.flush()

    invite.is_used = True
    invite.used_by = user.id
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.username, "role": user.role})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        role=user.role,
        username=user.username,
    )


@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with username and password.

    Args:
        login_data: Login credentials.
        db: Database session.

    Returns:
        JWT token and user info on success.

    Raises:
        HTTPException 401 if credentials invalid or account disabled.
    """
    user = db.query(User).filter(User.username == login_data.username).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account has been disabled. Contact admin."
        )

    user.last_active = datetime.utcnow()
    db.commit()

    token = create_access_token({"sub": user.username, "role": user.role})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        role=user.role,
        username=user.username,
    )