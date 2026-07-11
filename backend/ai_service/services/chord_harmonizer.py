import os
import re
import requests
from dotenv import load_dotenv
from music21 import converter, note, chord

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"


def _get_melody_notes(midi_path: str) -> list[str]:
    """Extract note names from melody MIDI."""
    try:
        score = converter.parse(midi_path)
        notes = []
        for el in score.flatten().notes:
            if isinstance(el, note.Note):
                notes.append(el.nameWithOctave)
            elif isinstance(el, chord.Chord):
                notes.append(el.pitches[-1].nameWithOctave)
        return notes[:40]  # limit to first 40 notes
    except Exception:
        return []


def _ask_ai(melody_notes: list[str], musical_key: str, bpm: float, style: str, total_measures: int) -> list[str]:
    """Send melody info to Mistral and get chord progression."""
    notes_str = ", ".join(melody_notes) if melody_notes else "unknown"

    prompt = f"""[INST] You are a professional music theorist and composer.
Given this melody information, generate a chord progression:

Musical key: {musical_key}
BPM: {bpm}
Style: {style}
Total measures needed: {total_measures}
Melody notes (first 40): {notes_str}

Rules:
1. Return ONLY a comma-separated list of chord symbols, one per measure
2. Use standard chord notation: C, Cm, C7, Cmaj7, Cm7, Cdim, Csus4, etc.
3. The chords must fit the melody notes and key
4. Match the style: {style}
5. Return exactly {total_measures} chords
6. No explanations, no numbering, just the chords

Example format: Am, F, C, G, Am, F, C, E [/INST]"""

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.7, "return_full_text": False}
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    raw = result[0]["generated_text"] if isinstance(result, list) else ""

    # Extract chord list from response
    chords = [c.strip() for c in re.split(r"[,\n]", raw) if c.strip()]
    chords = [c for c in chords if re.match(r"^[A-G][#b]?(m|maj7|m7|7|dim|sus4|sus2|aug)?$", c)]

    return chords


def _fallback_progression(musical_key: str, total_measures: int) -> list[str]:
    """Simple fallback if AI call fails."""
    parts = musical_key.split()
    tonic = parts[0]
    mode = parts[1] if len(parts) > 1 else "major"
    chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    root = chromatic.index(tonic) if tonic in chromatic else 0

    if mode == "minor":
        base = [tonic + "m", chromatic[(root + 3) % 12], chromatic[(root + 5) % 12] + "m", chromatic[(root + 7) % 12]]
    else:
        base = [tonic, chromatic[(root + 5) % 12], chromatic[(root + 7) % 12], chromatic[(root + 9) % 12] + "m"]

    return [base[i % len(base)] for i in range(total_measures)]


def harmonize_melody(
    musicxml_path: str,
    musical_key: str,
    midi_path: str = None,
    bpm: float = 120.0,
    style: str = "pop",
) -> dict:
    """
    Generate chord progression using Hugging Face Mistral AI model.
    Falls back to basic diatonic progression if API call fails.
    """
    score = converter.parse(musicxml_path)
    measures = [m for m in score.parts[0].getElementsByClass("Measure")
                if float(m.duration.quarterLength) > 0]
    total_measures = len(measures)

    melody_notes = _get_melody_notes(midi_path) if midi_path else []

    try:
        chords_list = _ask_ai(melody_notes, musical_key, bpm, style, total_measures)
        # Pad or trim to exact measure count
        if len(chords_list) < total_measures:
            chords_list += [chords_list[-1]] * (total_measures - len(chords_list))
        chords_list = chords_list[:total_measures]
    except Exception as e:
        print(f"[chord_harmonizer] AI call failed: {e}. Using fallback.")
        chords_list = _fallback_progression(musical_key, total_measures)

    seconds_per_beat = 60.0 / bpm
    progression = []
    offset_beats = 0.0

    for measure, chord_label in zip(measures, chords_list):
        duration_beats = float(measure.duration.quarterLength)
        progression.append({
            "measure": measure.number,
            "chord": chord_label,
            "offset_beats": offset_beats,
            "offset_seconds": round(offset_beats * seconds_per_beat, 3),
            "duration_beats": duration_beats,
        })
        offset_beats += duration_beats

    return {
        "progression": progression,
        "chords": chords_list,
        "musical_key": musical_key,
        "total_measures": total_measures,
    }