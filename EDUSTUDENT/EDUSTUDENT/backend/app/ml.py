import random

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import func

from .extensions import db
from .models import Answer, Attempt, Question, Resource

LEVEL_NAMES = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
WEAK_THRESHOLD = 0.6
STRONG_THRESHOLD = 0.8
MIN_ROWS_FOR_MODEL = 30
QUIZ_MIX = {
    1: {1: 3, 2: 2, 3: 1},
    2: {1: 1, 2: 3, 3: 2},
    3: {1: 1, 2: 2, 3: 3},
}
COLUMNS = [
    "is_correct",
    "attempt_id",
    "created_at",
    "topic_id",
    "question_id",
    "difficulty",
    "text",
    "explanation",
]


def load_answers(user_id):
    rows = (
        db.session.query(
            Answer.is_correct,
            Answer.attempt_id,
            Attempt.created_at,
            Attempt.topic_id,
            Question.id,
            Question.difficulty,
            Question.text,
            Question.explanation,
        )
        .join(Attempt, Answer.attempt_id == Attempt.id)
        .join(Question, Answer.question_id == Question.id)
        .filter(Attempt.user_id == user_id)
        .all()
    )
    frame = pd.DataFrame([tuple(r) for r in rows], columns=COLUMNS)
    frame["is_correct"] = frame["is_correct"].astype(int)
    return frame


def level_from_ratio(ratio):
    if ratio is None or ratio < 0.5:
        return 1
    if ratio < STRONG_THRESHOLD:
        return 2
    return 3


def status_from_ratio(ratio):
    if ratio is None:
        return "not_started"
    if ratio < WEAK_THRESHOLD:
        return "weak"
    if ratio < STRONG_THRESHOLD:
        return "improving"
    return "strong"


def topic_stats(frame, topics):
    stats = []
    for topic in topics:
        sub = frame[frame["topic_id"] == topic.id]
        attempted = int(len(sub))
        correct = int(sub["is_correct"].sum()) if attempted else 0
        ratio = correct / attempted if attempted else None
        level = level_from_ratio(ratio)
        stats.append(
            {
                "topic_id": topic.id,
                "name": topic.name,
                "icon": topic.icon,
                "description": topic.description,
                "attempted": attempted,
                "correct": correct,
                "quizzes": int(sub["attempt_id"].nunique()) if attempted else 0,
                "ratio": ratio,
                "accuracy": round(ratio * 100, 1) if ratio is not None else None,
                "level": level,
                "level_name": LEVEL_NAMES[level],
                "status": status_from_ratio(ratio),
            }
        )
    return stats


def _features(topic_values, difficulty_values, topic_ids):
    rows = []
    for topic_value, difficulty in zip(topic_values, difficulty_values):
        rows.append(
            [float(difficulty)] + [1.0 if int(topic_value) == tid else 0.0 for tid in topic_ids]
        )
    return np.array(rows)


def predict_success(frame, topic_ids):
    model = None
    if len(frame) >= MIN_ROWS_FOR_MODEL and frame["is_correct"].nunique() == 2:
        features = _features(frame["topic_id"], frame["difficulty"], topic_ids)
        model = LogisticRegression(max_iter=1000).fit(features, frame["is_correct"])
    predictions = {}
    for tid in topic_ids:
        sub = frame[frame["topic_id"] == tid]
        if model is not None and len(sub) > 0:
            row = _features([tid], [2], topic_ids)
            predictions[tid] = float(model.predict_proba(row)[0][1])
        else:
            predictions[tid] = float((sub["is_correct"].sum() + 1) / (len(sub) + 2))
    method = "logistic_regression" if model is not None else "bayesian_estimate"
    return predictions, method


