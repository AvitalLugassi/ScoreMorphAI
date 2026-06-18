from backend.services.chord_detector import detect_chords


audio_file = "data/uploads/אלי.mp3"


chords = detect_chords(audio_file)


print("Detected chords:")
print(chords)