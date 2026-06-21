import librosa
from basic_pitch.inference import predict

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def detect_key(audio_path: str) -> str:
    """
    Detect musical key from audio using chroma energy.
    Returns key string like 'C major' or 'A minor'.
    """
    y, sr = librosa.load(audio_path)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    # Krumhansl-Schmuckler key profiles
    major_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
    minor_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

    best_key, best_mode, best_score = 0, "major", -float("inf")
    for i in range(12):
        rotated = [chroma_mean[(i + j) % 12] for j in range(12)]
        major_score = sum(a * b for a, b in zip(rotated, major_profile))
        minor_score = sum(a * b for a, b in zip(rotated, minor_profile))
        if major_score > best_score:
            best_score, best_key, best_mode = major_score, i, "major"
        if minor_score > best_score:
            best_score, best_key, best_mode = minor_score, i, "minor"

    return f"{NOTE_NAMES[best_key]} {best_mode}"


def extract_melody(audio_path: str):
    """
    Extract melody from audio file and convert it to MIDI.
    Also detects the musical key.

    Parameters:
        audio_path (str): path to mp3/wav file

    Returns:
        dict containing midi_path, note_count, and musical_key
    """
    model_output, midi_data, note_events = predict(audio_path)

    output_path = "data/midi/melody.mid"
    midi_data.write(output_path)

    musical_key = detect_key(audio_path)

    return {
        "midi_path": output_path,
        "note_count": len(note_events),
        "musical_key": musical_key
    }