# 🚀 מדריך פיתוח

## הגדרת סביבת פיתוח

### 1. Clone הפרויקט
```bash
git clone <repository-url>
cd ScoreMorph-AI
```

### 2. צור Virtual Environment
```bash
python -m venv venv
```

### 3. הפעל את ה-Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. התקן תלויות
```bash
pip install -r requirements.txt
```

### 5. הגדר משתנים סביבה
```bash
cp .env.example .env
# ערוך את .env לפי הצרכים שלך
```

---

## מבנה הפרויקט

### Backend Architecture
```
backend/
├── app.py              - Flask entry point
├── config.py           - Configuration management
│
├── api/                - REST API endpoints
│   ├── upload_routes.py
│   ├── score_routes.py
│   └── export_routes.py
│
├── services/           - ← CORE: עיבוד מוזיקלי
│   ├── melody_extractor.py      - חילוץ מלודיה
│   ├── chord_detector.py         - זיהוי אקורדים
│   ├── tempo_detector.py         - זיהוי קצב
│   ├── arrangement_engine.py     - יצירת עיבודים
│   └── score_generator.py        - יצירת תווים
│
├── models/             - Data models
│   ├── song.py
│   ├── score.py
│   └── track.py
│
└── utils/              - Utility functions
    ├── file_manager.py
    ├── audio_utils.py
    └── logger.py
```

---

## זרימת פיתוח (Development Workflow)

### 1. יצירת Branch חדש
```bash
git checkout -b feature/your-feature-name
```

### 2. כתיבת קוד
- עבוד ב-service אחד בכל פעם
- שמור קוד **מודולרי ונקי**
- הוסף **Docstrings** לכל פונקציה
- כתוב **בדיקות** תוך כדי

### 3. בדיקה מקומית
```bash
# הרץ את ה-backend
cd backend
python app.py

# בטרמינל אחר, הרץ בדיקות
pytest tests/ -v
```

### 4. Code Quality Checks
```bash
# Formatting
black backend/

# Linting
flake8 backend/

# Type checking (אם קיים)
pylint backend/
```

### 5. Commit ו-Push
```bash
git add .
git commit -m "feat: add melody extraction service"
git push origin feature/your-feature-name
```

---

## כתיבת Docstrings

### Python Docstring Format
```python
def extract_melody(audio_path: str) -> Dict:
    """
    Short description of what the function does.
    
    Longer description can go here if needed,
    explaining the algorithm or approach.
    
    Args:
        audio_path (str): Path to the audio file
        
    Returns:
        dict: Dictionary containing {
            'notes': list of notes,
            'contour': pitch contour,
            'range': pitch range
        }
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If audio format is not supported
        
    Example:
        >>> melody = extract_melody("song.mp3")
        >>> print(melody['notes'])
    """
    pass
```

---

## כתיבת בדיקות

### Test Structure
```python
import unittest
from unittest.mock import Mock, patch

class TestMelodyExtractor(unittest.TestCase):
    """Test suite for melody extraction"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = MelodyExtractor()
        self.test_audio = "tests/fixtures/test_audio.wav"
    
    def test_extract_melody_success(self):
        """Test successful melody extraction"""
        result = self.extractor.extract_melody(self.test_audio)
        self.assertIsNotNone(result)
        self.assertIn('notes', result)
    
    def test_extract_melody_file_not_found(self):
        """Test error handling for missing file"""
        with self.assertRaises(FileNotFoundError):
            self.extractor.extract_melody("nonexistent.mp3")
```

### הרצת בדיקות
```bash
# הרץ את כל הבדיקות
pytest tests/ -v

# הרץ בדיקות ספציפיות
pytest tests/test_melody_extractor.py -v

# הרץ עם coverage report
pytest tests/ --cov=backend --cov-report=html
```

---

## עצות לפיתוח

### 1. שמור על Simplicity
- התחל עם פתרון פשוט
- הוסף complexity בהדרגה
- עדיף placeholder שעובד מאשר ML מורכב שלא עובד

### 2. Code Organization
```python
# ❌ לא טוב - mixed concerns
class AudioProcessor:
    def extract_melody(self): pass
    def detect_chords(self): pass
    def generate_score(self): pass

# ✅ טוב - separate concerns
class MelodyExtractor:
    def extract_melody(self): pass

class ChordDetector:
    def detect_chords(self): pass

class ScoreGenerator:
    def generate_score(self): pass
```

### 3. Logging
```python
from utils.logger import Logger

class MyService:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
    
    def process(self):
        self.logger.info("Starting process")
        try:
            # ... code ...
            self.logger.info("Process completed")
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise
```

### 4. Type Hints
```python
from typing import List, Dict, Optional

def process_audio(
    audio_path: str,
    sample_rate: int = 44100
) -> Dict:
    """Process audio file"""
    pass

def filter_notes(
    notes: List[Dict],
    min_duration: float = 0.1
) -> List[Dict]:
    """Filter short notes"""
    pass
```

---

## Common Issues & Fixes

### Issue: Import errors
```bash
# Solution: Make sure __init__.py exists in packages
# and your Python path is correct

# Debug:
python -c "import backend.services.melody_extractor"
```

### Issue: File not found
```python
# ❌ Wrong - relative to current directory
audio_path = "data/uploads/song.mp3"

# ✅ Better - use absolute path
import os
audio_path = os.path.join(os.path.dirname(__file__), 
                          "../data/uploads/song.mp3")
```

### Issue: Memory issues with large audio
```python
# ✅ Solution - process in chunks
def process_large_audio(audio_path, chunk_size=30):
    """Process audio in 30-second chunks"""
    for chunk in load_audio_chunks(audio_path, chunk_size):
        yield process_chunk(chunk)
```

---

## Pre-commit Checklist

לפני commit:
- ✅ Code runs without errors
- ✅ All tests pass
- ✅ Code is formatted (black)
- ✅ No linting errors (flake8)
- ✅ Docstrings added
- ✅ No hardcoded paths (use os.path.join)
- ✅ Logging added for debugging
- ✅ Type hints included

---

## Useful Commands

```bash
# Start Flask dev server
cd backend && python app.py

# Run tests with coverage
pytest tests/ --cov=backend

# Format code
black backend/

# Check for issues
flake8 backend/

# Generate documentation (if using sphinx)
cd docs && make html

# Check imports
python -m py_compile backend/**/*.py
```

---

## Resources

- **librosa docs:** https://librosa.org/
- **music21 docs:** https://web.mit.edu/music21/
- **Flask docs:** https://flask.palletsprojects.com/
- **Python typing:** https://docs.python.org/3/library/typing.html

---

**המטרה:** יצירת קוד מוזי מודולרי וקל לתחזוקה, המאפשר הרחבה עתידית בלי שינויים גדולים בהיסוד.
