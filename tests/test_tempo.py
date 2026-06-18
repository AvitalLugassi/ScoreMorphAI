import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.services.tempo_detector import detect_tempo

result = detect_tempo(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'uploads', 'אלי.mp3')
)

print(result)