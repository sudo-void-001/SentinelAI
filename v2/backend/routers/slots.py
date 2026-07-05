"""
routers/slots.py — Digest slot management for SentinelAI V2.

Handles unique time slot selection per user.
Admin slot is permanently reserved and cannot be selected.
No two users can share the same slot.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.auth_deps import get_current_user, require_admin
from models.user import User

router = APIRouter(prefix="/slots", tags=["Digest Slots"])

# All available slots in IST
ALL_SLOTS = [
    {"hour": 6,  "label": "6:00 AM"},
    {"hour": 7,  "label": "7:00 AM"},
    {"hour": 8,  "label": "8:00 AM"},
    {"hour": 9,  "label": "9:00 AM"},
    {"hour": 10, "label": "10:00 AM"},
    {"hour": 11, "label": "11:00 AM"},
    {"hour": 12, "label": "12:00 PM"},
]

ADMIN_SLOT = 9  # Admin permanently owns 9 AM


@router.get("/available")
def get_available_slots(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of available (unreserved) digest slots.

    Admin slot is always excluded from available list.
    Current user's own slot is shown as 'yours'.

    Returns:
        List of slot dicts with availability status.
    """
    reserved_slots = db.query(User.digest_slot)\
                       .filter(User.digest_slot != None)\
                       .all()
    reserved_hours = {r[0] for r in reserved_slots}

    result = []
    for slot in ALL_SLOTS:
        hour = slot["hour"]
        if hour == ADMIN_SLOT and current_user.role != "admin":
            continue  # Hide admin slot from users
        result.append({
            "hour": hour,
            "label": slot["label"],
            "available": hour not in reserved_hours or hour == current_user.digest_slot,
            "is_yours": hour == current_user.digest_slot,
            "is_admin_slot": hour == ADMIN_SLOT,
        })

    return result


@router.post("/select/{hour}")
def select_slot(
    hour: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Select a digest time slot.

    Enforces uniqueness at database level with transaction lock.
    Admin slot cannot be selected by regular users.

    Args:
        hour: Hour (IST) to select (6-12).

    Raises:
        HTTPException 400 if slot taken or invalid.
    """
    if hour not in [s["hour"] for s in ALL_SLOTS]:
        raise HTTPException(status_code=400, detail="Invalid slot hour.")

    if hour == ADMIN_SLOT and current_user.role != "admin":
        raise HTTPException(
            status_code=400,
            detail="This slot is reserved for admin."
        )

    # Check if slot is taken by another user (with lock)
    existing = db.query(User)\
                 .filter(User.digest_slot == hour)\
                 .filter(User.id != current_user.id)\
                 .with_for_update()\
                 .first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="This slot is already taken. Please choose another."
        )

    old_slot = current_user.digest_slot
    current_user.digest_slot = hour
    db.commit()

    return {
        "message": f"Digest slot set to {hour}:00 IST.",
        "previous_slot": old_slot,
        "new_slot": hour,
    }


@router.delete("/remove")
def remove_slot(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove current user's digest slot reservation.

    Returns:
        Confirmation message.
    """
    if current_user.role == "admin":
        raise HTTPException(
            status_code=400,
            detail="Admin slot cannot be removed."
        )

    current_user.digest_slot = None
    db.commit()
    return {"message": "Digest slot removed."}