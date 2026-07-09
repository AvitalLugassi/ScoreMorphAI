from backend.services.source_separator import SourceSeparator
from backend.services.melody_extractor import extract_melody
from backend.services.chord_harmonizer import harmonize_melody
from backend.services.tempo_detector import detect_tempo
from backend.services.midi_builder import transcribe_to_scale


def process_song(audio_path: str) -> dict:
    separated_tracks = SourceSeparator().separate(audio_path)

    melody = extract_melody(separated_tracks["vocals"])

    tempo_info = detect_tempo(audio_path)

    musicxml_path = transcribe_to_scale(
        midi_path=melody["midi_path"],
        musical_key=melody["musical_key"]
    )

    harmony = harmonize_melody(
        musicxml_path,
        melody["musical_key"],
        midi_path=melody["midi_path"],
        bpm=tempo_info["bpm"],
    )

    return {
        "midi_path": melody["midi_path"],
        "musicxml_path": musicxml_path,
        "note_count": melody["note_count"],
        "musical_key": melody["musical_key"],
        "chords": harmony["chords"],
        "chord_progression": harmony["progression"],
        "bpm": tempo_info["bpm"]
    }