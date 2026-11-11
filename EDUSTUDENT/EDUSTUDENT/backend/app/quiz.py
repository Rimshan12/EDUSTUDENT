from flask import Blueprint, jsonify, request

from . import ml
from .auth import login_required
from .extensions import db
from .models import Answer, Attempt, Question, Resource, Topic

bp = Blueprint("quiz", __name__, url_prefix="/api")
VALID_OPTIONS = {"A", "B", "C", "D"}


def _context(user):
    topics = Topic.query.order_by(Topic.id).all()
    frame = ml.load_answers(user.id)
    stats = ml.topic_stats(frame, topics)
    return topics, frame, stats


def _result_payload(user, attempt):
    answers = (
        Answer.query.filter_by(attempt_id=attempt.id).order_by(Answer.id).all()
    )
    review = []
    for answer in answers:
        question = answer.question
        review.append(
            {
                "question_id": question.id,
                "text": question.text,
                "options": question.options(),
                "selected": answer.selected,
                "correct": question.correct_option,
                "is_correct": answer.is_correct,
                "difficulty": question.difficulty,
                "explanation": question.explanation,
            }
        )
    _, frame, stats = _context(user)
    topic_stat = next(s for s in stats if s["topic_id"] == attempt.topic_id)
    recommendations = ml.recommend(frame, stats, limit=4, topic_id=attempt.topic_id)
    return {
        "attempt": attempt.to_dict(),
        "review": review,
        "topic_status": {
            "accuracy": topic_stat["accuracy"],
            "level_name": topic_stat["level_name"],
            "status": topic_stat["status"],
        },
        "recommendations": recommendations,
    }


@bp.get("/topics")
@login_required
def topics(user):
    topic_rows, _, stats = _context(user)
    resources = Resource.query.order_by(Resource.level, Resource.id).all()
    payload = []
    for stat in stats:
        item = {k: v for k, v in stat.items() if k != "ratio"}
        item["question_count"] = Question.query.filter_by(topic_id=stat["topic_id"]).count()
        item["resources"] = [r.to_dict() for r in resources if r.topic_id == stat["topic_id"]]
        payload.append(item)
    return jsonify(topics=payload)


@bp.get("/quiz/<int:topic_id>")
@login_required
def start_quiz(user, topic_id):
    topic = db.session.get(Topic, topic_id)
    if topic is None:
        return jsonify(error="Topic not found"), 404
    _, _, stats = _context(user)
    stat = next(s for s in stats if s["topic_id"] == topic_id)
    questions = ml.pick_questions(user.id, topic_id, stat["level"])
    return jsonify(
        topic={"id": topic.id, "name": topic.name, "icon": topic.icon},
        level_name=stat["level_name"],
        questions=[q.to_public() for q in questions],
    )


@bp.post("/quiz/<int:topic_id>/submit")
@login_required
def submit_quiz(user, topic_id):
    topic = db.session.get(Topic, topic_id)
    if topic is None:
        return jsonify(error="Topic not found"), 404
    payload = request.get_json(silent=True) or {}
    submitted = payload.get("answers")
    if not isinstance(submitted, list) or not 0 < len(submitted) <= 20:
        return jsonify(error="Provide between 1 and 20 answers"), 400
    cleaned = {}
    for item in submitted:
        if not isinstance(item, dict):
            return jsonify(error="Invalid answer format"), 400
        try:
            question_id = int(item.get("question_id"))
        except (TypeError, ValueError):
            return jsonify(error="Invalid question id"), 400
        selected = item.get("selected")
        if selected is not None:
            selected = str(selected).upper()
            if selected not in VALID_OPTIONS:
                return jsonify(error="Invalid option selected"), 400
        try:
            time_taken = max(0, min(int(item.get("time_taken", 0)), 3600))
        except (TypeError, ValueError):
            time_taken = 0
        cleaned[question_id] = (selected, time_taken)
    questions = Question.query.filter(
        Question.id.in_(list(cleaned)), Question.topic_id == topic_id
    ).all()
    if len(questions) != len(cleaned):
        return jsonify(error="Answers contain questions outside this topic"), 400
    score = 0
    attempt = Attempt(
        user_id=user.id,
        topic_id=topic_id,
        score=0,
        total=len(questions),
        percentage=0.0,
        duration_seconds=sum(t for _, t in cleaned.values()),
    )
    db.session.add(attempt)
    db.session.flush()
    for question in sorted(questions, key=lambda q: q.id):
        selected, time_taken = cleaned[question.id]
        correct = selected == question.correct_option
        score += 1 if correct else 0
        db.session.add(
            Answer(
                attempt_id=attempt.id,
                question_id=question.id,
                selected=selected,
                is_correct=correct,
                time_taken=time_taken,
            )
        )
    attempt.score = score
    attempt.percentage = round(score * 100.0 / len(questions), 2)
    db.session.commit()
    return jsonify(_result_payload(user, attempt)), 201


@bp.get("/attempts/<int:attempt_id>")
@login_required
def attempt_detail(user, attempt_id):
    attempt = Attempt.query.filter_by(id=attempt_id, user_id=user.id).first()
    if attempt is None:
        return jsonify(error="Attempt not found"), 404
    return jsonify(_result_payload(user, attempt))
