import { createContext, useContext, useState, useCallback } from "react";
import { login as apiLogin, signup as apiSignup, logout as apiLogout, getStoredToken } from "../api/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    // Restore session from token presence (swap for JWT decode if needed)
    return getStoredToken() ? { token: getStoredToken() } : null;
  });

  const login = useCallback(async (email, password) => {
    const u = await apiLogin(email, password);
    setUser(u);
  }, []);

  const signup = useCallback(async (email, password) => {
    const u = await apiSignup(email, password);
    setUser(u);
  }, []);

  const logout = useCallback(() => {
    apiLogout();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
