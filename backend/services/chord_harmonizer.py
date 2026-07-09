import random
import numpy as np
import librosa
from music21 import converter, note, chord

# ─────────────────────────────────────────────
# Common progressions as scale degrees (Roman numerals → semitone intervals)
# Each tuple: (name, [scale_degree_intervals])
# Intervals relative to tonic in semitones (major scale degrees)
# ─────────────────────────────────────────────

MAJOR_PROGRESSIONS = [
    ("I-IV-V-I",       [0, 5, 7, 0]),
    ("I-V-vi-IV",      [0, 7, 9, 5]),
    ("I-IV-vi-V",      [0, 5, 9, 7]),
    ("I-vi-IV-V",      [0, 9, 5, 7]),
    ("I-vi-ii-V",      [0, 9, 2, 7]),
    ("I-IV-I-V",       [0, 5, 0, 7]),
    ("I-V-IV-V",       [0, 7, 5, 7]),
    ("ii-V-I",         [2, 7, 0]),
    ("I-iii-IV-V",     [0, 4, 5, 7]),
    ("I-IV-ii-V",      [0, 5, 2, 7]),
    ("I-V-vi-iii-IV",  [0, 7, 9, 4, 5]),
    ("I-IV-V-vi",      [0, 5, 7, 9]),
]

MINOR_PROGRESSIONS = [
    ("i-VII-VI-VII",   [0, 10, 8, 10]),
    ("i-iv-VII-III",   [0, 5, 10, 3]),
    ("i-VI-III-VII",   [0, 8, 3, 10]),
    ("i-iv-v-i",       [0, 5, 7, 0]),
    ("i-VI-VII-i",     [0, 8, 10, 0]),
    ("i-III-VII-VI",   [0, 3, 10, 8]),
    ("i-v-VI-VII",     [0, 7, 8, 10]),
    ("i-iv-i-V",       [0, 5, 0, 7]),
    ("i-VI-III-iv",    [0, 8, 3, 5]),
    ("i-VII-VI-V",     [0, 10, 8, 7]),
    ("i-iv-VII-VI",    [0, 5, 10, 8]),
    ("i-III-VI-VII",   [0, 3, 8, 10]),
]

# Chord quality per interval in major/minor context
MAJOR_QUALITIES = {0: "", 2: "m", 4: "m", 5: "", 7: "", 9: "m", 10: "", 11: "dim"}
MINOR_QUALITIES = {0: "m", 2: "dim", 3: "", 5: "m", 7: "m", 8: "", 10: ""}

CHROMATIC = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

ENHARMONICS = {
    "Db": "C#", "Eb": "D#", "Fb": "E", "Gb": "F#",
    "Ab": "G#", "Bb": "A#", "Cb": "B",
    "E#": "F", "B#": "C",
}


def _normalize_tonic(tonic: str) -> str:
    return ENHARMONICS.get(tonic, tonic)


def _build_chord_label(root_idx: int, interval: int, mode: str) -> str:
    note_idx = (root_idx + interval) % 12
    root_name = CHROMATIC[note_idx]
    qualities = MAJOR_QUALITIES if mode == "major" else MINOR_QUALITIES
    quality = qualities.get(interval, "m")
    return root_name + quality


def _progression_to_chords(intervals: list[int], root_idx: int, mode: str) -> list[str]:
    return [_build_chord_label(root_idx, i, mode) for i in intervals]


def _melody_fits_chord(chord_label: str, melody_pitch_classes: set[int]) -> float:
    """Score how well a chord fits the melody pitch classes (0.0–1.0)."""
    if not melody_pitch_classes:
        return 1.0

    root_name = chord_label.rstrip("m").rstrip("dim")
    if root_name not in CHROMATIC:
        return 0.5

    root = CHROMATIC.index(root_name)
    is_minor = chord_label.endswith("m") and not chord_label.endswith("dim")
    is_dim = chord_label.endswith("dim")

    if is_dim:
        chord_pcs = {root % 12, (root + 3) % 12, (root + 6) % 12}
    elif is_minor:
        chord_pcs = {root % 12, (root + 3) % 12, (root + 7) % 12}
    else:
        chord_pcs = {root % 12, (root + 4) % 12, (root + 7) % 12}

    overlap = len(chord_pcs & melody_pitch_classes)
    return overlap / len(chord_pcs)


def _get_melody_pitch_classes(midi_path: str) -> set[int]:
    """Extract all pitch classes from the melody MIDI."""
    try:
        score = converter.parse(midi_path)
        pcs = set()
        for element in score.flatten().notes:
            if isinstance(element, note.Note):
                pcs.add(element.pitch.midi % 12)
            elif isinstance(element, chord.Chord):
                for p in element.pitches:
                    pcs.add(p.midi % 12)
        return pcs
    except Exception:
        return set()


