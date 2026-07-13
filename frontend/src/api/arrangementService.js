import { coreClient, aiClient } from "./client";

export async function submitArrangement({ audioFile, style, difficulty, instruments, voices_count }) {
  const form = new FormData();
  form.append("file", audioFile);
  form.append("style", style);
  form.append("difficulty", difficulty);
  instruments.forEach((inst) => form.append("instruments", inst));
  form.append("voices_count", String(voices_count));

  const { data } = await aiClient.post("/api/upload/audio", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function fetchArrangements() {
  const { data } = await coreClient.get("/arrangements");
  return data;
}

export async function exportScore(scoreId, format = "pdf") {
  const { data } = await aiClient.get(`/api/export/score/${scoreId}`, {
    params: { format },
    responseType: "blob",
  });
  return data;
}
