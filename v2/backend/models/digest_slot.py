"""
models/digest_slot.py — Digest time slot management.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from models.user import Base


class DigestSlot(Base):
    """Represents an available digest delivery time slot."""

    __tablename__ = "digest_slots"

    id = Column(Integer, primary_key=True, index=True)
    hour = Column(Integer, nullable=False)
    label = Column(String, nullable=False)
    is_reserved = Column(Boolean, default=False)
    reserved_by_user_id = Column(
        Integer, ForeignKey("users.id"), unique=True, nullable=True
    )
    is_admin_slot = Column(Boolean, default=False)