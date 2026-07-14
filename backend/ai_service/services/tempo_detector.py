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
    midi = pretty_midi.PrettyMIDI(midi_path)
    bpm = midi.estimate_tempo()
    return {"bpm": round(float(bpm), 2)}
