from music21 import converter, stream


def generate_score(midi_path, output_path):
    """
    Convert MIDI file into MusicXML score.

    Args:
        midi_path: path to MIDI file
        output_path: where to save MusicXML

    Returns:
        generated file path
    """

    score = converter.parse(midi_path)

    score.write(
        "musicxml",
        fp=output_path
    )

    return output_path



def save_midi(score, output_path):
    """
    Save music21 score as MIDI.
    """

    score.write(
        "midi",
        fp=output_path
    )

    return output_path