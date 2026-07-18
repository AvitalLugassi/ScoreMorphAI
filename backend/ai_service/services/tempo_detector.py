import pretty_midi


def detect_tempo(midi_path: str) -> dict:
    """
    Extract BPM from a MIDI file produced by Basic Pitch.
    Consistent with the MIDI that will be used for MusicXML generation.

    Args:
        midi_path: path to MIDI file

    Returns:
        dict with bpm (float)
    """
    # טעינת קובץ ה-MIDI עם pretty_midi
    midi = pretty_midi.PrettyMIDI(midi_path)

    # estimate_tempo() מחשב BPM על בסיס הצפיפות של התווים בזמן
    # (אלגוריתם autocorrelation על ה-onset times)
    bpm = midi.estimate_tempo()

    # עיגול ל-2 ספרות אחרי הנקודה לנוחות השימוש
    return {"bpm": round(float(bpm), 2)}
