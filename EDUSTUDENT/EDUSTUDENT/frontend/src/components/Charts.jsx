export function BarList({ items }) {
  return (
    <div className="bars">
      {items.map((item) => (
        <div className="bar-row" key={item.label}>
          <div className="bar-label">{item.label}</div>
          <div className="bar-track">
            <div
              className={`bar-fill ${item.tone || ""}`}
              style={{ width: `${item.value ?? 0}%` }}
            />
          </div>
          <div className="bar-value">{item.value === null || item.value === undefined ? "–" : `${Math.round(item.value)}%`}</div>
        </div>
      ))}
    </div>
  );
}

export function TrendChart({ points }) {
  if (!points.length) return <p className="muted">Take a quiz to see your progress trend.</p>;
  const width = 560;
  const height = 180;
  const pad = 28;
  const step = points.length > 1 ? (width - pad * 2) / (points.length - 1) : 0;
  const coords = points.map((p, i) => [
    points.length > 1 ? pad + i * step : width / 2,
    height - pad - ((height - pad * 2) * p.percentage) / 100,
  ]);
  const path = coords.map(([x, y], i) => `${i === 0 ? "M" : "L"}${x},${y}`).join(" ");
  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="trend" role="img" aria-label="Score trend">
      {[0, 50, 100].map((tick) => {
        const y = height - pad - ((height - pad * 2) * tick) / 100;
        return (
          <g key={tick}>
            <line x1={pad} x2={width - pad} y1={y} y2={y} className="grid" />
            <text x={4} y={y + 4} className="tick">{tick}</text>
          </g>
        );
      })}
      {coords.length > 1 && <path d={path} className="line" />}
      {coords.map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r="5" className="dot">
          <title>{`${points[i].topic_name}: ${points[i].percentage}%`}</title>
        </circle>
      ))}
    </svg>
  );
}

export function ScoreRing({ value }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (circumference * value) / 100;
  return (
    <svg viewBox="0 0 140 140" className="ring">
      <circle cx="70" cy="70" r={radius} className="ring-bg" />
      <circle
        cx="70"
        cy="70"
        r={radius}
        className="ring-fg"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform="rotate(-90 70 70)"
      />
      <text x="70" y="76" textAnchor="middle" className="ring-text">{Math.round(value)}%</text>
    </svg>
  );
}
