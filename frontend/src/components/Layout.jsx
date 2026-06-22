import { BarChart3, Boxes, LogOut } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { user, logout } = useAuth();
  const linkClass = ({ isActive }) =>
    `flex items-center gap-2 rounded-md px-3 py-2 text-sm ${
      isActive ? "bg-mint text-white" : "text-slate-700 hover:bg-slate-100"
    }`;

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <div>
            <h1 className="text-lg font-semibold text-ink">Structured Investment Platform</h1>
            <p className="text-xs text-slate-500">{user?.full_name}</p>
          </div>
          <button onClick={logout} className="flex items-center gap-2 border border-slate-300 px-3 py-2 hover:bg-slate-50">
            <LogOut size={16} />
            Logout
          </button>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 md:grid-cols-[220px_1fr]">
        <nav className="space-y-1">
          <NavLink to="/" end className={linkClass}>
            <BarChart3 size={16} />
            Dashboard
          </NavLink>
          <NavLink to="/products" className={linkClass}>
            <Boxes size={16} />
            Products
          </NavLink>
        </nav>
        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}

