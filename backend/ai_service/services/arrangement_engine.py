def create_arrangement(
    melody,
    chords,
    bpm,
    preferences
):
    """
    Creates a new musical arrangement
    based on extracted music data
    and user preferences.
    """

    arrangement = {
        "tempo": bpm,
        "melody": melody,
        "chords": chords,
        "instruments": preferences["instruments"],
        "difficulty": preferences["difficulty"]
    }

    return arrangement