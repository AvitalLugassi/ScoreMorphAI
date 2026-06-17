import librosa


def detect_tempo(audio_path):
    """
    Detect BPM from audio file.
    """

    y, sr = librosa.load(audio_path)

    tempo, _ = librosa.beat.beat_track(
        y=y,
        sr=sr
    )

    return {
        "bpm": round(float(tempo[0] if hasattr(tempo, '__len__') else tempo), 2)
    }