from backend.services.source_separator import SourceSeparator
from backend.services.melody_extractor import extract_melody
from backend.services.chord_detector import detect_chords
from backend.services.tempo_detector import detect_tempo


def process_song(audio_path: str) -> dict:
    separated_tracks = SourceSeparator().separate(audio_path)

    melody = extract_melody(separated_tracks["vocals"])

    chords = detect_chords(audio_path)

    tempo_info = detect_tempo(audio_path)

    return {
        "midi_path": melody["midi_path"],
        "note_count": melody["note_count"],
        "musical_key": melody["musical_key"],
        "chords": chords,
        "bpm": tempo_info["bpm"]
    }