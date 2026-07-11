import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { submitArrangement } from "../api/arrangementService";

// ── Enum constants matching backend ArrangementRequest ───────────────────────
const STYLES      = ["classical", "pop", "rock", "jazz", "blues"];
const DIFFICULTIES = ["easy", "medium", "hard"];
const INSTRUMENTS = ["piano", "guitar", "bass", "strings", "brass", "reed", "synth_lead", "ensemble"];
const VOICES      = [2, 3, 4];
const ACCEPTED_AUDIO = ["audio/mpeg", "audio/wav", "audio/flac", "audio/ogg", "audio/mp4"];

// ── Step sub-components ───────────────────────────────────────────────────────
function StepUpload({ register, errors }) {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Upload Audio</h2>
      <p className="text-gray-400 text-sm">Supported: MP3, WAV, FLAC, OGG, M4A (max 500 MB)</p>
      <input
        type="file"
        accept=".mp3,.wav,.flac,.ogg,.m4a"
        className="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-brand-600 file:text-white file:cursor-pointer hover:file:bg-brand-700"
        {...register("audioFile", {
          required: "Please upload an audio file",
          validate: {
            type: (files) =>
              ACCEPTED_AUDIO.includes(files[0]?.type) || "Unsupported file type",
            size: (files) =>
              files[0]?.size <= 500 * 1024 * 1024 || "File must be under 500 MB",
          },
        })}
      />
      {errors.audioFile && <p className="text-red-400 text-sm">{errors.audioFile.message}</p>}
    </div>
  );
}

function StepStyle({ register, errors }) {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Musical Style & Difficulty</h2>
      <div>
        <label className="block text-sm mb-2">Style</label>
        <div className="flex flex-wrap gap-2">
          {STYLES.map((s) => (
            <label key={s} className="cursor-pointer">
              <input type="radio" value={s} className="sr-only peer" {...register("style", { required: "Select a style" })} />
              <span className="px-4 py-2 rounded-full border border-gray-700 text-sm capitalize
                peer-checked:border-brand-500 peer-checked:bg-brand-500/20 peer-checked:text-brand-400 transition">
                {s}
              </span>
            </label>
          ))}
        </div>
        {errors.style && <p className="text-red-400 text-xs mt-1">{errors.style.message}</p>}
      </div>

      <div>
        <label className="block text-sm mb-2">Difficulty</label>
        <div className="flex gap-2">
          {DIFFICULTIES.map((d) => (
            <label key={d} className="cursor-pointer">
              <input type="radio" value={d} className="sr-only peer" {...register("difficulty", { required: "Select a difficulty" })} />
              <span className="px-4 py-2 rounded-full border border-gray-700 text-sm capitalize
                peer-checked:border-brand-500 peer-checked:bg-brand-500/20 peer-checked:text-brand-400 transition">
                {d}
              </span>
            </label>
          ))}
        </div>
        {errors.difficulty && <p className="text-red-400 text-xs mt-1">{errors.difficulty.message}</p>}
      </div>
    </div>
  );
}

function StepInstruments({ register, errors, watch }) {
  const selected = watch("instruments") || [];
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Instruments & Voices</h2>

      <div>
        <label className="block text-sm mb-2">
          Instruments <span className="text-gray-500">(select at least one)</span>
        </label>
        <div className="flex flex-wrap gap-2">
          {INSTRUMENTS.map((inst) => (
            <label key={inst} className="cursor-pointer">
              <input
                type="checkbox"
                value={inst}
                className="sr-only peer"
                {...register("instruments", {
                  validate: (v) => (v && v.length > 0) || "Select at least one instrument",
                })}
              />
              <span className={`px-4 py-2 rounded-full border text-sm capitalize transition
                ${selected.includes(inst)
                  ? "border-brand-500 bg-brand-500/20 text-brand-400"
                  : "border-gray-700 hover:border-gray-500"}`}>
                {inst.replace("_", " ")}
              </span>
            </label>
          ))}
        </div>
        {errors.instruments && <p className="text-red-400 text-xs mt-1">{errors.instruments.message}</p>}
      </div>

      <div>
        <label className="block text-sm mb-2">Number of Voices</label>
        <div className="flex gap-2">
          {VOICES.map((v) => (
            <label key={v} className="cursor-pointer">
              <input type="radio" value={v} className="sr-only peer"
                {...register("voices_count", { required: "Select voice count" })} />
              <span className="w-12 h-12 flex items-center justify-center rounded-full border border-gray-700 text-sm
                peer-checked:border-brand-500 peer-checked:bg-brand-500/20 peer-checked:text-brand-400 transition cursor-pointer">
                {v}
              </span>
            </label>
          ))}
        </div>
        {errors.voices_count && <p className="text-red-400 text-xs mt-1">{errors.voices_count.message}</p>}
      </div>
    </div>
  );
}

