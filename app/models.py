from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app # Needed for logger access in check_password
from .extensions import db # Assumed to be your Flask-SQLAlchemy instance

# NOTE: The 'current_app' import in your provided code was slightly misplaced
# with the 'werkzeug.security' imports. It is usually imported from 'flask'.

#===============================
# 1. Mixins
#===============================

class TimestampMixin:
    """Adds created_at and updated_at fields to models."""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    """Adds soft delete functionality."""
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def soft_delete(self):
        """Marks the record as deleted without removing it from the database."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        db.session.add(self)

    def restore(self):
        """Restores a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        db.session.add(self)

#===============================
# 2. Association Table (Many-to-Many)
#===============================

# Association table for the many-to-many relationship between Role and Permission
role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True)
)


#===============================
# 3. Models
#===============================

class Role(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

    # Many-to-Many relationship with Permission
    permissions = db.relationship(
        "Permission",
        secondary=role_permissions,
        backref=db.backref("roles", lazy="dynamic"),
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Role {self.name}>"

class Permission(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Permission {self.name}>"

class User(db.Model, UserMixin, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    # Foreign Keys
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Relationships
    role = db.relationship("Role", backref=db.backref("users", lazy=True))
    # Self-referential relationship (one user creates many users)
    creator = db.relationship("User", remote_side=[id], backref=db.backref("created_users", lazy=True))

    def set_password(self, password):
        """Generates a password hash using Werkzeug's current default algorithm."""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """
        Verify a password against the stored hash and automatically upgrade 
        legacy hashes to the current standard (e.g., PBKDF2) upon successful login.
        """
        if self.password_hash is None:
            return False

        try:
            valid = check_password_hash(self.password_hash, password)
            
            if valid:
                # Security: Check for Hash Upgrade Requirement
                if not self.password_hash.startswith("pbkdf2:"):
                    self.password_hash = generate_password_hash(password)
                    
                    # NOTE: Assuming 'db' import is resolvable from the application context
                    from app import db # Local import required if 'db' is not global
                    db.session.commit()
                    current_app.logger.info(f"Upgraded password hash to PBKDF2 for user {self.email}")
            
            return valid
        
        except ValueError as e:
            current_app.logger.warning(f"Password check failed due to hash format error for user {self.email}: {e}")
            return False
            
    def __repr__(self):
        return f"<User {self.email}>"

class AuditLog(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45))
    object_type = db.Column(db.String(50), nullable=True) # e.g., 'User', 'Role', 'Product'
    object_id = db.Column(db.Integer, nullable=True)

    user = db.relationship("User", backref=db.backref("audit_logs", lazy=True))

    def __repr__(self):
        return f"<AuditLog {self.action} by User {self.user_id}>"

class CompanySettings(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "company_settings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    short_name = db.Column(db.String(50))
    logo = db.Column(db.String(255))
    address = db.Column(db.String(255))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    website = db.Column(db.String(120))

    def __repr__(self):
        return f"<CompanySettings {self.name}>"