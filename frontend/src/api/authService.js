import { coreClient } from "./client";

export async function login(email, password) {
  const { data } = await coreClient.post("/auth/login", { email, password });
  localStorage.setItem("token", data.access_token);
  return data.user;
}

export async function signup(email, password) {
  const { data } = await coreClient.post("/auth/register", {
    email,
    username: email.split("@")[0],
    password,
  });
  localStorage.setItem("token", data.access_token);
  return data.user;
}

export function logout() {
  localStorage.removeItem("token");
}

export function getStoredToken() {
  return localStorage.getItem("token");
}
