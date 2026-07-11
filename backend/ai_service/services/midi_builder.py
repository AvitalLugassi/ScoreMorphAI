from music21 import converter, key


def transcribe_to_scale(midi_path: str, musical_key: str) -> str:
    """
    Parse MIDI and write MusicXML with the correct key signature.

    Args:
        midi_path: path to input MIDI file
        musical_key: key string like 'A minor' or 'C major'

    Returns:
        path to generated MusicXML file
    """
    score = converter.parse(midi_path)

    tonic, mode = musical_key.split(" ")
    score.insert(0, key.Key(tonic, mode))

    output_path = midi_path.replace(".mid", ".musicxml")
    score.write("musicxml", fp=output_path)

    return output_path
