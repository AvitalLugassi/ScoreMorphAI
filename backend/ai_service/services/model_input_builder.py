"""Converts MIDI files and user preferences into model input tensors."""

import pretty_midi
import torch
from models.arrangement_request import (
    ArrangementRequest, Style, Difficulty,
    INSTRUMENT_MIDI_MAP, PAD_TOKEN, OUTPUT_PAD, MAX_TRACKS, SEQ_LEN
)

# רשימות הערכים האפשריים לסגנון ולקושי — לבניית וקטורי one-hot
_STYLES      = [s.value for s in Style]
_DIFFICULTIES = [d.value for d in Difficulty]


def _midi_to_note_sequence(midi_path: str) -> list[int]:
    """Extract a flat sequence of MIDI pitch values, padded to SEQ_LEN."""
    midi  = pretty_midi.PrettyMIDI(midi_path)
    notes = []

    # איסוף כל התווים מכל הכלים, ממוינים לפי זמן התחלה
    for instrument in midi.instruments:
        for note in sorted(instrument.notes, key=lambda n: n.start):
            notes.append(note.pitch)  # pitch = ערך MIDI בין 0-127

    # חיתוך לאורך מקסימלי (SEQ_LEN=256 תווים)
    notes = notes[:SEQ_LEN]

    # ריפוד ב-PAD_TOKEN (-1) כדי להגיע לאורך אחיד
    notes += [PAD_TOKEN] * (SEQ_LEN - len(notes))
    return notes


def _build_global_cond(request: ArrangementRequest) -> list[float]:
    """Build the 10-element conditioning vector from user preferences."""
    # one-hot encoding לסגנון (5 ערכים): למשל classical → [1,0,0,0,0]
    style_onehot = [1.0 if request.style.value == s else 0.0 for s in _STYLES]

    # one-hot encoding לקושי (3 ערכים): למשל medium → [0,1,0]
    difficulty_onehot = [1.0 if request.difficulty.value == d else 0.0 for d in _DIFFICULTIES]

    # נרמול מספר הקולות לטווח [0,1]: 4 קולות → 1.0
    voices_norm = [request.voices_count / 4.0]

    # נרמול מספר הכלים לטווח [0,1]: 8 כלים → 1.0
    instruments_norm = [len(request.instruments) / float(MAX_TRACKS)]

    # וקטור סופי באורך 10: [5 style + 3 difficulty + 1 voices + 1 instruments]
    return style_onehot + difficulty_onehot + voices_norm + instruments_norm


def _build_inst_indices(request: ArrangementRequest) -> list[int]:
    """Build the 8-slot instrument index list, padded with PAD_TOKEN (-1).
    The transformer converts -1 → 128 internally before embedding.
    """
    # המרת שמות הכלים למספרי תוכנית MIDI (0-127)
    indices  = [INSTRUMENT_MIDI_MAP[inst] for inst in request.instruments[:MAX_TRACKS]]

    # ריפוד ל-8 slots קבועים (MAX_TRACKS)
    indices += [PAD_TOKEN] * (MAX_TRACKS - len(indices))
    return indices


def build_model_inputs(
    melody_midi_path:  str,
    harmony_midi_path: str,
    request:           ArrangementRequest,
    device:            torch.device
) -> dict[str, torch.Tensor]:
    """
    Prepare all model input tensors from MIDI files and user preferences.

    Args:
        melody_midi_path:  path to melody MIDI (vocals stem)
        harmony_midi_path: path to accompaniment MIDI (other stem)
        request:           user arrangement preferences
        device:            torch device (cpu or cuda)

    Returns:
        dict with keys: melody_in, harmony_guide, global_cond, inst_indices
    """
    melody_seq   = _midi_to_note_sequence(melody_midi_path)
    harmony_seq  = _midi_to_note_sequence(harmony_midi_path)
    global_cond  = _build_global_cond(request)
    inst_indices = _build_inst_indices(request)

    # המרה ל-tensors והוספת batch dimension (unsqueeze(0)) → shape: [1, SEQ_LEN]
    return {
        "melody_in":     torch.tensor(melody_seq,   dtype=torch.long).unsqueeze(0).to(device),
        "harmony_guide": torch.tensor(harmony_seq,  dtype=torch.long).unsqueeze(0).to(device),
        "global_cond":   torch.tensor(global_cond,  dtype=torch.float32).unsqueeze(0).to(device),
        "inst_indices":  torch.tensor(inst_indices, dtype=torch.long).unsqueeze(0).to(device),
    }
