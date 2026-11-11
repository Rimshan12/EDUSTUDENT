import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api.js";
import { PageState } from "../components/Common.jsx";
import { useLoad } from "../hooks.js";

export default function Quiz() {
  const { topicId } = useParams();
  const state = useLoad(() => api.startQuiz(topicId), [topicId]);
  return <PageState state={state}>{(quiz) => <QuizRunner quiz={quiz} topicId={topicId} />}</PageState>;
}

function QuizRunner({ quiz, topicId }) {
  const navigate = useNavigate();
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState({});
  const [times, setTimes] = useState({});
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const startedAt = useRef(Date.now());

  const questions = quiz.questions;
  const current = questions[index];
  const isLast = index === questions.length - 1;

  useEffect(() => {
    startedAt.current = Date.now();
  }, [index]);

  const recordTime = () => {
    const spent = Math.round((Date.now() - startedAt.current) / 1000);
    setTimes((prev) => ({ ...prev, [current.id]: (prev[current.id] || 0) + spent }));
    return { ...times, [current.id]: (times[current.id] || 0) + spent };
  };

  const go = (step) => {
    recordTime();
    setIndex(index + step);
  };

  const finish = async () => {
    const finalTimes = recordTime();
    setBusy(true);
    setError("");
    try {
      const answers = questions.map((q) => ({
        question_id: q.id,
        selected: selected[q.id] || null,
        time_taken: finalTimes[q.id] || 0,
      }));
      const result = await api.submitQuiz(topicId, answers);
      navigate(`/result/${result.attempt.id}`, { state: { result }, replace: true });
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  };

  const answered = Object.keys(selected).length;

  return (
    <div className="quiz">
      <div className="page-head">
        <div>
          <h1>{quiz.topic.icon} {quiz.topic.name} Quiz</h1>
          <p className="muted">Adaptive difficulty · Your level: {quiz.level_name}</p>
        </div>
        <div className="muted">{answered}/{questions.length} answered</div>
      </div>
      <div className="progress"><div style={{ width: `${((index + 1) / questions.length) * 100}%` }} /></div>
      <div className="card question">
        <div className="q-meta">
          Question {index + 1} of {questions.length}
          <span className={`badge diff d${current.difficulty}`}>{["", "Easy", "Medium", "Hard"][current.difficulty]}</span>
        </div>
        <h2>{current.text}</h2>
        <div className="options">
          {Object.entries(current.options).map(([key, text]) => (
            <button
              key={key}
              className={`option ${selected[current.id] === key ? "chosen" : ""}`}
              onClick={() => setSelected({ ...selected, [current.id]: key })}
            >
              <span className="key">{key}</span>
              <span>{text}</span>
            </button>
          ))}
        </div>
        {error && <div className="alert">{error}</div>}
        <div className="quiz-nav">
          <button className="btn ghost" disabled={index === 0 || busy} onClick={() => go(-1)}>← Previous</button>
          {isLast ? (
            <button className="btn primary" disabled={busy} onClick={finish}>
              {busy ? "Submitting…" : "Submit quiz"}
            </button>
          ) : (
            <button className="btn primary" onClick={() => go(1)}>Next →</button>
          )}
        </div>
      </div>
    </div>
  );
}
