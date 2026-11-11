from app.extensions import db
from app.models import Question, Topic


def correct_map(app, question_ids):
    with app.app_context():
        rows = Question.query.filter(Question.id.in_(question_ids)).all()
        return {q.id: q.correct_option for q in rows}


def take_quiz(app, client, topic_id, accuracy):
    quiz = client.get(f"/api/quiz/{topic_id}").get_json()
    ids = [q["id"] for q in quiz["questions"]]
    answers = correct_map(app, ids)
    payload = []
    for index, qid in enumerate(ids):
        right = index < round(len(ids) * accuracy)
        if right:
            selected = answers[qid]
        else:
            selected = next(o for o in "ABCD" if o != answers[qid])
        payload.append({"question_id": qid, "selected": selected, "time_taken": 5})
    return client.post(f"/api/quiz/{topic_id}/submit", json={"answers": payload})


def test_register_validation_and_duplicate(client):
    assert client.post("/api/auth/register", json={"name": "A", "email": "x", "password": "1"}).status_code == 400
    ok = {"name": "Alice", "email": "alice@example.com", "password": "longpassword"}
    assert client.post("/api/auth/register", json=ok).status_code == 201
    assert client.post("/api/auth/register", json=ok).status_code == 409


def test_login_logout_me(client):
    client.post(
        "/api/auth/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "longpassword"},
    )
    client.post("/api/auth/logout")
    assert client.get("/api/auth/me").get_json()["user"] is None
    assert client.post("/api/auth/login", json={"email": "alice@example.com", "password": "wrongpass1"}).status_code == 401
    good = client.post("/api/auth/login", json={"email": "ALICE@example.com", "password": "longpassword"})
    assert good.status_code == 200
    assert client.get("/api/auth/me").get_json()["user"]["name"] == "Alice"


def test_password_is_hashed(app, auth_client):
    from app.models import User

    with app.app_context():
        user = User.query.filter_by(email="student@example.com").one()
        assert user.password_hash != "password123"
        assert user.password_hash.startswith(("scrypt:", "pbkdf2:"))


def test_protected_routes_require_login(client):
    for path in ["/api/topics", "/api/dashboard", "/api/analytics", "/api/achievements", "/api/quiz/1"]:
        assert client.get(path).status_code == 401


def test_topics_listing(auth_client):
    data = auth_client.get("/api/topics").get_json()["topics"]
    assert len(data) == 5
    assert all(t["question_count"] == 9 and len(t["resources"]) == 4 for t in data)
    assert all(t["status"] == "not_started" for t in data)


def test_quiz_hides_answers_and_mixes_difficulty(auth_client):
    quiz = auth_client.get("/api/quiz/1").get_json()
    assert len(quiz["questions"]) == 6
    assert all("correct_option" not in q and "explanation" not in q for q in quiz["questions"])
    assert len({q["id"] for q in quiz["questions"]}) == 6
    assert auth_client.get("/api/quiz/999").status_code == 404


def test_submit_scores_correctly(app, auth_client):
    response = take_quiz(app, auth_client, 1, 1.0)
    assert response.status_code == 201
    body = response.get_json()
    assert body["attempt"]["score"] == 6
    assert body["attempt"]["percentage"] == 100.0
    assert all(r["is_correct"] for r in body["review"])
    detail = auth_client.get(f"/api/attempts/{body['attempt']['id']}")
    assert detail.status_code == 200


def test_submit_rejects_bad_payloads(app, auth_client):
    assert auth_client.post("/api/quiz/1/submit", json={}).status_code == 400
    assert auth_client.post("/api/quiz/1/submit", json={"answers": [{"question_id": 1, "selected": "Z"}]}).status_code == 400
    with app.app_context():
        other = Question.query.filter(Question.topic_id == 2).first().id
    assert auth_client.post("/api/quiz/1/submit", json={"answers": [{"question_id": other, "selected": "A"}]}).status_code == 400


def test_skipped_answer_counts_wrong(app, auth_client):
    quiz = auth_client.get("/api/quiz/2").get_json()
    answers = [{"question_id": q["id"], "selected": None} for q in quiz["questions"]]
    body = auth_client.post("/api/quiz/2/submit", json={"answers": answers}).get_json()
    assert body["attempt"]["score"] == 0


def test_attempts_are_private(app, auth_client):
    attempt_id = take_quiz(app, auth_client, 1, 0.5).get_json()["attempt"]["id"]
    auth_client.post("/api/auth/logout")
    auth_client.post(
        "/api/auth/register",
        json={"name": "Other", "email": "other@example.com", "password": "password123"},
    )
    assert auth_client.get(f"/api/attempts/{attempt_id}").status_code == 404


def test_dashboard_identifies_weak_topics_and_recommends(app, auth_client):
    take_quiz(app, auth_client, 1, 0.0)
    take_quiz(app, auth_client, 2, 1.0)
    data = auth_client.get("/api/dashboard").get_json()
    assert data["summary"]["quizzes"] == 2
    assert "Python Programming" in data["weak_topics"]
    statuses = {t["name"]: t["status"] for t in data["topics"]}
    assert statuses["Python Programming"] == "weak"
    assert statuses["Data Structures"] == "strong"
    assert statuses["Machine Learning"] == "not_started"
    assert data["recommendations"]
    assert data["recommendations"][0]["topic_name"] == "Python Programming"
    assert data["recommendations"][0]["level"] == 1
    assert len(data["learning_path"]) == 5
    assert data["learning_path"][0]["status"] == "weak"
    assert data["prediction_method"] == "bayesian_estimate"


def test_logistic_model_activates_with_enough_data(app, auth_client):
    for index in range(6):
        take_quiz(app, auth_client, 1, 0.5)
        take_quiz(app, auth_client, 2, 1.0 if index % 2 else 0.5)
    data = auth_client.get("/api/dashboard").get_json()
    assert data["prediction_method"] == "logistic_regression"
    assert all(0 <= t["predicted"] <= 100 for t in data["topics"])


def test_analytics_and_achievements(app, auth_client):
    take_quiz(app, auth_client, 1, 1.0)
    analytics = auth_client.get("/api/analytics").get_json()
    assert len(analytics["trend"]) == 1
    assert {d["label"] for d in analytics["difficulty"]} == {"Easy", "Medium", "Hard"}
    achievements = auth_client.get("/api/achievements").get_json()
    earned = {a["key"] for a in achievements["achievements"] if a["earned"]}
    assert {"first_quiz", "perfect"} <= earned
    assert "five_quizzes" not in earned


def test_adaptive_quiz_gets_harder_after_success(app, auth_client):
    take_quiz(app, auth_client, 1, 1.0)
    quiz = auth_client.get("/api/quiz/1").get_json()
    assert quiz["level_name"] == "Advanced"
    hard = sum(1 for q in quiz["questions"] if q["difficulty"] == 3)
    assert hard == 3


def test_seed_is_idempotent(app):
    from app.seed_data import seed

    with app.app_context():
        before = Topic.query.count()
        seed()
        assert Topic.query.count() == before


def test_spa_fallback(client):
    assert client.get("/api/health").get_json()["status"] == "ok"
    assert client.get("/api/nope").status_code == 404
