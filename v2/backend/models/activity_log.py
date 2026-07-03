"""
models/activity_log.py — Activity logging model.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from models.user import Base


class ActivityLog(Base):
    """Records all user actions for admin monitoring."""

    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)