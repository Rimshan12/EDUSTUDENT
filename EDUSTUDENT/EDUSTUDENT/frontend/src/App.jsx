import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./auth.jsx";
import Layout from "./components/Layout.jsx";
import Achievements from "./pages/Achievements.jsx";
import Analytics from "./pages/Analytics.jsx";
import AuthPage from "./pages/AuthPage.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Modules from "./pages/Modules.jsx";
import Quiz from "./pages/Quiz.jsx";
import Result from "./pages/Result.jsx";

function Protected({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="splash">Loading EDUSTUDENT…</div>;
  if (!user) return <Navigate to="/login" replace />;
  return <Layout>{children}</Layout>;
}

export default function App() {
  const { user, loading } = useAuth();
  return (
    <Routes>
      <Route
        path="/login"
        element={loading ? <div className="splash">Loading EDUSTUDENT…</div> : user ? <Navigate to="/" replace /> : <AuthPage />}
      />
      <Route path="/" element={<Protected><Dashboard /></Protected>} />
      <Route path="/modules" element={<Protected><Modules /></Protected>} />
      <Route path="/quiz/:topicId" element={<Protected><Quiz /></Protected>} />
      <Route path="/result/:attemptId" element={<Protected><Result /></Protected>} />
      <Route path="/analytics" element={<Protected><Analytics /></Protected>} />
      <Route path="/achievements" element={<Protected><Achievements /></Protected>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
