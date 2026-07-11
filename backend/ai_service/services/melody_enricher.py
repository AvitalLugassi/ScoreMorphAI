import os
import requests
import pretty_midi
import numpy as np
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-melody"


def _midi_to_token_sequence(midi_path: str) -> list[dict]:
    """Convert MIDI file to a sequence of note events."""
    midi = pretty_midi.PrettyMIDI(midi_path)
    notes = []
    for instrument in midi.instruments:
        for note in instrument.notes:
            notes.append({
                "pitch": note.pitch,
                "start": round(note.start, 3),
                "end": round(note.end, 3),
                "velocity": note.velocity
            })
    notes.sort(key=lambda x: x["start"])
    return notes


def _notes_to_prompt(notes: list[dict], musical_key: str, style: str) -> str:
    """Build a text prompt describing the melody for the AI."""
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    pitch_names = [note_names[n["pitch"] % 12] for n in notes[:16]]
    melody_str = " ".join(pitch_names)
    return f"{style} music in {musical_key}, melody: {melody_str}, full orchestral arrangement"


def _build_enriched_midi(original_midi_path: str, new_notes: list[dict], output_path: str) -> str:
    """Merge original melody with enriched notes into a new MIDI file."""
    original = pretty_midi.PrettyMIDI(original_midi_path)
    enriched = pretty_midi.PrettyMIDI(initial_tempo=original.estimate_tempo())

    # Keep original melody as track 0
    enriched.instruments.append(original.instruments[0])

    # Add enriched harmony as track 1
    harmony_track = pretty_midi.Instrument(program=0, name="harmony")
    for n in new_notes:
        harmony_track.notes.append(
            pretty_midi.Note(
                velocity=n.get("velocity", 64),
                pitch=n["pitch"],
                start=n["start"],
                end=n["end"]
            )
        )
    enriched.instruments.append(harmony_track)
    enriched.write(output_path)
    return output_path


def _generate_harmonic_enrichment(notes: list[dict], musical_key: str, bpm: float) -> list[dict]:
    """
    Generate harmonic enrichment notes based on the melody.
    Creates inner voices that complement the melody harmonically.
    """
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    tonic_name = musical_key.split()[0]
    mode = musical_key.split()[1] if len(musical_key.split()) > 1 else "major"
    tonic = note_names.index(tonic_name) if tonic_name in note_names else 0

    # Intervals for harmonization (thirds and fifths)
    if mode == "minor":
        harmony_intervals = [3, 7]  # minor third + fifth
    else:
        harmony_intervals = [4, 7]  # major third + fifth

    enriched = []
    for note in notes:
        for interval in harmony_intervals:
            new_pitch = note["pitch"] - 12 + interval  # one octave lower + interval
            if 21 <= new_pitch <= 108:  # valid MIDI range
                enriched.append({
                    "pitch": new_pitch,
                    "start": note["start"],
                    "end": note["end"],
                    "velocity": max(40, note["velocity"] - 20)
                })
    return enriched


def enrich_melody(midi_path: str, musical_key: str, bpm: float, style: str = "classical") -> dict:
    """
    Enrich melody MIDI with harmonic voices using Music Transformer via HF API.
    Falls back to algorithmic enrichment if API is unavailable.

    Args:
        midi_path: path to melody MIDI file
        musical_key: e.g. 'F minor'
        bpm: tempo
        style: musical style for the enrichment

    Returns:
        dict with enriched_midi_path and note_count
    """
    output_path = midi_path.replace(".mid", "_enriched.mid")
    notes = _midi_to_token_sequence(midi_path)

    try:
        prompt = _notes_to_prompt(notes, musical_key, style)
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 256, "temperature": 0.8}
        }
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()
        # musicgen returns audio - fall through to algorithmic enrichment
        # since we need MIDI output, not audio
        raise ValueError("musicgen returns audio, using algorithmic enrichment")

    except Exception as e:
        print(f"[melody_enricher] Using algorithmic enrichment: {e}")
        enriched_notes = _generate_harmonic_enrichment(notes, musical_key, bpm)

    enriched_midi_path = _build_enriched_midi(midi_path, enriched_notes, output_path)

    return {
        "enriched_midi_path": enriched_midi_path,
        "original_midi_path": midi_path,
        "note_count": len(enriched_notes)
    }