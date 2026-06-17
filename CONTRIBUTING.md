# 🤝 תרומה לפרויקט

תודה שאתה מעוניין לתרום לפרויקט ScoreMorph-AI! 🎵

## Code of Conduct

- כבד את כל אנשי הצוות
- כתוב קוד נקי וקל להבנה
- תעזור לאחרים להבין את הקוד שלך

## איך תורמים

### 1. Fork ו-Clone
```bash
# Fork בגיטהאב
git clone https://github.com/YOUR_USERNAME/ScoreMorph-AI.git
cd ScoreMorph-AI
```

### 2. צור Feature Branch
```bash
git checkout -b feature/amazing-feature
```

### 3. עשה את השינויים
- בחר ONE ספציפי שירות (service) לעבודה
- כתוב קוד מודולרי
- הוסף tests
- עדכן documentation

### 4. Commit changes
```bash
# Good commit message
git commit -m "feat: add vibrato detection in melody extractor"

# Avoid: "fixed stuff", "update", "changes"
```

### 5. Push ו-Create Pull Request
```bash
git push origin feature/amazing-feature
# ואז צור PR בגיטהאב
```

---

## סטנדרטים לקוד

### ✅ DO

```python
# ✅ Type hints
def extract_melody(audio_path: str) -> Dict:
    """Extract melody from audio."""
    pass

# ✅ Error handling
try:
    result = process_audio(audio_path)
except FileNotFoundError:
    logger.error(f"File not found: {audio_path}")
    raise

# ✅ Logging
self.logger.info("Processing started")

# ✅ Docstrings
def detect_tempo(audio_path: str) -> Dict:
    """
    Detect tempo from audio.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        dict: Contains 'bpm' and 'confidence'
    """
    pass

# ✅ Constants in CAPS
MIN_TEMPO = 40
MAX_TEMPO = 240
```

### ❌ DON'T

```python
# ❌ No type hints
def extract_melody(audio_path):
    pass

# ❌ Bare except
try:
    result = process()
except:
    pass

# ❌ print() for debugging (use logger!)
print("DEBUG: tempo =", tempo)

# ❌ Hardcoded paths
audio_file = "C:\\Users\\john\\music\\song.mp3"

# ❌ Magic numbers
if len(notes) > 50:  # What does 50 mean?
    pass
```

---

## Areas We Need Help With

### 🔴 High Priority

1. **melody_extractor.py**
   - Implement actual melody extraction (placeholder now)
   - Add vibrato detection
   - Add pitch detection algorithm

2. **chord_detector.py**
   - Implement chord recognition (placeholder now)
   - Support different chord types
   - Add chord voicing suggestions

3. **tempo_detector.py**
   - Implement BPM detection (placeholder now)
   - Add beat tracking
   - Detect time signature

### 🟡 Medium Priority

1. **arrangement_engine.py**
   - Implement smart arrangement creation
   - Add more arrangement styles
   - Support different difficulty levels

2. **score_generator.py**
   - Export to MusicXML
   - Export to PDF
   - Add proper formatting

### 🟢 Lower Priority

- Frontend implementation
- Database integration
- Authentication system
- API optimization

---

## Testing Requirements

כל PR חייב להכיל:

### Unit Tests
```python
class TestMelodyExtractor(unittest.TestCase):
    def test_happy_path(self):
        """Test normal successful operation"""
        pass
    
    def test_error_handling(self):
        """Test error cases"""
        pass
    
    def test_edge_cases(self):
        """Test boundary conditions"""
        pass
```

### Minimum Coverage
- ✅ Core functions: 80%+ coverage
- ✅ Helper functions: 60%+ coverage

### Run Tests Before PR
```bash
pytest tests/ -v --cov=backend
```

---

## Documentation Requirements

### Code Documentation
- ✅ Docstrings for all functions
- ✅ Comments for complex logic
- ✅ Type hints on all parameters

### Changes Documentation
- ✅ Update DEVELOPMENT.md if needed
- ✅ Update README.md if adding features
- ✅ Update docs/vision.md if scope changed

---

## Pull Request Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation

## How to Test
Steps to verify the changes:
1. Run `pytest tests/test_xxx.py`
2. Check that X works correctly

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review done
- [ ] Comments added where needed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass

## Related Issues
Closes #123
```

---

## Review Process

### What Reviewers Look For
1. **Code Quality** - Is it clean and maintainable?
2. **Tests** - Are there sufficient tests?
3. **Documentation** - Is it well documented?
4. **Scope** - Does it stick to one feature?
5. **Performance** - Are there any performance issues?

### Timeline
- First review: 2-3 days
- Approval to merge: 1-2 days

---

## Git Workflow

### Good Commit Messages
```
feat: add vibrato detection
fix: handle edge case in tempo detection
docs: update melody extractor documentation
test: add tests for chord detection
refactor: simplify arrangement engine logic
```

### Keep Your Branch Updated
```bash
git fetch upstream
git rebase upstream/main
```

---

## Questions?

אם יש לך שאלה:
1. Check [DEVELOPMENT.md](DEVELOPMENT.md)
2. Check [vision.md](docs/vision.md)
3. Open an Issue בגיטהאב

---

## Appreciation

תודה רבה על התרומה! 🙏

כל תרומה, גדולה או קטנה, עוזרת להפוך את הפרויקט לטוב יותר.

**Happy coding! 🎵**
