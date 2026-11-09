"""
Module: auth_utils.py
Description: Authentication and role authorization utilities using Flask-JWT-Extended
             and Werkzeug password hashing.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User

def hash_password(password: str) -> str:
    """Hashes password with salted scrypt/pbkdf2."""
    return generate_password_hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verifies plain password against hash."""
    return check_password_hash(hashed, password)

def admin_required():
    """Decorator that enforces valid JWT with role='admin'."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role != "admin":
                return jsonify({
                    "error": "Forbidden",
                    "message": "Administrative privileges are required to access this resource."
                }), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def get_current_user():
    """Retrieves the current User entity from the active JWT token."""
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity) if isinstance(identity, (int, str)) and str(identity).isdigit() else None
            if user_id:
                return User.query.get(user_id)
    except Exception:
        pass
    return None
