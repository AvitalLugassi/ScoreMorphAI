"""Converts arrangement MIDI into MusicXML and PDF using music21 + MuseScore."""

import os
import subprocess
from music21 import converter, key, tempo, metadata

# נתיב MuseScore — משמש להמרת MusicXML ל-PDF
# אם לא מותקן, הפונקציה תחזיר pdf_path=None
MUSESCORE_PATH = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"


def generate_pdf(
    arrangement_midi_path: str,
    musical_key:           str,
    bpm:                   float,
    output_dir:            str,
    title:                 str = "Arrangement"
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
    # יצירת תיקיית הפלט אם לא קיימת
    os.makedirs(output_dir, exist_ok=True)

    # שם בסיס לקבצי הפלט — רווחים מוחלפים ב-underscore
    base_name = os.path.join(output_dir, title.replace(" ", "_"))

    # פרסור ה-MIDI ל-Score של music21
    score = converter.parse(arrangement_midi_path)

    # הוספת חתימת מפתח בתחילת הפרטיטורה
    tonic, mode = musical_key.split()
    score.insert(0, key.Key(tonic, mode))

    # הוספת סימון טמפו (BPM)
    score.insert(0, tempo.MetronomeMark(number=bpm))

    # הוספת מטאדאטה — כותרת הפרטיטורה
    score.metadata       = metadata.Metadata()
    score.metadata.title = title

    # ייצוא ל-MusicXML — פורמט פתוח שניתן לפתוח בכל תוכנת תווים
    musicxml_path = base_name + ".musicxml"
    score.write("musicxml", fp=musicxml_path)

    # ייצוא ל-PDF באמצעות MuseScore (אם מותקן)
    pdf_path = base_name + ".pdf"
    if os.path.exists(MUSESCORE_PATH):
        subprocess.run(
            [MUSESCORE_PATH, "-T", "0", "--export-to", pdf_path, musicxml_path],
            check=True,
            capture_output=True  # מסתיר את הפלט של MuseScore מהטרמינל
        )
    else:
        # MuseScore לא מותקן — מחזירים None, הלקוח יוכל להוריד MusicXML במקום
        pdf_path = None

    return {
        "musicxml_path": musicxml_path,
        "pdf_path":      pdf_path
    }
