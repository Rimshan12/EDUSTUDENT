import { api } from "../api.js";
import { PageState } from "../components/Common.jsx";
import { useLoad } from "../hooks.js";

const ICONS = {
  first_quiz: "🚀",
  five_quizzes: "📚",
  perfect: "💯",
  explorer: "🧭",
  streak: "🔥",
  master: "🏆",
  high: "⭐",
};

export default function Achievements() {
  const state = useLoad(api.achievements);
  return (
    <PageState state={state}>
      {(data) => (
        <>
          <div className="page-head">
            <div>
              <h1>Achievements</h1>
              <p className="muted">{data.earned} of {data.total} unlocked</p>
            </div>
          </div>
          <section className="grid three">
            {data.achievements.map((a) => (
              <div className={`card achievement ${a.earned ? "earned" : "locked"}`} key={a.key}>
                <div className="trophy">{ICONS[a.key] || "🎖️"}</div>
                <h3>{a.title}</h3>
                <p>{a.description}</p>
                <div className="meter"><div style={{ width: `${(a.progress / a.target) * 100}%` }} /></div>
                <div className="meta"><span>{a.progress}/{a.target}</span><span>{a.earned ? "Unlocked" : "Locked"}</span></div>
              </div>
            ))}
          </section>
        </>
      )}
    </PageState>
  );
}
