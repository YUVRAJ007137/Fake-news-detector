"""
Application: app.py
Description: Main entry point for Flask backend serving the AI Based Fake News
             Detection System REST APIs.
"""

import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Ensure root directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import Config
from backend.models import db
from backend.services.prediction_service import PredictionService
from backend.routes import (
    auth_bp, admin_auth_bp, news_bp, file_bp,
    dataset_bp, model_bp, admin_bp, health_bp
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # CORS Configuration
    CORS(app, origins=app.config.get("CORS_ORIGINS", ["http://localhost:5173", "http://127.0.0.1:5173"]), supports_credentials=True)

    # Database & JWT
    db.init_app(app)
    jwt = JWTManager(app)

    # JWT Error handlers
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "error": "Unauthorized",
            "message": "Authorization token is missing. Please log in."
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "error": "Invalid Token",
            "message": "Provided token is invalid or corrupted."
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "Token Expired",
            "message": "Your session has expired. Please log in again."
        }), 401

    # Standard HTTP Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"error": "Forbidden", "message": "Access denied."}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested endpoint does not exist."}), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({"error": "Payload Too Large", "message": "Uploaded file exceeds the maximum 10MB limit."}), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal Server Error", "message": "An unexpected server error occurred."}), 500

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_auth_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(dataset_bp)
    app.register_blueprint(model_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(health_bp)

    # Root route
    @app.route("/")
    def index():
        return jsonify({
            "system": "AI Based Fake News Detection System API",
            "version": "1.0.0",
            "documentation": "/api/health",
            "status": "online"
        }), 200

    # Preload ML model within application context
    with app.app_context():
        try:
            PredictionService.load_artifacts()
            print("[INFO] ML champion model and TF-IDF vectorizer pre-loaded successfully.")
        except Exception as e:
            print(f"[WARNING] ML artifacts could not be pre-loaded: {e}")

    return app

if __name__ == "__main__":
    app = create_app()
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    print("Starting AI Based Fake News Detection Flask server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
