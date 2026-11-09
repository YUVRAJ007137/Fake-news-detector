"""
Routes: auth_routes.py
Description: Public user registration, login, logout, and profile endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.models import db, User
from backend.utils.auth_utils import hash_password, verify_password

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    username = data.get("username", "").strip() or None
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")

    # Validations
    if not full_name or not email or not password:
        return jsonify({"error": "Full Name, Email, and Password are required."}), 400

    if password != confirm_password:
        return jsonify({"error": "Password and Confirm Password do not match."}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters in length."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email address already exists."}), 409

    if username and User.query.filter_by(username=username).first():
        return jsonify({"error": "This username is already taken."}), 409

    # Enforce standard 'user' role strictly on server
    new_user = User(
        full_name=full_name,
        email=email,
        username=username,
        password_hash=hash_password(password),
        role="user",
        is_active=True
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registration successful. Please log in with your credentials.",
        "user": new_user.to_dict()
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and Password are required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid email or password credentials."}), 401

    if not user.is_active:
        return jsonify({"error": "Your account has been deactivated. Please contact the administrator."}), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "email": user.email, "full_name": user.full_name}
    )

    return jsonify({
        "message": "Login successful.",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"user": user.to_dict()}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Successfully logged out."}), 200
