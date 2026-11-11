from flask import Blueprint, jsonify

from . import ml
from .auth import login_required
from .models import Attempt, Topic

bp = Blueprint("dashboard", __name__, url_prefix="/api")


def _context(user):
    topics = Topic.query.order_by(Topic.id).all()
    frame = ml.load_answers(user.id)
    stats = ml.topic_stats(frame, topics)
    predictions, method = ml.predict_success(frame, [t.id for t in topics])
    for stat in stats:
        stat["predicted"] = round(predictions[stat["topic_id"]] * 100)
    return frame, stats, method


def _public(stats):
    return [{k: v for k, v in s.items() if k != "ratio"} for s in stats]


@bp.get("/dashboard")
@login_required
def dashboard(user):
    frame, stats, method = _context(user)
    attempts = (
        Attempt.query.filter_by(user_id=user.id).order_by(Attempt.created_at.desc()).all()
    )
    percentages = [a.percentage for a in attempts]
    recommendations = ml.recommend(frame, stats, limit=6)
    return jsonify(
        user=user.to_dict(),
        summary={
            "quizzes": len(attempts),
            "average": round(sum(percentages) / len(percentages), 1) if percentages else 0,
            "best": round(max(percentages), 1) if percentages else 0,
            "questions_answered": int(len(frame)),
            "topics_started": sum(1 for s in stats if s["attempted"]),
            "topics_total": len(stats),
        },
        topics=_public(stats),
        weak_topics=[s["name"] for s in stats if s["status"] == "weak"],
        recommendations=recommendations,
        learning_path=ml.learning_path(stats, recommendations),
        recent_attempts=[a.to_dict() for a in attempts[:5]],
        prediction_method=method,
    )


@bp.get("/analytics")
@login_required
def analytics(user):
    frame, stats, method = _context(user)
    attempts = (
        Attempt.query.filter_by(user_id=user.id).order_by(Attempt.created_at.asc()).all()
    )
    difficulty = []
    for level, label in ml.LEVEL_NAMES.items():
        sub = frame[frame["difficulty"] == level]
        answered = int(len(sub))
        difficulty.append(
            {
                "difficulty": level,
                "label": {1: "Easy", 2: "Medium", 3: "Hard"}[level],
                "answered": answered,
                "accuracy": round(float(sub["is_correct"].mean()) * 100, 1) if answered else None,
            }
        )
    return jsonify(
        topics=_public(stats),
        difficulty=difficulty,
        trend=[
            {
                "attempt_id": a.id,
                "topic_name": a.topic.name,
                "percentage": round(a.percentage, 1),
                "created_at": a.created_at.isoformat(),
            }
            for a in attempts
        ],
        attempts=[a.to_dict() for a in reversed(attempts)],
        prediction_method=method,
    )


@bp.get("/achievements")
@login_required
def achievements(user):
    frame, stats, _ = _context(user)
    attempts = Attempt.query.filter_by(user_id=user.id).all()
    items = ml.achievements(attempts, stats)
    return jsonify(
        achievements=items,
        earned=sum(1 for i in items if i["earned"]),
        total=len(items),
    )
