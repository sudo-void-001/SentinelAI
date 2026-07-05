"""
routers/admin.py — Admin-only routes for SentinelAI V2.

All routes require admin role.
Handles user management and activity monitoring.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from core.database import get_db
from core.auth_deps import require_admin
from models.user import User
from models.activity_log import ActivityLog
from models.invite import InviteCode
from pydantic import BaseModel
import secrets

router = APIRouter(prefix="/admin", tags=["Admin"])


# ─── RESPONSE SCHEMAS ─────────────────────────────

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    digest_slot: int | None
    created_at: datetime
    last_active: datetime | None

    class Config:
        from_attributes = True


class ActivityResponse(BaseModel):
    id: int
    user_id: int
    action: str
    ip_address: str | None
    timestamp: datetime

    class Config:
        from_attributes = True


# ─── USER MANAGEMENT ──────────────────────────────

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Get all registered users.

    Returns:
        List of all users with their details.
    """
    return db.query(User).all()


@router.post("/users/{user_id}/disable")
def disable_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Disable a user account.

    Args:
        user_id: ID of user to disable.

    Raises:
        HTTPException 404 if user not found.
        HTTPException 400 if trying to disable admin.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot disable admin.")

    user.is_active = False
    user.force_logout_at = datetime.utcnow() + timedelta(seconds=1)

    log = ActivityLog(
        user_id=admin.id,
        action=f"Disabled user: {user.username}",
    )
    db.add(log)
    db.commit()
    return {"message": f"User {user.username} disabled."}


@router.post("/users/{user_id}/enable")
def enable_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Re-enable a disabled user account.

    Args:
        user_id: ID of user to enable.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.is_active = True
    user.force_logout_at = None

    log = ActivityLog(
        user_id=admin.id,
        action=f"Enabled user: {user.username}",
    )
    db.add(log)
    db.commit()
    return {"message": f"User {user.username} enabled."}


@router.post("/users/{user_id}/force-logout")
def force_logout(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Force logout a user by invalidating their session.

    Args:
        user_id: ID of user to force logout.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.force_logout_at = datetime.utcnow() + timedelta(seconds=1)

    log = ActivityLog(
        user_id=admin.id,
        action=f"Force logged out: {user.username}",
    )
    db.add(log)
    db.commit()
    return {"message": f"User {user.username} force logged out."}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Permanently delete a user account.

    Args:
        user_id: ID of user to delete.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete admin.")

    username = user.username
    db.delete(user)

    log = ActivityLog(
        user_id=admin.id,
        action=f"Deleted user: {username}",
    )
    db.add(log)
    db.commit()
    return {"message": f"User {username} permanently deleted."}


# ─── ACTIVITY LOGS ────────────────────────────────

@router.get("/activity-logs", response_model=List[ActivityResponse])
def get_activity_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Get recent activity logs.

    Args:
        limit: Number of logs to return (default 50).

    Returns:
        List of activity log entries.
    """
    return db.query(ActivityLog)\
             .order_by(ActivityLog.timestamp.desc())\
             .limit(limit)\
             .all()


# ─── INVITE MANAGEMENT ────────────────────────────

@router.post("/invites/create")
def create_invite(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Generate a new invite code.

    Returns:
        New invite code string.
    """
    code = secrets.token_urlsafe(8)
    invite = InviteCode(
        code=code,
        created_by=admin.id,
    )
    db.add(invite)
    db.commit()
    return {"invite_code": code}


@router.get("/invites")
def get_invites(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Get all invite codes and their status.

    Returns:
        List of all invite codes.
    """
    invites = db.query(InviteCode).all()
    return [
        {
            "code": i.code,
            "is_used": i.is_used,
            "used_by": i.used_by,
            "created_at": i.created_at,
        }
        for i in invites
    ]


# ─── SYSTEM STATS ─────────────────────────────────

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Get platform statistics for admin dashboard.

    Returns:
        Dict with user counts and system status.
    """
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_invites = db.query(InviteCode).count()
    used_invites = db.query(InviteCode).filter(InviteCode.is_used == True).count()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "max_users": 10,
        "slots_remaining": 10 - total_users,
        "total_invites": total_invites,
        "used_invites": used_invites,
        "available_invites": total_invites - used_invites,
        "system_status": "online",
    }