def _select_best_progression(
    progressions: list[tuple],
    root_idx: int,
    mode: str,
    melody_pcs: set[int],
) -> tuple[str, list[str]]:
    """Score all progressions against melody and pick the best fitting one."""
    best_name, best_chords, best_score = progressions[0][0], [], -1.0

    for name, intervals in progressions:
        chords = _progression_to_chords(intervals, root_idx, mode)
        score = np.mean([_melody_fits_chord(c, melody_pcs) for c in chords])
        if score > best_score:
            best_score, best_name, best_chords = score, name, chords

    return best_name, best_chords


def _expand_progression(base_chords: list[str], total_measures: int,
                        root_idx: int, mode: str) -> list[str]:
    """
    Build a full song structure with varied sections:
    intro → verse → chorus → verse → chorus → bridge → chorus → outro
    Each section uses a related but different progression.
    """
    progressions = MINOR_PROGRESSIONS if mode == "minor" else MAJOR_PROGRESSIONS
    phrase = len(base_chords)

    # Pick 3 different progressions for verse / chorus / bridge
    scored = []
    for name, intervals in progressions:
        chords = _progression_to_chords(intervals, root_idx, mode)
        scored.append((name, chords))

    # Ensure we have at least 3 distinct progressions
    verse_chords   = scored[0][1]
    chorus_chords  = scored[1][1] if len(scored) > 1 else scored[0][1]
    bridge_chords  = scored[2][1] if len(scored) > 2 else scored[0][1]

    # Song structure — proportional to total_measures
    # Each "block" = one repetition of a 4-chord phrase
    section_sizes = {
        "intro":   max(1, total_measures // 10),
        "verse1":  max(2, total_measures // 5),
        "chorus1": max(2, total_measures // 5),
        "verse2":  max(2, total_measures // 5),
        "chorus2": max(2, total_measures // 5),
        "bridge":  max(1, total_measures // 8),
        "outro":   max(1, total_measures // 10),
    }

    section_progressions = {
        "intro":   verse_chords,
        "verse1":  verse_chords,
        "chorus1": chorus_chords,
        "verse2":  verse_chords,
        "chorus2": chorus_chords,
        "bridge":  bridge_chords,
        "outro":   verse_chords,
    }

    result = []
    for section, size in section_sizes.items():
        prog = section_progressions[section]
        measures_added = 0
        while measures_added < size:
            for chord in prog:
                if measures_added >= size:
                    break
                result.append(chord)
                measures_added += 1

    # Trim or pad to exact total_measures
    if len(result) > total_measures:
        result = result[:total_measures]
    while len(result) < total_measures:
        result.append(verse_chords[len(result) % len(verse_chords)])

    return result


def harmonize_melody(
    musicxml_path: str,
    musical_key: str,
    midi_path: str = None,
    bpm: float = 120.0,
) -> dict:
    """
    Generate a musical chord progression based on key, song length,
    and optionally the melody MIDI for best-fit selection.

    Args:
        musicxml_path: path to MusicXML (to count measures)
        musical_key:   string like 'C# minor' or 'A major'
        midi_path:     path to melody MIDI for fit scoring (optional)
        bpm:           tempo in BPM

    Returns:
        dict with chord progression data
    """
    parts = musical_key.split()
    tonic = _normalize_tonic(parts[0])
    mode = parts[1] if len(parts) > 1 else "major"

    if tonic not in CHROMATIC:
        tonic = "C"
    root_idx = CHROMATIC.index(tonic)

    # Count measures from MusicXML
    score = converter.parse(musicxml_path)
    measures = [m for m in score.parts[0].getElementsByClass("Measure")
                if float(m.duration.quarterLength) > 0]
    total_measures = len(measures)

    # Get melody pitch classes for fit scoring
    melody_pcs = _get_melody_pitch_classes(midi_path) if midi_path else set()

    # Select best-fitting progression from database
    progressions = MINOR_PROGRESSIONS if mode == "minor" else MAJOR_PROGRESSIONS
    prog_name, base_chords = _select_best_progression(progressions, root_idx, mode, melody_pcs)

    # Expand to fill all measures with song structure
    full_progression = _expand_progression(base_chords, total_measures, root_idx, mode)

    # Build output with timestamps
    seconds_per_beat = 60.0 / bpm
    progression = []
    offset_beats = 0.0

    for i, (measure, chord_label) in enumerate(zip(measures, full_progression)):
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
        "chords": full_progression,
        "progression_name": prog_name,
        "musical_key": musical_key,
        "total_measures": total_measures,
    }
