"""Song analysis result from audio processing pipeline"""

from dataclasses import dataclass


@dataclass
class SongAnalysis:
    """Holds all musical properties extracted and generated from an audio file."""

    melody_midi_path: str
    musicxml_path: str
    other_midi_path: str
    bass_midi_path: str
    arrangement_midi_path: str
    arrangement_musicxml_path: str
    pdf_path: str
    musical_key: str
    bpm: float
