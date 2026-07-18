from basic_pitch.inference import predict


def extract_accompaniment(other_path: str, bass_path: str) -> dict:
    """
    Transcribe basic accompaniment from Demucs stems to MIDI.

    Args:
        other_path: path to other.wav (chords/harmony instruments)
        bass_path:  path to bass.wav

    Returns:
        dict with other_midi_path and bass_midi_path
    """
    # נתיבי הפלט — אותה תיקייה כמו ה-wav, רק עם סיומת .mid
    other_midi_path = other_path.replace(".wav", ".mid")
    bass_midi_path  = bass_path.replace(".wav", ".mid")

    # המרת stem ה-"other" (כלי הרמוניה) ל-MIDI באמצעות Basic Pitch
    # _ = מתעלמים מ-model_output ו-note_events, רק שומרים את ה-MIDI
    _, other_midi, _ = predict(other_path)
    other_midi.write(other_midi_path)

    # המרת stem הבס ל-MIDI
    _, bass_midi, _ = predict(bass_path)
    bass_midi.write(bass_midi_path)

    return {
        "other_midi_path": other_midi_path,  # MIDI של כלי ההרמוניה
        "bass_midi_path":  bass_midi_path    # MIDI של הבס
    }