function StepReview({ getValues }) {
  const v = getValues();
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Review & Submit</h2>
      <div className="rounded-xl border border-gray-800 bg-gray-900 p-5 text-sm space-y-2">
        <p><span className="text-gray-400">File:</span> {v.audioFile?.[0]?.name}</p>
        <p><span className="text-gray-400">Style:</span> <span className="capitalize">{v.style}</span></p>
        <p><span className="text-gray-400">Difficulty:</span> <span className="capitalize">{v.difficulty}</span></p>
        <p><span className="text-gray-400">Instruments:</span> {v.instruments?.join(", ")}</p>
        <p><span className="text-gray-400">Voices:</span> {v.voices_count}</p>
      </div>
    </div>
  );
}

// ── Wizard shell ──────────────────────────────────────────────────────────────
const STEPS = ["Upload", "Style", "Instruments", "Review"];

export default function NewArrangement() {
  const [step, setStep] = useState(0);
  const [serverError, setServerError] = useState("");
  const navigate = useNavigate();

  const { register, handleSubmit, watch, getValues, trigger, formState: { errors, isSubmitting } } = useForm({
    defaultValues: { style: "classical", difficulty: "medium", voices_count: 4, instruments: [] },
  });

  // Fields to validate per step before advancing
  const STEP_FIELDS = [
    ["audioFile"],
    ["style", "difficulty"],
    ["instruments", "voices_count"],
  ];

  const next = async () => {
    const valid = await trigger(STEP_FIELDS[step]);
    if (valid) setStep((s) => s + 1);
  };

  const onSubmit = async (data) => {
    setServerError("");
    try {
      await submitArrangement({
        audioFile:   data.audioFile[0],
        style:       data.style,
        difficulty:  data.difficulty,
        instruments: data.instruments,
        voices_count: Number(data.voices_count),
      });
      navigate("/dashboard");
    } catch (e) {
      setServerError(e.response?.data?.error || "Submission failed. Please try again.");
    }
  };

  return (
    <div className="min-h-screen pt-24 px-6 max-w-xl mx-auto">
      {/* Progress bar */}
      <div className="flex items-center gap-2 mb-10">
        {STEPS.map((label, i) => (
          <div key={label} className="flex items-center gap-2 flex-1">
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition
              ${i < step ? "bg-brand-600 text-white" : i === step ? "bg-brand-500 text-white ring-2 ring-brand-400" : "bg-gray-800 text-gray-500"}`}>
              {i < step ? "✓" : i + 1}
            </div>
            <span className={`text-xs hidden sm:block ${i === step ? "text-white" : "text-gray-500"}`}>{label}</span>
            {i < STEPS.length - 1 && <div className={`flex-1 h-px ${i < step ? "bg-brand-600" : "bg-gray-800"}`} />}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="min-h-[260px]">
          {step === 0 && <StepUpload register={register} errors={errors} />}
          {step === 1 && <StepStyle  register={register} errors={errors} />}
          {step === 2 && <StepInstruments register={register} errors={errors} watch={watch} />}
          {step === 3 && <StepReview getValues={getValues} />}
        </div>

        {serverError && <p className="text-red-400 text-sm mt-4">{serverError}</p>}

        <div className="flex justify-between mt-8">
          {step > 0 ? (
            <button type="button" onClick={() => setStep((s) => s - 1)}
              className="px-5 py-2 rounded-full border border-gray-700 hover:border-gray-500 transition text-sm">
              ← Back
            </button>
          ) : <div />}

          {step < STEPS.length - 1 ? (
            <button type="button" onClick={next}
              className="px-5 py-2 rounded-full bg-brand-600 hover:bg-brand-700 transition text-sm font-medium">
              Next →
            </button>
          ) : (
            <button type="submit" disabled={isSubmitting}
              className="px-6 py-2 rounded-full bg-brand-600 hover:bg-brand-700 disabled:opacity-50 transition font-medium">
              {isSubmitting ? "Generating…" : "Generate Arrangement ✨"}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
