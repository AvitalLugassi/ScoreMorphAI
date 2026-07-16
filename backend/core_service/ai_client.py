import requests
from config import settings


def process_arrangement(arrangement_id: int, file_path: str, style: str,
                        difficulty: str, instruments: list[str], voices_count: int) -> dict:
    with open(file_path, "rb") as f:
        files = {"file": (file_path.split("\\")[-1], f)}
        data = {
            "style": style,
            "difficulty": difficulty,
            "instruments": instruments,
            "voices_count": str(voices_count),
        }
        response = requests.post(
            f"{settings.AI_SERVICE_URL}/api/upload/audio",
            files=files,
            data=data,
            timeout=1200,
        )
    response.raise_for_status()
    return response.json()
