import { createContext, useContext, useState, useCallback, useEffect } from "react";
import { login as apiLogin, signup as apiSignup, logout as apiLogout, getStoredToken } from "../api/authService";
import { coreClient } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser]       = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getStoredToken();
    if (!token) {
      setLoading(false);
      return;
    }
    coreClient.get("/auth/me", { timeout: 5000 })
      .then(({ data }) => setUser(data))
      .catch(() => {
        apiLogout();
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

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
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
