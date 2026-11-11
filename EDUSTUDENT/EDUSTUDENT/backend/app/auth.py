import re
from functools import wraps

from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/api/auth")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def current_user():
    user_id = session.get("user_id")
    return db.session.get(User, user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        user = current_user()
        if user is None:
            return jsonify(error="Authentication required"), 401
        return view(user, *args, **kwargs)

    return wrapper


@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    roll_no = str(data.get("roll_no", "")).strip() or None
    if len(name) < 2:
        return jsonify(error="Name must be at least 2 characters"), 400
    if not EMAIL_RE.match(email):
        return jsonify(error="Enter a valid email address"), 400
    if len(password) < 8:
        return jsonify(error="Password must be at least 8 characters"), 400
    if User.query.filter_by(email=email).first():
        return jsonify(error="An account with this email already exists"), 409
    user = User(
        name=name,
        email=email,
        roll_no=roll_no,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    session.clear()
    session["user_id"] = user.id
    return jsonify(user=user.to_dict()), 201


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    user = User.query.filter_by(email=email).first()
    if user is None or not check_password_hash(user.password_hash, password):
        return jsonify(error="Invalid email or password"), 401
    session.clear()
    session["user_id"] = user.id
    session.permanent = True
    return jsonify(user=user.to_dict())


@bp.post("/logout")
def logout():
    session.clear()
    return jsonify(message="Logged out")


@bp.get("/me")
def me():
    user = current_user()
    if user is None:
        return jsonify(user=None)
    return jsonify(user=user.to_dict())
