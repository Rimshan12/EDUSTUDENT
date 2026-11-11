from datetime import datetime, timezone

from .extensions import db


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(190), unique=True, nullable=False, index=True)
    roll_no = db.Column(db.String(40))
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "roll_no": self.roll_no,
            "joined": self.created_at.isoformat(),
        }


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(400), nullable=False)
    icon = db.Column(db.String(8), nullable=False, default="📘")


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False, index=True)
    text = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(300), nullable=False)
    option_b = db.Column(db.String(300), nullable=False)
    option_c = db.Column(db.String(300), nullable=False)
    option_d = db.Column(db.String(300), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.String(500), nullable=False)

    def options(self):
        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }

    def to_public(self):
        return {
            "id": self.id,
            "text": self.text,
            "options": self.options(),
            "difficulty": self.difficulty,
        }


class Resource(db.Model):
    __tablename__ = "resources"
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(400), nullable=False)
    kind = db.Column(db.String(30), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.String(300), nullable=False, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "title": self.title,
            "url": self.url,
            "kind": self.kind,
            "level": self.level,
            "description": self.description,
        }


class Attempt(db.Model):
    __tablename__ = "attempts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    topic = db.relationship("Topic")
    answers = db.relationship("Answer", backref="attempt", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "topic_name": self.topic.name,
            "score": self.score,
            "total": self.total,
            "percentage": round(self.percentage, 1),
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat(),
        }


class Answer(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("attempts.id"), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False, index=True)
    selected = db.Column(db.String(1))
    is_correct = db.Column(db.Boolean, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False, default=0)
    question = db.relationship("Question")
