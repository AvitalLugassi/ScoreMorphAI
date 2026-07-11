"""Output paths produced after arrangement generation"""

from dataclasses import dataclass


@dataclass
class ArrangementResult:
    """Holds the file paths of the generated arrangement outputs."""

    midi_path: str
    musicxml_path: str
    pdf_path: str
