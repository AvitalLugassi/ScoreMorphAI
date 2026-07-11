import { useState } from "react";
import { Link } from "react-router-dom";

// ─── Interactive Demo Simulation ────────────────────────────────────────────
const DEMO_STEPS = [
  { label: "Upload Audio",      icon: "🎵", desc: "Drop your MP3, WAV, or FLAC file" },
  { label: "Choose Style",      icon: "🎼", desc: "Classical · Pop · Rock · Jazz · Blues" },
  { label: "Pick Instruments",  icon: "🎹", desc: "Piano, Violin, Guitar, Brass & more" },
  { label: "Generate Score",    icon: "✨", desc: "AI arranges your music in seconds" },
];

function DemoSimulator() {
  const [active, setActive] = useState(0);
  const [done, setDone] = useState(false);

  const next = () => {
    if (active < DEMO_STEPS.length - 1) setActive((p) => p + 1);
    else setDone(true);
  };
  const reset = () => { setActive(0); setDone(false); };

  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900 p-6 max-w-lg mx-auto">
      {/* Step indicators */}
      <div className="flex justify-between mb-6">
        {DEMO_STEPS.map((s, i) => (
          <div key={i} className="flex flex-col items-center gap-1 flex-1">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm transition-all
              ${i < active ? "bg-brand-600 text-white" : i === active ? "bg-brand-500 text-white ring-2 ring-brand-400" : "bg-gray-800 text-gray-500"}`}>
              {i < active ? "✓" : i + 1}
            </div>
            <span className={`text-xs hidden sm:block ${i === active ? "text-white" : "text-gray-500"}`}>{s.label}</span>
          </div>
        ))}
      </div>

      {/* Active step card */}
      {!done ? (
        <div className="text-center py-6">
          <div className="text-5xl mb-3">{DEMO_STEPS[active].icon}</div>
          <h3 className="text-lg font-semibold mb-1">{DEMO_STEPS[active].label}</h3>
          <p className="text-gray-400 text-sm mb-6">{DEMO_STEPS[active].desc}</p>
          <button onClick={next}
            className="px-6 py-2 rounded-full bg-brand-600 hover:bg-brand-700 transition font-medium text-sm">
            {active < DEMO_STEPS.length - 1 ? "Next →" : "Generate"}
          </button>
        </div>
      ) : (
        <div className="text-center py-6">
          <div className="text-5xl mb-3">🎉</div>
          <h3 className="text-lg font-semibold mb-1">Your score is ready!</h3>
          <p className="text-gray-400 text-sm mb-6">Download as PDF, MusicXML, or MIDI</p>
          <button onClick={reset} className="text-brand-500 hover:text-brand-400 text-sm underline">
            Try again
          </button>
        </div>
      )}
    </div>
  );
}

// ─── Landing Page ────────────────────────────────────────────────────────────
export default function Landing() {
  return (
    <main className="pt-20">
      {/* ── Hero ── */}
      <section className="min-h-screen flex flex-col items-center justify-center text-center px-6 py-24 gap-6">
        <span className="px-3 py-1 rounded-full bg-brand-500/20 text-brand-500 text-xs font-medium tracking-wide uppercase">
          AI-Powered Music Arrangement
        </span>
        <h1 className="text-5xl sm:text-6xl font-extrabold leading-tight max-w-3xl">
          Transform Any Audio Into a{" "}
          <span className="text-brand-500">Professional Score</span>
        </h1>
        <p className="text-gray-400 max-w-xl text-lg">
          {/* ── PLACEHOLDER: Replace with your custom hero subtitle ── */}
          Upload a melody, choose your style and instruments — ScoreMorphAI handles the rest.
        </p>
        <div className="flex gap-3 flex-wrap justify-center">
          <Link to="/signup" className="px-6 py-3 rounded-full bg-brand-600 hover:bg-brand-700 transition font-semibold">
            Start for Free
          </Link>
          <a href="#demo" className="px-6 py-3 rounded-full border border-gray-700 hover:border-gray-500 transition font-semibold">
            See How It Works
          </a>
        </div>
      </section>

      {/* ── About / Intro ── */}
      <section className="max-w-3xl mx-auto px-6 py-20 text-center" id="about">
        <h2 className="text-3xl font-bold mb-6">Our Story</h2>
        {/* ── PLACEHOLDER: Replace the paragraphs below with your custom story ── */}
        <p className="text-gray-400 leading-relaxed mb-4">
          [PLACEHOLDER — Where the project started: describe the origin story, the problem you set out to solve, and the team behind ScoreMorphAI.]
        </p>
        <p className="text-gray-400 leading-relaxed">
          [PLACEHOLDER — Vision: describe where you want to take this product and what impact you hope to have on musicians, composers, and learners worldwide.]
        </p>
      </section>

      {/* ── Interactive Demo ── */}
      <section className="max-w-2xl mx-auto px-6 py-20" id="demo">
        <h2 className="text-3xl font-bold text-center mb-10">See It In Action</h2>
        <DemoSimulator />
      </section>

      {/* ── Features ── */}
      <section className="max-w-5xl mx-auto px-6 py-20 grid sm:grid-cols-3 gap-6">
        {[
          { icon: "🎸", title: "8 Instrument Types", body: "Piano, Guitar, Bass, Strings, Brass, Reed, Synth Lead, Ensemble" },
          { icon: "🎭", title: "5 Musical Styles",   body: "Classical, Pop, Rock, Jazz, Blues — each with its own voicing logic" },
          { icon: "📄", title: "Multiple Exports",   body: "Download your arrangement as PDF, MusicXML, MIDI, or PNG" },
        ].map((f) => (
          <div key={f.title} className="rounded-xl border border-gray-800 bg-gray-900 p-6">
            <div className="text-3xl mb-3">{f.icon}</div>
            <h3 className="font-semibold mb-2">{f.title}</h3>
            <p className="text-gray-400 text-sm">{f.body}</p>
          </div>
        ))}
      </section>

      {/* ── CTA ── */}
      <section className="text-center px-6 py-24">
        <h2 className="text-3xl font-bold mb-4">Ready to arrange your music?</h2>
        <Link to="/signup" className="px-8 py-3 rounded-full bg-brand-600 hover:bg-brand-700 transition font-semibold text-lg">
          Get Started Free
        </Link>
      </section>
    </main>
  );
}
