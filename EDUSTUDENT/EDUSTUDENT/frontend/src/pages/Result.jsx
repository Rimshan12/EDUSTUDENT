import { Link, useLocation, useParams } from "react-router-dom";
import { api } from "../api.js";
import { ScoreRing } from "../components/Charts.jsx";
import { LevelBadge, PageState, ResourceCard, StatusBadge } from "../components/Common.jsx";
import { useLoad } from "../hooks.js";

export default function Result() {
  const { attemptId } = useParams();
  const location = useLocation();
  const fromQuiz = location.state && location.state.result;
  const state = useLoad(
    () => (fromQuiz && String(fromQuiz.attempt.id) === attemptId ? Promise.resolve(fromQuiz) : api.attempt(attemptId)),
    [attemptId]
  );
  return (
    <PageState state={state}>
      {(data) => {
        const { attempt, review, recommendations, topic_status: status } = data;
        const message =
          attempt.percentage >= 80
            ? "Excellent work! You have a strong grasp of this topic."
            : attempt.percentage >= 60
              ? "Good effort. A little more practice will take you to the next level."
              : "This topic needs attention. Review the resources below and try again.";
        return (
          <>
            <section className="card result-head">
              <ScoreRing value={attempt.percentage} />
              <div>
                <h1>{attempt.topic_name}</h1>
                <p className="big">{attempt.score} / {attempt.total} correct · {attempt.duration_seconds}s</p>
                <p>{message}</p>
                <p>
                  Overall in this topic: <StatusBadge status={status.status} /> <LevelBadge level={status.level_name} />
                </p>
                <div className="actions">
                  <Link className="btn primary" to={`/quiz/${attempt.topic_id}`}>Try again</Link>
                  <Link className="btn ghost" to="/">Dashboard</Link>
                </div>
              </div>
            </section>

            <h2 className="section-title">Recommended for you</h2>
            <section className="grid two">
              {recommendations.map((resource) => (
                <ResourceCard key={resource.id} resource={resource} showReason />
              ))}
            </section>

            <h2 className="section-title">Answer review</h2>
            {review.map((item, i) => (
              <div className={`card review ${item.is_correct ? "ok" : "bad"}`} key={item.question_id}>
                <div className="q-meta">
                  Question {i + 1} · {item.is_correct ? "Correct ✓" : item.selected ? "Incorrect ✗" : "Skipped ✗"}
                </div>
                <h3>{item.text}</h3>
                <ul className="review-options">
                  {Object.entries(item.options).map(([key, text]) => (
                    <li
                      key={key}
                      className={key === item.correct ? "right" : key === item.selected ? "wrong" : ""}
                    >
                      <strong>{key}.</strong> {text}
                      {key === item.correct && " ✓"}
                      {key === item.selected && key !== item.correct && " (your answer)"}
                    </li>
                  ))}
                </ul>
                <p className="explain">💡 {item.explanation}</p>
              </div>
            ))}
          </>
        );
      }}
    </PageState>
  );
}
