# EDUSTUDENT – AI-Based Personalized Learning Platform

B.Tech CSE (AIML), SR University, Warangal – Capstone Review 1 implementation.

Team: Rimsha (2303A52493), Athiqa (2303A52185), Mounika (2303A52350), Karuna (2303A52295), Vaishnavi (2303A52376)

## What it does

| Objective from the review deck | Implemented in |
| --- | --- |
| Secure registration, login, logout (password hashing + Flask sessions) | `backend/app/auth.py` |
| Topic-based quizzes with automatic scoring | `backend/app/quiz.py` |
| Answer storage and result tracking in MySQL | `backend/app/models.py` |
| Topic-wise performance analysis and weak-topic detection | `backend/app/ml.py`, `backend/app/dashboard.py` |
| AI recommendations (TF-IDF + cosine similarity over missed concepts, level-matched) | `ml.recommend` |
| Performance prediction (logistic regression, Bayesian fallback for little data) | `ml.predict_success` |
| Adaptive learning path and adaptive quiz difficulty | `ml.learning_path`, `ml.pick_questions` |
| Personalized dashboard, analytics, learning modules, achievements | `frontend/src/pages` |
| Pink-themed responsive UI | `frontend/src/styles.css` |

Seed content: 5 topics (Python, Data Structures, DBMS, Machine Learning, Web Development), 45 questions (3 easy, 3 medium, 3 hard per topic) and 20 learning resources.

## Prerequisites

- Python 3.10+
- Node.js 18+ (only needed for development mode or rebuilding the UI)
- MySQL 8 running locally (MySQL Workbench is fine for checking data)

## Step 1 – Configure the database connection

Open `backend/.env.example`, copy it to `backend/.env` and put in your MySQL password:

```
SECRET_KEY=any-long-random-string
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/edustudent
FRONTEND_ORIGINS=http://localhost:5173
```

The `edustudent` database, all tables and the seed data are created automatically on first start. You can also run `database/schema.sql` in MySQL Workbench if you prefer to create the empty database yourself.

## Step 2 – Start the backend

Windows (PowerShell):

```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

macOS / Linux:

```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

The API runs on http://localhost:5000 (check http://localhost:5000/api/health).

## Step 3 – Open the app

Option A (simplest): the repository already contains a built frontend in `frontend/dist`, so just open **http://localhost:5000** after Step 2.

Option B (development with hot reload): keep the backend running, open a second terminal:

```
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. Requests to `/api` are proxied to port 5000.

To rebuild the production UI after changing frontend code: `npm run build` inside `frontend`.

## Step 4 – Try it out

1. Click **Create an account** and register.
2. Open **Learning Modules**, pick a topic and click **Take quiz** (6 questions, adaptive difficulty).
3. Submit to see your score, answer review with explanations and AI-recommended resources.
4. Take quizzes in a few topics (and get some wrong on purpose) to see weak topics, the learning path, predictions, analytics and achievements update.
5. After 30 answered questions the prediction switches from the Bayesian estimate to a trained logistic regression model.

## Run the tests

```
cd backend
pytest
```

16 tests cover authentication, validation, scoring, privacy of attempts, adaptive difficulty, recommendations, the prediction model, analytics and achievements. They use a temporary SQLite database, so MySQL is not needed for the tests.

## Troubleshooting

- `Access denied for user 'root'`: the password in `DATABASE_URL` is wrong.
- `Can't connect to MySQL server`: start the MySQL service (Windows: Services → MySQL80 → Start).
- `RuntimeError: 'cryptography' package is required`: run `pip install cryptography`.
- Port 5000 busy (macOS AirPlay): change the port in `backend/run.py` and in `frontend/vite.config.js`.
- Special characters in the MySQL password must be URL-encoded inside `DATABASE_URL` (for example `@` becomes `%40`).
- Reset all data: drop the `edustudent` database in MySQL Workbench and restart the backend.

## Project structure

```
EDUSTUDENT/
├── backend/
│   ├── app/            Flask app: auth, quiz, dashboard, ml, models, seed data
│   ├── tests/          pytest suite
│   ├── config.py, run.py, requirements.txt, .env.example
├── frontend/
│   ├── src/            React app (pages, components, API client)
│   └── dist/           prebuilt production UI
└── database/schema.sql
```
