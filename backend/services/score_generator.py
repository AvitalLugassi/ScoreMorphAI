from backend.services.music_processing_service import process_song
from backend.services.midi_builder import transcribe_to_scale
from backend.models.arrangement_request import ArrangementRequest


def generate(audio_path: str, request: ArrangementRequest) -> dict:
    """
    Main orchestrator for parts 1 and 2.
    Analyzes audio and transcribes melody to correct scale.

    Returns everything needed for part 3 (arrangement).
    """
    analysis = process_song(audio_path)

    musicxml_path = transcribe_to_scale(
        midi_path=analysis["midi_path"],
        musical_key=analysis["musical_key"]
    )

    return {
        "musicxml_path": musicxml_path,
        "musical_key": analysis["musical_key"],
        "bpm": analysis["bpm"],
        "chords": analysis["chords"],
        "style": request.style,
        "difficulty": request.difficulty,
        "instruments": request.instruments,
        "voices_count": request.voices_count
    }