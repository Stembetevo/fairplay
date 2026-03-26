import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const navItems = [
  { to: "/players", label: "Players" },
  { to: "/teams/generate", label: "Generate Teams" },
  { to: "/teams", label: "Teams" },
  { to: "/matches", label: "Matches" },
  { to: "/history", label: "My History" },
];

export function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    try {
      await logout();
      navigate("/login");
    } catch {
      navigate("/login");
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1>FairPlay</h1>
          <p>Balanced football teams, match tracking, and history</p>
        </div>
        <div className="user-actions">
          <span className="badge">Signed in: {user?.username}</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <nav className="main-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <main className="page">
        <Outlet />
      </main>
    </div>
  );
}
