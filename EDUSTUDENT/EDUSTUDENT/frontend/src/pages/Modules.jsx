import { useState } from "react";
import { api } from "../api.js";
import { LevelBadge, PageState, ResourceCard, StatusBadge, TakeQuizButton } from "../components/Common.jsx";
import { useLoad } from "../hooks.js";

const FILTERS = [
  [0, "All levels"],
  [1, "Beginner"],
  [2, "Intermediate"],
  [3, "Advanced"],
];

export default function Modules() {
  const state = useLoad(api.topics);
  const [level, setLevel] = useState(0);
  return (
    <PageState state={state}>
      {(data) => (
        <>
          <div className="page-head">
            <div>
              <h1>Learning Modules</h1>
              <p className="muted">Pick a topic, study the resources, then test yourself with an adaptive quiz.</p>
            </div>
            <div className="filters">
              {FILTERS.map(([value, label]) => (
                <button key={value} className={`chip ${level === value ? "on" : ""}`} onClick={() => setLevel(value)}>
                  {label}
                </button>
              ))}
            </div>
          </div>
          {data.topics.map((topic) => (
            <section className="card module" key={topic.topic_id}>
              <div className="module-head">
                <div className="topic-head">
                  <span className="icon">{topic.icon}</span>
                  <div>
                    <h2>{topic.name}</h2>
                    <p className="muted">{topic.description}</p>
                    <StatusBadge status={topic.status} /> <LevelBadge level={`Your level: ${topic.level_name}`} />
                  </div>
                </div>
                <TakeQuizButton topicId={topic.topic_id} />
              </div>
              <div className="grid two">
                {topic.resources
                  .filter((r) => level === 0 || r.level === level)
                  .map((resource) => (
                    <ResourceCard key={resource.id} resource={resource} />
                  ))}
              </div>
            </section>
          ))}
        </>
      )}
    </PageState>
  );
}
