import librosa


def detect_chords(audio_path):
    """
    Detect chord progression from audio file.

    Returns:
        list of detected chords
    """

    y, sr = librosa.load(audio_path)


    chroma = librosa.feature.chroma_cqt(
        y=y,
        sr=sr
    )


    # placeholder for chord estimation
    # next step: add chord recognition model

    chords = [
        "C",
        "Am",
        "F",
        "G"
    ]

    return chords