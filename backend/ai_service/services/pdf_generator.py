"""Converts arrangement MIDI into MusicXML and PDF using music21 + MuseScore."""

import os
import subprocess
from music21 import converter, key, tempo, metadata

MUSESCORE_PATH = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"


def generate_pdf(
    arrangement_midi_path: str,
    musical_key: str,
    bpm: float,
    output_dir: str,
    title: str = "Arrangement"
) -> dict:
    """
    Convert arrangement MIDI to MusicXML and PDF.

    Args:
        arrangement_midi_path: path to the generated arrangement MIDI
        musical_key: e.g. 'A minor'
        bpm: tempo
        output_dir: directory to save output files
        title: score title for the PDF

    Returns:
        dict with musicxml_path and pdf_path
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.join(output_dir, title.replace(" ", "_"))

    score = converter.parse(arrangement_midi_path)
    tonic, mode = musical_key.split()
    score.insert(0, key.Key(tonic, mode))
    score.insert(0, tempo.MetronomeMark(number=bpm))
    score.metadata = metadata.Metadata()
    score.metadata.title = title

    musicxml_path = base_name + ".musicxml"
    score.write("musicxml", fp=musicxml_path)

    pdf_path = base_name + ".pdf"
    subprocess.run(
        [MUSESCORE_PATH, "-T", "0", "--export-to", pdf_path, musicxml_path],
        check=True,
        capture_output=True
    )

    return {
        "musicxml_path": musicxml_path,
        "pdf_path": pdf_path
    }
