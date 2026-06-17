"""User preferences for arrangement output"""

from dataclasses import dataclass


@dataclass
class UserPreferences:
    """Stores the user's personal preferences for arrangement generation."""

    preferred_style: str
    preferred_difficulty: str
    preferred_instruments: list[str]
    default_voices_count: int
