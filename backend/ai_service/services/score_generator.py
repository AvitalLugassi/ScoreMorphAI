from backend.services.music_processing_service import process_song
from backend.models.arrangement_request import ArrangementRequest


def generate(audio_path: str, request: ArrangementRequest) -> dict:
    """
    Main orchestrator for parts 1 and 2.
    Analyzes audio, extracts melody, detects key/tempo,
    and generates a diatonic chord progression from the melody.

    Returns everything needed for part 3 (arrangement).
    """
    analysis = process_song(audio_path)

    return {
        "musicxml_path": analysis["musicxml_path"],
        "musical_key": analysis["musical_key"],
        "bpm": analysis["bpm"],
        "chords": analysis["chords"],
        "chord_progression": analysis["chord_progression"],
        "style": request.style,
        "difficulty": request.difficulty,
        "instruments": request.instruments,
        "voices_count": request.voices_count
    }