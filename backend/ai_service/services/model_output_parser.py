"""Converts model output tensor into a MIDI file."""

import numpy as np
import pretty_midi
from models.arrangement_request import ArrangementRequest, INSTRUMENT_MIDI_MAP, OUTPUT_PAD


def parse_model_output(predictions: np.ndarray, request: ArrangementRequest, bpm: float, output_path: str) -> str:
    """
    Convert model predictions [8, 256] into a MIDI file.

    Args:
        predictions: numpy array of shape [8, 256] with MIDI pitch values
        request:     user arrangement preferences (for instrument mapping)
        bpm:         tempo for the output MIDI
        output_path: where to save the generated MIDI file

    Returns:
        path to the generated MIDI file
    """
    seconds_per_step = 60.0 / bpm / 4  # 16th note resolution

    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)

    for track_idx, instrument in enumerate(request.instruments):
        program = INSTRUMENT_MIDI_MAP[instrument]
        is_drum = instrument.value == "drums"
        track = pretty_midi.Instrument(program=program, is_drum=is_drum, name=instrument.value)

        note_pitches = predictions[track_idx]

        for step, pitch in enumerate(note_pitches):
            if pitch == OUTPUT_PAD:
                continue
            start = step * seconds_per_step
            end = start + seconds_per_step
            track.notes.append(pretty_midi.Note(velocity=80, pitch=int(pitch), start=start, end=end))

        midi.instruments.append(track)

    midi.write(output_path)
    return output_path
