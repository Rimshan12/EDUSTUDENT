import { Link } from "react-router-dom";
import { api } from "../api.js";
import { TrendChart } from "../components/Charts.jsx";
import { LevelBadge, PageState, ResourceCard, StatusBadge, TakeQuizButton } from "../components/Common.jsx";
import { useLoad } from "../hooks.js";

export default function Dashboard() {
  const state = useLoad(api.dashboard);
  return (
    <PageState state={state}>
      {(data) => (
        <>
          <section className="hero-card">
            <div>
              <h1>Hello, {data.user.name.split(" ")[0]} 👋</h1>
              <p>
                {data.summary.quizzes === 0
                  ? "Take your first quiz and EDUSTUDENT will start building your personalized learning path."
                  : data.weak_topics.length
                    ? `Focus areas right now: ${data.weak_topics.join(", ")}.`
                    : "You are doing great. Keep pushing to advanced levels."}
              </p>
            </div>
            <Link className="btn light" to="/modules">Start learning</Link>
          </section>

          <section className="stat-grid">
            <Stat label="Quizzes taken" value={data.summary.quizzes} />
            <Stat label="Average score" value={`${data.summary.average}%`} />
            <Stat label="Best score" value={`${data.summary.best}%`} />
            <Stat label="Topics started" value={`${data.summary.topics_started}/${data.summary.topics_total}`} />
          </section>

          <h2 className="section-title">Topic mastery</h2>
          <section className="grid three">
            {data.topics.map((topic) => (
              <div className="card topic" key={topic.topic_id}>
                <div className="topic-head">
                  <span className="icon">{topic.icon}</span>
                  <div>
                    <h3>{topic.name}</h3>
                    <StatusBadge status={topic.status} /> <LevelBadge level={topic.level_name} />
                  </div>
                </div>
                <div className="meter"><div style={{ width: `${topic.accuracy ?? 0}%` }} /></div>
                <div className="meta">
                  <span>Accuracy: {topic.accuracy === null ? "–" : `${topic.accuracy}%`}</span>
                  <span title="Predicted chance of answering a medium question correctly">
                    Predicted: {topic.predicted}%
                  </span>
                </div>
                <TakeQuizButton topicId={topic.topic_id} label={topic.attempted ? "Practice again" : "Start quiz"} />
              </div>
            ))}
          </section>

          <section className="grid two">
            <div className="card">
              <h2>Your progress</h2>
              <TrendChart points={[...data.recent_attempts].reverse().map((a) => ({ percentage: a.percentage, topic_name: a.topic_name }))} />
            </div>
            <div className="card">
              <h2>Personalized learning path</h2>
              <ol className="path">
                {data.learning_path.map((step) => (
                  <li key={step.topic_id} className={step.status}>
                    <div>
                      <strong>{step.icon} {step.action}</strong>
                      {step.resource && (
                        <a href={step.resource.url} target="_blank" rel="noreferrer"> → {step.resource.title}</a>
                      )}
                    </div>
                  </li>
                ))}
              </ol>
            </div>
          </section>

          <h2 className="section-title">AI recommended resources</h2>
          {data.recommendations.length === 0 ? (
            <div className="card muted">Complete a quiz to receive personalized resource recommendations.</div>
          ) : (
            <section className="grid three">
              {data.recommendations.map((resource) => (
                <ResourceCard key={resource.id} resource={resource} showReason />
              ))}
            </section>
          )}
        </>
      )}
    </PageState>
  );
}

function Stat({ label, value }) {
  return (
    <div className="card stat">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}
