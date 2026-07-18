import os
import librosa
from basic_pitch.inference import predict

# שמות 12 הנוטות בסולם הכרומטי — משמשים להמרת אינדקס לשם תו
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# נתיב תיקיית ה-MIDI — נבנה יחסית למיקום הקובץ הנוכחי
_MIDI_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "midi"
)


def detect_key(audio_path: str) -> str:
    """
    Detect musical key from audio using chroma energy.
    Returns key string like 'C major' or 'A minor'.
    """
    # טעינת האודיו עם librosa — מחזיר אות גלים (y) ו-sample rate (sr)
    y, sr = librosa.load(audio_path)

    # חישוב Chroma CQT — מייצג את עוצמת כל אחד מ-12 הנוטות לאורך הזמן
    chroma      = librosa.feature.chroma_cqt(y=y, sr=sr)
    # ממוצע לאורך ציר הזמן — מקבלים וקטור של 12 ערכים
    chroma_mean = chroma.mean(axis=1)

    # פרופילי Krumhansl-Schmuckler — ערכים אמפיריים שמייצגים
    # את ההסתברות של כל נוטה להופיע בסולם מז'ורי/מינורי
    major_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
    minor_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

    best_key, best_mode, best_score = 0, "major", -float("inf")

    # בדיקת כל 12 הטרנספוזיציות האפשריות (C, C#, D, ...)
    for i in range(12):
        # סיבוב הכרומה כדי להתאים לכל טוניקה אפשרית
        rotated = [chroma_mean[(i + j) % 12] for j in range(12)]

        # ציון התאמה — מכפלה סקלרית בין הכרומה לפרופיל
        major_score = sum(a * b for a, b in zip(rotated, major_profile))
        minor_score = sum(a * b for a, b in zip(rotated, minor_profile))

        if major_score > best_score:
            best_score, best_key, best_mode = major_score, i, "major"
        if minor_score > best_score:
            best_score, best_key, best_mode = minor_score, i, "minor"

    return f"{NOTE_NAMES[best_key]} {best_mode}"


def extract_melody(audio_path: str) -> dict:
    """
    Extract melody from audio file and convert it to MIDI.
    Also detects the musical key.

    Parameters:
        audio_path (str): path to mp3/wav file

    Returns:
        dict containing midi_path, note_count, and musical_key
    """
    # Basic Pitch — מודל AI של Spotify שממיר אודיו ל-MIDI
    # מחזיר: model_output (raw), midi_data (PrettyMIDI), note_events (רשימת תווים)
    model_output, midi_data, note_events = predict(audio_path)

    # יצירת תיקיית MIDI אם לא קיימת
    os.makedirs(_MIDI_DIR, exist_ok=True)
    output_path = os.path.join(_MIDI_DIR, "melody.mid")

    # שמירת קובץ ה-MIDI
    midi_data.write(output_path)

    # זיהוי הטונאליות של השיר
    musical_key = detect_key(audio_path)

    return {
        "midi_path":    output_path,
        "note_count":   len(note_events),  # מספר התווים שזוהו
        "musical_key":  musical_key        # למשל: "A minor"
    }
