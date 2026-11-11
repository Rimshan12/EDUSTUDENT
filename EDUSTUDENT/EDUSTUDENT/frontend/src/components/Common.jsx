import { Link } from "react-router-dom";

export const STATUS_LABEL = {
  not_started: "Not started",
  weak: "Needs work",
  improving: "Improving",
  strong: "Strong",
};

export function StatusBadge({ status }) {
  return <span className={`badge ${status}`}>{STATUS_LABEL[status]}</span>;
}

export function LevelBadge({ level }) {
  return <span className="badge level">{level}</span>;
}

export function ResourceCard({ resource, showReason }) {
  return (
    <a className="resource" href={resource.url} target="_blank" rel="noreferrer">
      <div className="resource-head">
        <strong>{resource.title}</strong>
        <span className="badge kind">{resource.kind}</span>
      </div>
      <p>{resource.description}</p>
      {showReason && resource.reason && <p className="reason">💡 {resource.reason}</p>}
    </a>
  );
}

export function PageState({ state, children }) {
  if (state.loading) return <div className="state">Loading…</div>;
  if (state.error) return <div className="state error">{state.error}</div>;
  return children(state.data);
}

export function TakeQuizButton({ topicId, label = "Take quiz" }) {
  return (
    <Link className="btn primary small" to={`/quiz/${topicId}`}>
      {label}
    </Link>
  );
}
