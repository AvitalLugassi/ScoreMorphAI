import client from "./client";

export async function login(email, password) {
  const { data } = await client.post("/api/auth/login", { email, password });
  localStorage.setItem("token", data.token);
  return data.user;
}

export async function signup(email, password) {
  const { data } = await client.post("/api/auth/signup", { email, password });
  localStorage.setItem("token", data.token);
  return data.user;
}

export function logout() {
  localStorage.removeItem("token");
}

export function getStoredToken() {
  return localStorage.getItem("token");
}
