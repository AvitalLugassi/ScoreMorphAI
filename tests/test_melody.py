from backend.services.melody_extractor import extract_melody

result = extract_melody(
    "data/uploads/אלי.mp3"
)

print(result)