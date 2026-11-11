import { useState } from "react";
import { useAuth } from "../auth.jsx";

export default function AuthPage() {
  const { login, register } = useAuth();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ name: "", email: "", roll_no: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const update = (key) => (event) => setForm({ ...form, [key]: event.target.value });

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      if (mode === "login") {
        await login({ email: form.email, password: form.password });
      } else {
        await register(form);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-wrap">
      <div className="auth-hero">
        <h1>🎓 EDU<span>STUDENT</span></h1>
        <p className="tagline">Your AI-Based Personalized Learning Platform</p>
        <ul>
          <li>Topic-wise quizzes that adapt to your level</li>
          <li>AI-powered weak-area detection</li>
          <li>Personalized learning resources and path</li>
          <li>Progress tracking and achievements</li>
        </ul>
        <p className="quote">“Right content → Right difficulty → Right student → Right time”</p>
      </div>
      <form className="card auth-card" onSubmit={submit}>
        <h2>{mode === "login" ? "Welcome back" : "Create your account"}</h2>
        {mode === "register" && (
          <>
            <label>Full name
              <input value={form.name} onChange={update("name")} required minLength={2} />
            </label>
            <label>Roll number (optional)
              <input value={form.roll_no} onChange={update("roll_no")} />
            </label>
          </>
        )}
        <label>Email
          <input type="email" value={form.email} onChange={update("email")} required />
        </label>
        <label>Password
          <input type="password" value={form.password} onChange={update("password")} required minLength={mode === "register" ? 8 : 1} />
        </label>
        {error && <div className="alert">{error}</div>}
        <button className="btn primary block" disabled={busy}>
          {busy ? "Please wait…" : mode === "login" ? "Login" : "Register"}
        </button>
        <p className="switch">
          {mode === "login" ? "New here?" : "Already registered?"}{" "}
          <button type="button" className="link" onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(""); }}>
            {mode === "login" ? "Create an account" : "Login"}
          </button>
        </p>
      </form>
    </div>
  );
}
