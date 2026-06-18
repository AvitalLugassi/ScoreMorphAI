from backend.services.source_separator import separate_sources
from backend.services.melody_extractor import extract_melody
from backend.services.chord_detector import detect_chords
from backend.services.tempo_detector import detect_tempo


def process_song(audio_path):

    separated_tracks = separate_sources(audio_path)

    melody = extract_melody(separated_tracks["vocals"])

    chords = detect_chords(audio_path)
# KEY
    tempo_info = detect_tempo(audio_path)

    return {
        "melody": melody,
        "chords": chords,# KEY
        "tempo": tempo_info
    }