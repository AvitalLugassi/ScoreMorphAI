import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchArrangements, exportScore } from "../api/arrangementService";
import StatusBadge from "../components/StatusBadge";

export default function Dashboard() {
  const [arrangements, setArrangements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchArrangements()
      .then(setArrangements)
      .catch(() => setError("Could not load arrangements."))
      .finally(() => setLoading(false));
  }, []);

  const handleExport = async (id, format) => {
    const blob = await exportScore(id, format);
    const url = URL.createObjectURL(blob);
    Object.assign(document.createElement("a"), { href: url, download: `score-${id}.${format}` }).click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen pt-24 px-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold">My Arrangements</h1>
        <Link to="/new" className="px-4 py-2 rounded-full bg-brand-600 hover:bg-brand-700 transition text-sm font-medium">
          + New Arrangement
        </Link>
      </div>

      {loading && <p className="text-gray-400">Loading…</p>}
      {error   && <p className="text-red-400">{error}</p>}

      {!loading && !error && arrangements.length === 0 && (
        <div className="text-center py-24 text-gray-500">
          <p className="text-4xl mb-4">🎵</p>
          <p className="mb-4">No arrangements yet.</p>
          <Link to="/new" className="text-brand-500 hover:underline">Create your first one →</Link>
        </div>
      )}

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {arrangements.map((a) => (
          <div key={a.id} className="rounded-xl border border-gray-800 bg-gray-900 p-5 flex flex-col gap-3">
            <div className="flex items-start justify-between">
              <h3 className="font-medium truncate">{a.title || `Arrangement #${a.id}`}</h3>
              <StatusBadge status={a.status} />
            </div>
            <div className="text-xs text-gray-500 space-y-0.5">
              <p>Style: <span className="text-gray-300 capitalize">{a.style}</span></p>
              <p>Difficulty: <span className="text-gray-300 capitalize">{a.difficulty}</span></p>
              <p>Instruments: <span className="text-gray-300">{a.instruments?.join(", ")}</span></p>
              <p>Voices: <span className="text-gray-300">{a.voices_count}</span></p>
            </div>
            {a.status === "completed" && (
              <div className="flex gap-2 flex-wrap mt-auto">
                {["pdf", "midi", "musicxml"].map((fmt) => (
                  <button key={fmt} onClick={() => handleExport(a.id, fmt)}
                    className="px-2.5 py-1 rounded text-xs border border-gray-700 hover:border-brand-500 hover:text-brand-400 transition uppercase">
                    {fmt}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
