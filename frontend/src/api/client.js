import axios from "axios";

function makeClient(baseURL) {
  const client = axios.create({ baseURL });

  client.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  });

  client.interceptors.response.use(
    (res) => res,
    (err) => {
      if (err.response?.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
      return Promise.reject(err);
    }
  );

  return client;
}

export const coreClient = makeClient(
  process.env.REACT_APP_CORE_API_URL || "http://127.0.0.1:8000"
);

export const aiClient = makeClient(
  process.env.REACT_APP_AI_API_URL || "http://127.0.0.1:5000"
);

export default coreClient;
