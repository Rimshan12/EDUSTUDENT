import { Link } from "react-router-dom";
import { api } from "../api.js";
import { BarList, TrendChart } from "../components/Charts.jsx";
import { PageState, StatusBadge } from "../components/Common.jsx";
import { useLoad } from "../hooks.js";

const tone = (status) => (status === "strong" ? "good" : status === "weak" ? "bad" : "mid");

export default function Analytics() {
  const state = useLoad(api.analytics);
  return (
    <PageState state={state}>
      {(data) => (
        <>
          <div className="page-head">
            <div>
              <h1>Performance Analytics</h1>
              <p className="muted">
                Predictions use {data.prediction_method === "logistic_regression"
                  ? "a logistic regression model trained on your answer history."
                  : "a Bayesian estimate until you have answered 30 questions, then a logistic regression model takes over."}
              </p>
            </div>
          </div>
          <section className="grid two">
            <div className="card">
              <h2>Accuracy by topic</h2>
              <BarList items={data.topics.map((t) => ({ label: t.name, value: t.accuracy, tone: tone(t.status) }))} />
            </div>
            <div className="card">
              <h2>Predicted success (medium question)</h2>
              <BarList items={data.topics.map((t) => ({ label: t.name, value: t.predicted, tone: "mid" }))} />
            </div>
            <div className="card">
              <h2>Accuracy by difficulty</h2>
              <BarList items={data.difficulty.map((d) => ({ label: `${d.label} (${d.answered})`, value: d.accuracy, tone: "mid" }))} />
            </div>
            <div className="card">
              <h2>Score trend</h2>
              <TrendChart points={data.trend} />
            </div>
          </section>
          <h2 className="section-title">Topic breakdown</h2>
          <div className="card table-wrap">
            <table>
              <thead>
                <tr><th>Topic</th><th>Quizzes</th><th>Answered</th><th>Correct</th><th>Accuracy</th><th>Level</th><th>Status</th></tr>
              </thead>
              <tbody>
                {data.topics.map((t) => (
                  <tr key={t.topic_id}>
                    <td>{t.icon} {t.name}</td>
                    <td>{t.quizzes}</td>
                    <td>{t.attempted}</td>
                    <td>{t.correct}</td>
                    <td>{t.accuracy === null ? "–" : `${t.accuracy}%`}</td>
                    <td>{t.level_name}</td>
                    <td><StatusBadge status={t.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <h2 className="section-title">Quiz history</h2>
          <div className="card table-wrap">
            {data.attempts.length === 0 ? (
              <p className="muted">No quizzes taken yet.</p>
            ) : (
              <table>
                <thead>
                  <tr><th>Date</th><th>Topic</th><th>Score</th><th>Percentage</th><th>Time</th></tr>
                </thead>
                <tbody>
                  {data.attempts.map((a) => (
                    <tr key={a.id}>
                      <td>{new Date(a.created_at + "Z").toLocaleString()}</td>
                      <td><Link to={`/result/${a.id}`}>{a.topic_name}</Link></td>
                      <td>{a.score}/{a.total}</td>
                      <td>{a.percentage}%</td>
                      <td>{a.duration_seconds}s</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </PageState>
  );
}
