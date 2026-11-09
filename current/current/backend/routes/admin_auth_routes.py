"""
Routes: admin_auth_routes.py
Description: Dedicated administrator authentication with secret enrollment authorization.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from backend.config import Config
from backend.models import db, User, Admin, AdminLog
from backend.utils.auth_utils import hash_password, verify_password

admin_auth_bp = Blueprint("admin_auth", __name__, url_prefix="/api/admin/auth")

@admin_auth_bp.route("/register", methods=["POST"])
def admin_register():
    data = request.get_json() or {}
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    username = data.get("username", "").strip() or None
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    admin_secret = data.get("admin_secret", "")

    # Security check: Admin enrollment is strictly protected by server secret
    if not admin_secret or admin_secret != Config.ADMIN_REGISTRATION_SECRET:
        return jsonify({
            "error": "Forbidden",
            "message": "Invalid administrator enrollment secret code. Unauthorized administrator creation is prohibited."
        }), 403

    if not full_name or not email or not password:
        return jsonify({"error": "Full Name, Email, and Password are required."}), 400

    if password != confirm_password:
        return jsonify({"error": "Password and Confirm Password do not match."}), 400

    if len(password) < 8:
        return jsonify({"error": "Administrator password must be at least 8 characters in length."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email address already exists."}), 409

    # Create user with role='admin'
    admin_user = User(
        full_name=full_name,
        email=email,
        username=username,
        password_hash=hash_password(password),
        role="admin",
        is_active=True
    )
    db.session.add(admin_user)
    db.session.flush()

    # Link to admins table
    admin_ref = Admin(user_id=admin_user.id)
    db.session.add(admin_ref)

    # Audit log
    audit_log = AdminLog(
        admin_id=admin_user.id,
        action="ENROLLED_NEW_ADMIN",
        target_type="USER",
        target_id=admin_user.id
    )
    db.session.add(audit_log)
    db.session.commit()

    return jsonify({
        "message": "Administrator registered successfully. Please proceed to Admin Login.",
        "user": admin_user.to_dict()
    }), 201

@admin_auth_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and Password are required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid administrative credentials."}), 401

    if user.role != "admin":
        return jsonify({"error": "Forbidden: This account does not possess administrator privileges."}), 403

    if not user.is_active:
        return jsonify({"error": "Administrator account has been deactivated."}), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "email": user.email, "full_name": user.full_name}
    )

    # Log login action
    try:
        log_entry = AdminLog(
            admin_id=user.id,
            action="ADMIN_LOGIN",
            target_type="AUTH",
            target_id=user.id
        )
        db.session.add(log_entry)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return jsonify({
        "message": "Administrator authenticated successfully.",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200
