import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Role, Permission
from werkzeug.security import generate_password_hash

# Load .env
load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@pharmacy.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # fallback if not set

app = create_app()
with app.app_context():
    # --- Create or get Admin role ---
    admin_role = Role.query.filter_by(name="Admin").first()
    if not admin_role:
        admin_role = Role(name="Admin", description="Administrator")
        db.session.add(admin_role)
        db.session.commit()
        print("Admin role created.")
    else:
        print("Admin role already exists.")

    # --- Create default permissions ---
    default_permissions = ["update_settings", "view_dashboard"]
    for perm_name in default_permissions:
        perm = Permission.query.filter_by(name=perm_name).first()
        if not perm:
            perm = Permission(name=perm_name)
            db.session.add(perm)
            db.session.commit()
            print(f"Permission '{perm_name}' created.")
        else:
            print(f"Permission '{perm_name}' already exists.")

        # Add permission to admin_role if not already linked
        if perm not in admin_role.permissions:
            admin_role.permissions.append(perm)
    db.session.commit()

    # --- Create admin user ---
    admin_user = User.query.filter_by(email=ADMIN_EMAIL).first()
    if not admin_user:
        admin_user = User(
            email=ADMIN_EMAIL,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            role_id=admin_role.id
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{ADMIN_EMAIL}' created.")
    else:
        print(f"Admin user '{ADMIN_EMAIL}' already exists.")
