import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from config import Config

from .dbutil import ensure_database
from .extensions import db

DIST = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
)


def create_app(overrides=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    if overrides:
        app.config.update(overrides)
    CORS(app, supports_credentials=True, origins=app.config["FRONTEND_ORIGINS"])
    ensure_database(app.config["SQLALCHEMY_DATABASE_URI"])
    db.init_app(app)

    from .auth import bp as auth_bp
    from .dashboard import bp as dashboard_bp
    from .quiz import bp as quiz_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(dashboard_bp)

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def spa(path):
        if path.startswith("api/"):
            return jsonify(error="Not found"), 404
        target = os.path.join(DIST, path)
        if path and os.path.isfile(target):
            return send_from_directory(DIST, path)
        if os.path.isfile(os.path.join(DIST, "index.html")):
            return send_from_directory(DIST, "index.html")
        return jsonify(message="EDUSTUDENT API is running. Start the frontend with npm run dev.")

    with app.app_context():
        from . import models
        from .seed_data import seed

        db.create_all()
        seed()
    return app
