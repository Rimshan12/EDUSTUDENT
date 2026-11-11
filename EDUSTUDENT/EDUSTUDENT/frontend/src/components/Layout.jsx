import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../auth.jsx";

const links = [
  ["/", "Dashboard"],
  ["/modules", "Learning Modules"],
  ["/analytics", "Analytics"],
  ["/achievements", "Achievements"],
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">🎓 EDU<span>STUDENT</span></div>
        <nav>
          {links.map(([to, label]) => (
            <NavLink key={to} to={to} end={to === "/"} className={({ isActive }) => (isActive ? "active" : "")}>
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="user-box">
          <span>{user.name}</span>
          <button className="btn ghost small" onClick={handleLogout}>Logout</button>
        </div>
      </header>
      <main className="content">{children}</main>
      <footer className="footer">EDUSTUDENT · Learn what you need, at the pace you need.</footer>
    </div>
  );
}
