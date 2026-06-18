# 🎵 ScoreMorph-AI

**מערכת AI להמרת אודיו לעיבוד מוזיקלי - פרויקט אקדמי**

## 📋 סקירת הפרויקט

ScoreMorph-AI היא מערכת מבוססת בינה מלאכותית הממרה קבצי אודיו למידע מוזיקלי ויוצרת עיבודים חדשים המותאמים להעדפות המשתמש.

**חזון:** לא לשחזר את ההקלטה המקורית, אלא **לחלץ את המבנה המוזיקלי** (מלודיה, אקורדים, קצב) ו**ליצור עיבוד חדש** בהתאם להעדפות.

## test:

# Run this command to verify that the SourceSeparator service is working correctly:
# python -m tests.test_source_separator
#
# This test checks that Demucs successfully separates the input audio
# into stems (vocals, drums, bass, and other) and handles invalid paths properly.



## 🚀 זרימת משתמש

```
1. העלאת אודיו (MP3/WAV)
   ↓
2. ניתוח המערכת (חילוץ מלודיה, אקורדים, BPM)
   ↓
3. בחירת העדפות (סגנון, רמה, כלים)
   ↓
4. יצירת עיבוד חדש
   ↓
5. ייצוא (MIDI / MusicXML / PDF)
```

## 🎯 מטרות המערכת

✅ **חילוץ מידע מוזיקלי:**
- מלודיה מרכזית
- מהלך אקורדים
- קצב (BPM)
- סולם מוזיקלי

✅ **יצירת עיבודים:**
- התאמה לסגנון מוזיקלי
- התאמה לרמת קושי
- בחירת כלי נגינה

✅ **ייצוא:**
- MIDI (לתוכנות סימון)
- MusicXML (סטנדרט בינלאומי)
- PDF (תווים)

❌ **מה אנחנו לא עושים:**
- שחזור מושלם של ההקלטה
- הפרדת כל כלי נגינה
- תמלול מלא של השיר

## 🏗️ ארכיטקטורה

### Core Services (ליבת הפרויקט)

```
backend/services/
├── melody_extractor.py     - חילוץ מלודיה
├── chord_detector.py       - זיהוי אקורדים
├── tempo_detector.py       - זיהוי קצב וקליד
├── arrangement_engine.py   - יצירת עיבודים
└── score_generator.py      - יצירת תווים
```

### API Routes
```
backend/api/
├── upload_routes.py        - POST /api/upload/audio
├── score_routes.py         - POST /api/score/generate
└── export_routes.py        - GET /api/export/score/<id>
```

### Models & Utils
```
backend/models/             - Song, Score, Track
backend/utils/              - File Manager, Logger, Audio Utils
```

## 📁 מבנה הפרויקט

```
ScoreMorph-AI/
├── backend/                  ← קוד ליבי
│   ├── services/            ← Core processing
│   ├── api/                 ← REST endpoints
│   ├── models/              ← Data models
│   ├── utils/               ← Utilities
│   └── app.py, config.py
├── frontend/                ← UI (בעתיד)
├── data/                    ← אודיו, MIDI, תווים
│   ├── uploads/
│   ├── midi/
│   ├── scores/
│   └── temp/
├── docs/                    ← תיעוד
│   ├── vision.md           ← חזון הפרויקט
│   ├── architecture.md     ← ארכיטקטורה
│   ├── requirements.md     ← דרישות
│   └── project_plan.md     ← תכנית
├── tests/                   ← בדיקות יחידה
└── requirements.txt         ← תלויות
```

## 🛠️ דרישות

### Python
- Python 3.8+

### ספריות עיקריות
- **librosa** - עיבוד אודיו
- **music21** - יצירת תווים
- **flask** - web framework
- **demucs** - הפרדת מקורות (אופציונלי)

ראה `requirements.txt` לרשימה מלאה.

## 📦 התקנה

### 1. Clone/Download הפרויקט
```bash
cd ScoreMorph-AI
```

### 2. צור Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. התקן תלויות
```bash
pip install -r requirements.txt
```

## 🚀 הפעלה

### Backend
```bash
cd backend
python app.py
```

יחמם Flask server על `http://localhost:5000`

### הפעלת בדיקות
```bash
python -m pytest tests/
```

## 📖 תיעוד

- **[vision.md](docs/vision.md)** - חזון הפרויקט המפורט
- **[architecture.md](docs/architecture.md)** - ארכיטקטורת המערכת
- **[requirements.md](docs/requirements.md)** - דרישות פונקציונליות וטכניות
- **[project_plan.md](docs/project_plan.md)** - תכנית הפרויקט ו-timeline

## 🎓 שלב הפיתוח

אנחנו בונים **MVP (Minimum Viable Product)** עם התמקדות ב:
1. ✅ חילוץ מלודיה
2. ✅ זיהוי אקורדים
3. ✅ זיהוי קצב
4. ⏳ מנוע עיבוד
5. ⏳ יצירת תווים

**אחרון בעדיפות:** Frontend, Database, Authentication, Deployment

## 💡 דוגמה לשימוש

```python
from backend.services.melody_extractor import MelodyExtractor
from backend.services.chord_detector import ChordDetector
from backend.services.tempo_detector import TempoDetector
from backend.services.arrangement_engine import ArrangementEngine

# 1. חלץ מידע מוזיקלי
melody_extractor = MelodyExtractor()
melody = melody_extractor.extract_melody("song.mp3")

chord_detector = ChordDetector()
chords = chord_detector.detect_chords("song.mp3")

tempo_detector = TempoDetector()
tempo = tempo_detector.detect_tempo("song.mp3")

# 2. צור עיבוד
arrangement_engine = ArrangementEngine()
user_preferences = {
    'style': 'pop',
    'difficulty': 'intermediate',
    'instruments': ['piano', 'guitar'],
    'voices': 2
}
arrangement = arrangement_engine.create_arrangement(
    melody, chords, style='pop'
)

# 3. יצא תווים
# (coming soon)
```

## 🤝 תרומה

זה פרויקט אקדמי. ההנחיות לכתיבת קוד:
- קוד **נקי ומודולרי**
- כל קובץ אחראי **על משימה אחת**
- **Docstrings** עבור כל פונקציה
- **Testable** ו-**Expandable** code

## 📝 רישיון

[כדאי להוסיף רישיון כאן]

## 👤 יוצר

פרויקט אקדמי

---

**עזר נוסף:** ראה [vision.md](docs/vision.md) לתיעוד מפורט על החזון, הארכיטקטורה והדוגמאות.


