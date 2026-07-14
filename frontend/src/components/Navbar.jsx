import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/", { replace: true });
  };

  return (
    <nav className="fixed top-0 inset-x-0 z-50 flex items-center justify-between px-6 py-4 bg-gray-950/80 backdrop-blur border-b border-gray-800">
      <Link to="/" className="text-xl font-bold tracking-tight text-brand-500">
        ScoreMorph<span className="text-white">AI</span>
      </Link>
      <div className="flex items-center gap-4 text-sm">
        {user ? (
          <>
            <Link to="/dashboard" className="text-gray-300 hover:text-white transition">My Arrangements</Link>
            <Link to="/new" className="px-4 py-1.5 rounded-full bg-brand-600 hover:bg-brand-700 transition font-medium">
              + New
            </Link>
            <span className="text-gray-400">
              Hi, <span className="text-white font-medium">{user.username}</span>
            </span>
            <button onClick={handleLogout} className="text-gray-400 hover:text-white transition">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="text-gray-300 hover:text-white transition">Login</Link>
            <Link to="/signup" className="px-4 py-1.5 rounded-full bg-brand-600 hover:bg-brand-700 transition font-medium">
              Get Started
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
