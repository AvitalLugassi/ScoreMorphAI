from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum


class StyleEnum(str, Enum):
    classical = "classical"
    pop       = "pop"
    rock      = "rock"
    jazz      = "jazz"
    blues     = "blues"


class DifficultyEnum(str, Enum):
    easy   = "easy"
    medium = "medium"
    hard   = "hard"


class InstrumentEnum(str, Enum):
    piano      = "piano"
    guitar     = "guitar"
    bass       = "bass"
    strings    = "strings"
    brass      = "brass"
    reed       = "reed"
    synth_lead = "synth_lead"
    ensemble   = "ensemble"


VALID_VOICES = {2, 3, 4}


class ArrangementCreate(BaseModel):
    title:        Optional[str] = None
    style:        StyleEnum
    difficulty:   DifficultyEnum
    instruments:  list[InstrumentEnum]
    voices_count: int

    @field_validator("instruments")
    @classmethod
    def at_least_one_instrument(cls, v):
        if not v:
            raise ValueError("At least one instrument is required")
        return v

    @field_validator("voices_count")
    @classmethod
    def valid_voices(cls, v):
        if v not in VALID_VOICES:
            raise ValueError(f"voices_count must be one of {VALID_VOICES}")
        return v


class ArrangementResponse(BaseModel):
    id:           int
    title:        Optional[str]
    style:        str
    difficulty:   str
    instruments:  list[str]
    voices_count: int
    status:       str
    midi_path:    Optional[str]
    musicxml_path: Optional[str]
    pdf_path:     Optional[str]
    created_at:   datetime

    model_config = {"from_attributes": True}
