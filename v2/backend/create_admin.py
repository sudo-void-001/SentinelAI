"""
create_admin.py — One-time script to create admin user and first invite codes.

Run once: python create_admin.py
"""

from core.database import SessionLocal, init_db, engine
from core.security import hash_password
from models.user import Base, User
from models.invite import InviteCode
import secrets
import sys

def create_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if admin exists
    existing = db.query(User).filter(User.role == "admin").first()
    if existing:
        print(f"✅ Admin already exists: {existing.username}")
        db.close()
        return

    # Create admin
    admin = User(
        username="rajesh",
        email="rajeshpattan585@gmail.com",
        hashed_password=hash_password("admin123"),
        role="admin",
        is_active=True,
        digest_slot=9,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"✅ Admin created: {admin.username}")

    # Generate 10 invite codes
    print("\n🎟 Invite codes for your friends:")
    for i in range(10):
        code = secrets.token_urlsafe(8)
        invite = InviteCode(
            code=code,
            created_by=admin.id,
        )
        db.add(invite)
        print(f"  {i+1}. {code}")

    db.commit()
    db.close()
    print("\n✅ Save these codes. Share one with each friend.")

if __name__ == "__main__":
    create_admin()