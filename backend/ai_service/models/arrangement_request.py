"""User request parameters for generating an arrangement"""

from dataclasses import dataclass, field


@dataclass
class ArrangementRequest:
    """Defines the parameters for a requested musical arrangement."""

    style: str
    difficulty: str
    instruments: list[str]
    voices_count: int
