"""Song analysis result from audio processing"""

from dataclasses import dataclass, field


@dataclass
class SongAnalysis:
    """Holds the analyzed musical properties extracted from an audio file."""

    melody_midi_path: str
    chords: list[str]
    bpm: float
    musical_key: str
