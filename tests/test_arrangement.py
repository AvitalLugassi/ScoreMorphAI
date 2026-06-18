from backend.services.arrangement_engine import create_arrangement


melody = "data/midi/melody.mid"

chords = [
    "C",
    "Am",
    "F",
    "G"
]

bpm = 90


preferences = {
    "instruments": [
        "piano",
        "violin"
    ],
    "difficulty": "beginner"
}


result = create_arrangement(
    melody,
    chords,
    bpm,
    preferences
)


print(result)