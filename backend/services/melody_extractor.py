from basic_pitch.inference import predict


def extract_melody(audio_path: str):
    """
    Extract melody from audio file and convert it to MIDI.

    Parameters:
        audio_path (str): path to mp3/wav file

    Returns:
        dict containing midi path and note count
    """

    model_output, midi_data, note_events = predict(audio_path)

    output_path = "data/midi/melody.mid"

    midi_data.write(output_path)

    return {
        "midi_path": output_path,
        "note_count": len(note_events)
    }