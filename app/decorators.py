from functools import wraps
from flask import abort
from flask_login import current_user

def permission_required(permission_name):
    """Require a specific permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if not current_user.role or permission_name not in [p.name for p in current_user.role.permissions]:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(allowed_roles):
    """Require the user to have one of the allowed roles."""
    if not isinstance(allowed_roles, (list, tuple, set)):
        allowed_roles = [allowed_roles]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            # Compare role name strings
            user_role_name = getattr(current_user.role, 'name', None)
            if user_role_name not in allowed_roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
