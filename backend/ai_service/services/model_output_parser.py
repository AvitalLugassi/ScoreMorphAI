"""Converts model output tensor into a MIDI file."""

import numpy as np
import pretty_midi
from models.arrangement_request import ArrangementRequest, INSTRUMENT_MIDI_MAP, OUTPUT_PAD


def parse_model_output(
    predictions: np.ndarray,
    request:     ArrangementRequest,
    bpm:         float,
    output_path: str
) -> str:
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
    # חישוב משך כל step בשניות — רזולוציה של 16th note (שישה-עשרה)
    # 60/bpm = משך רבע תו, חלקי 4 = משך שישה-עשרה
    seconds_per_step = 60.0 / bpm / 4

    # יצירת אובייקט MIDI חדש עם הטמפו הנכון
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)

    # עיבוד כל track (כלי) בנפרד
    for track_idx, instrument in enumerate(request.instruments):
        program = INSTRUMENT_MIDI_MAP[instrument]
        is_drum = instrument.value == "drums"  # תופים מקבלים channel 10 ב-MIDI

        track = pretty_midi.Instrument(
            program=program,
            is_drum=is_drum,
            name=instrument.value
        )

        # predictions[track_idx] = רצף של 256 ערכי pitch לכלי הנוכחי
        note_pitches = predictions[track_idx]

        for step, pitch in enumerate(note_pitches):
            # OUTPUT_PAD = silence — דילוג על steps ריקים
            if pitch == OUTPUT_PAD:
                continue

            # חישוב זמני התחלה וסיום של התו
            start = step * seconds_per_step
            end   = start + seconds_per_step

            track.notes.append(
                pretty_midi.Note(
                    velocity=80,        # עוצמה קבועה (0-127)
                    pitch=int(pitch),   # גובה התו
                    start=start,
                    end=end
                )
            )

        midi.instruments.append(track)

    midi.write(output_path)
    return output_path
