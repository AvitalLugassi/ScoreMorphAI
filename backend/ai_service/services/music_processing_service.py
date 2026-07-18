from services.source_separator import SourceSeparator
from services.melody_extractor import extract_melody
from services.accompaniment_extractor import extract_accompaniment
from services.tempo_detector import detect_tempo
from services.midi_builder import transcribe_to_scale
from services.model_runner import ModelRunner
from services.pdf_generator import generate_pdf
from models.song_analysis import SongAnalysis
from models.arrangement_request import ArrangementRequest
from config import Config
import os


def process_song(audio_path: str, request: ArrangementRequest) -> SongAnalysis:
    """
    Full pipeline:
    1. Separate stems (Demucs)
    2. Transcribe melody from vocals (Basic Pitch)
    3. Transcribe accompaniment from other + bass (Basic Pitch)
    4. Detect BPM from melody MIDI
    5. Build MusicXML with key signature
    6. Run arrangement model
    """

    # ── שלב 1: הפרדת מקורות ──────────────────────────────────────────────────
    # Demucs מפריד את השיר ל-4 stems: vocals, drums, bass, other
    stems = SourceSeparator().separate(audio_path)

    # ── שלב 2: חילוץ מנגינה ──────────────────────────────────────────────────
    # Basic Pitch ממיר את stem ה-vocals ל-MIDI ומזהה את הטונאליות
    melody = extract_melody(stems["vocals"])

    # ── שלב 3: חילוץ ליווי ───────────────────────────────────────────────────
    # המרת stems ה-other (הרמוניה) וה-bass ל-MIDI
    accompaniment = extract_accompaniment(stems["other"], stems["bass"])

    # ── שלב 4: זיהוי טמפו ────────────────────────────────────────────────────
    # חישוב BPM מקובץ ה-MIDI של המנגינה
    tempo_info = detect_tempo(melody["midi_path"])

    # ── שלב 5: בניית MusicXML ─────────────────────────────────────────────────
    # הוספת חתימת מפתח לפרטיטורה וייצוא כ-MusicXML
    musicxml_path = transcribe_to_scale(
        midi_path    = melody["midi_path"],
        musical_key  = melody["musical_key"]
    )

    # ── שלב 6: הרצת מודל ה-AI ────────────────────────────────────────────────
    # המודל מקבל מנגינה + הרמוניה + העדפות ומייצר arrangement מלא
    output_midi_path       = os.path.join(Config.MIDI_DIR, "arrangement.mid")
    arrangement_midi_path  = ModelRunner().run(
        melody_midi_path  = melody["midi_path"],
        harmony_midi_path = accompaniment["other_midi_path"],
        request           = request,
        bpm               = tempo_info["bpm"],
        output_midi_path  = output_midi_path
    )

    # ── שלב 7: יצירת PDF ─────────────────────────────────────────────────────
    # המרת ה-arrangement MIDI ל-MusicXML ו-PDF באמצעות MuseScore
    pdf_result = generate_pdf(
        arrangement_midi_path = arrangement_midi_path,
        musical_key           = melody["musical_key"],
        bpm                   = tempo_info["bpm"],
        output_dir            = Config.SCORE_DIR,
        title                 = "Arrangement"
    )

    # ── החזרת תוצאות מלאות ───────────────────────────────────────────────────
    return SongAnalysis(
        melody_midi_path          = melody["midi_path"],
        musicxml_path             = musicxml_path,
        other_midi_path           = accompaniment["other_midi_path"],
        bass_midi_path            = accompaniment["bass_midi_path"],
        arrangement_midi_path     = arrangement_midi_path,
        arrangement_musicxml_path = pdf_result["musicxml_path"],
        pdf_path                  = pdf_result["pdf_path"],
        musical_key               = melody["musical_key"],
        bpm                       = tempo_info["bpm"]
    )