def recommend(frame, stats, limit=6, topic_id=None):
    resources = Resource.query.all()
    if frame.empty or not resources:
        return []
    if topic_id is not None:
        candidates = [s for s in stats if s["topic_id"] == topic_id and s["attempted"]]
    else:
        candidates = [s for s in stats if s["attempted"] and s["ratio"] < STRONG_THRESHOLD]
        if not candidates:
            candidates = [s for s in stats if s["attempted"]]
    if not candidates:
        return []
    documents = [f"{r.title} {r.description} {r.tags}" for r in resources]
    missed = frame[frame["is_correct"] == 0]
    missed_text = (missed["text"] + " " + missed["explanation"]).tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    vectorizer.fit(documents + missed_text)
    matrix = vectorizer.transform(documents)
    items = []
    for stat in candidates:
        topic_missed = missed[missed["topic_id"] == stat["topic_id"]]
        query = " ".join((topic_missed["text"] + " " + topic_missed["explanation"]).tolist())
        query = query or stat["name"]
        similarity = cosine_similarity(vectorizer.transform([query]), matrix)[0]
        gap = 1.0 - stat["ratio"]
        per_topic = []
        for index, resource in enumerate(resources):
            if resource.topic_id != stat["topic_id"]:
                continue
            level_fit = 1.0 - abs(resource.level - stat["level"]) / 2.0
            score = (0.55 * float(similarity[index]) + 0.45 * level_fit) * (0.5 + gap)
            if stat["ratio"] < STRONG_THRESHOLD:
                reason = (
                    f"You scored {stat['accuracy']}% in {stat['name']}; this resource "
                    "targets the concepts you missed."
                )
            else:
                reason = f"You are strong in {stat['name']}; go deeper with this resource."
            item = resource.to_dict()
            item.update(
                {
                    "topic_name": stat["name"],
                    "score": round(score, 3),
                    "reason": reason,
                }
            )
            per_topic.append(item)
        per_topic.sort(key=lambda x: -x["score"])
        items.extend(per_topic[:2] if topic_id is None else per_topic[:limit])
    items.sort(key=lambda x: -x["score"])
    return items[:limit]


def learning_path(stats, recommendations):
    order = {"weak": 0, "not_started": 1, "improving": 2, "strong": 3}
    steps = []
    for stat in sorted(stats, key=lambda s: (order[s["status"]], s["ratio"] or 0)):
        resource = next((r for r in recommendations if r["topic_id"] == stat["topic_id"]), None)
        if stat["status"] == "weak":
            action = f"Revise {stat['name']} fundamentals, then retake the quiz"
        elif stat["status"] == "not_started":
            action = f"Take a baseline quiz in {stat['name']}"
        elif stat["status"] == "improving":
            action = f"Practise intermediate {stat['name']} questions to reach 80%"
        else:
            action = f"Move on to advanced {stat['name']} challenges"
        steps.append(
            {
                "topic_id": stat["topic_id"],
                "topic_name": stat["name"],
                "icon": stat["icon"],
                "status": stat["status"],
                "level_name": stat["level_name"],
                "action": action,
                "resource": resource,
            }
        )
    return steps


def pick_questions(user_id, topic_id, level, rng=None):
    rng = rng or random.Random()
    seen = dict(
        db.session.query(Answer.question_id, func.count(Answer.id))
        .join(Attempt, Answer.attempt_id == Attempt.id)
        .filter(Attempt.user_id == user_id, Attempt.topic_id == topic_id)
        .group_by(Answer.question_id)
        .all()
    )
    questions = Question.query.filter_by(topic_id=topic_id).all()
    chosen = []
    for difficulty, count in QUIZ_MIX[level].items():
        pool = [q for q in questions if q.difficulty == difficulty]
        rng.shuffle(pool)
        pool.sort(key=lambda q: seen.get(q.id, 0))
        chosen.extend(pool[:count])
    rng.shuffle(chosen)
    return chosen


def achievements(attempts, stats):
    percentages = [a.percentage for a in attempts]
    ordered = sorted(attempts, key=lambda a: a.created_at)
    streak = best_streak = 0
    for attempt in ordered:
        streak = streak + 1 if attempt.percentage >= 60 else 0
        best_streak = max(best_streak, streak)
    started = sum(1 for s in stats if s["attempted"])
    mastered = sum(1 for s in stats if s["attempted"] >= 6 and s["ratio"] >= STRONG_THRESHOLD)
    average = sum(percentages) / len(percentages) if percentages else 0
    definitions = [
        ("first_quiz", "First Steps", "Complete your first quiz", 1, len(attempts)),
        ("five_quizzes", "Quiz Enthusiast", "Complete 5 quizzes", 5, len(attempts)),
        ("perfect", "Perfect Score", "Score 100% in a quiz", 1, 1 if any(p >= 100 for p in percentages) else 0),
        ("explorer", "Topic Explorer", "Attempt every topic", len(stats), started),
        ("streak", "On a Streak", "Score 60%+ in 3 quizzes in a row", 3, best_streak),
        ("master", "Topic Master", "Reach 80%+ accuracy in a topic (6+ answers)", 1, mastered),
        ("high", "High Achiever", "Average 80%+ across 3 or more quizzes", 1, 1 if len(attempts) >= 3 and average >= 80 else 0),
    ]
    return [
        {
            "key": key,
            "title": title,
            "description": description,
            "target": target,
            "progress": min(progress, target),
            "earned": progress >= target,
        }
        for key, title, description, target, progress in definitions
    ]
