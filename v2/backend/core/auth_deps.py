"""
core/auth_deps.py — Authentication dependencies for FastAPI.

Provides get_current_user and require_admin functions
used as dependencies in protected routes.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import get_db
from core.security import decode_access_token
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Validate JWT token and return current user.

    Args:
        token: JWT token from request header.
        db: Database session.

    Returns:
        Current authenticated User object.

    Raises:
        HTTPException 401 if token invalid or user not found.
    """
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or disabled.",
        )

    # Check force logout
    if user.force_logout_at and datetime.utcnow() < user.force_logout_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have been logged out by admin.",
        )

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Require admin role for protected routes.

    Args:
        current_user: Current authenticated user.

    Returns:
        User if admin role confirmed.

    Raises:
        HTTPException 403 if user is not admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return current_user