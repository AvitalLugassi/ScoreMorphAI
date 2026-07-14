"""User request parameters for generating an arrangement"""

from dataclasses import dataclass
from enum import Enum

PAD_TOKEN = -1       # padding in input sequences (matches training)
OUTPUT_PAD = 128     # padding index in model output (NUM_CLASSES - 1)
MAX_TRACKS = 8
SEQ_LEN = 256


class Style(str, Enum):
    CLASSICAL = "classical"
    JAZZ = "jazz"
    POP = "pop"
    ROCK = "rock"
    BLUES = "blues"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Instrument(str, Enum):
    VIOLIN = "violin"
    CELLO = "cello"
    TRUMPET = "trumpet"
    FLUTE = "flute"
    PIANO = "piano"
    GUITAR = "guitar"
    BASS = "bass"
    DRUMS = "drums"


# MIDI program numbers per instrument (General MIDI standard)
INSTRUMENT_MIDI_MAP: dict[Instrument, int] = {
    Instrument.VIOLIN: 40,
    Instrument.CELLO: 42,
    Instrument.TRUMPET: 56,
    Instrument.FLUTE: 73,
    Instrument.PIANO: 0,
    Instrument.GUITAR: 25,
    Instrument.BASS: 32,
    Instrument.DRUMS: 118,
}


@dataclass
class ArrangementRequest:
    """Defines the parameters for a requested musical arrangement."""

    style: Style
    difficulty: Difficulty
    instruments: list[Instrument]
    voices_count: int
