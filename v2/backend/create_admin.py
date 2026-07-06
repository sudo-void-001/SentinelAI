"""
create_admin.py — One-time script to create admin user and invite codes.
Run once: python create_admin.py
"""

import secrets
import getpass
from core.database import SessionLocal, init_db, engine
from core.security import hash_password
from models.user import Base, User
from models.invite import InviteCode


def create_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    existing = db.query(User).filter(User.role == "admin").first()
    if existing:
        print(f"✅ Admin already exists: {existing.username}")
        db.close()
        return

    print("─" * 40)
    print("  SentinelAI V2 — Admin Setup")
    print("─" * 40)

    username = input("Admin username (default: rajesh): ").strip() or "rajesh"
    email = input("Admin email: ").strip()
    password = getpass.getpass("Admin password (min 8 chars): ")

    if len(password) < 8:
        print("❌ Password too short. Minimum 8 characters.")
        db.close()
        return

    admin = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role="admin",
        is_active=True,
        digest_slot=9,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"\n✅ Admin created: {admin.username}")

    print("\n🎟 Invite codes for your friends:")
    print("─" * 40)
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
    print("\n─" * 40)
    print("✅ Setup complete. Save invite codes safely.")
    print("─" * 40)


if __name__ == "__main__":
    create_admin()