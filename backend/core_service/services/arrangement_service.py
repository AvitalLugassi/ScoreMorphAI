from sqlalchemy.orm import Session
from arrangement_model import Arrangement, ArrangementStatus
from arrangement_schema import ArrangementCreate
from user_model import User
from repositories import ArrangementRepository


class ArrangementService:

    def __init__(self, db: Session):
        self.repo = ArrangementRepository(db)

    def create(self, data: ArrangementCreate, user: User) -> Arrangement:
        return self.repo.create(
            user_id      = user.id,
            title        = data.title,
            style        = data.style.value,
            difficulty   = data.difficulty.value,
            instruments  = [i.value for i in data.instruments],
            voices_count = data.voices_count,
        )

    def get_user_arrangements(self, user: User) -> list[Arrangement]:
        return self.repo.get_by_user(user.id)

    def _send_to_ai(self, arrangement_id: int, data: ArrangementCreate, audio_bytes: bytes, filename: str):
        try:
            files   = {"file": (filename, audio_bytes, "audio/mpeg")}
            payload = {
                "style":        data.style.value,
                "difficulty":   data.difficulty.value,
                "voices_count": str(data.voices_count),
                "arrangement_id": str(arrangement_id),
                "callback_url": f"{settings.CORE_SERVICE_URL}/arrangements/{arrangement_id}/complete",
            }
            for inst in data.instruments:
                payload.setdefault("instruments", [])
            form = {k: v for k, v in payload.items() if k != "instruments"}
            resp = requests.post(
                f"{settings.AI_SERVICE_URL}/api/upload/audio",
                files=files,
                data={**form, **{"instruments": [i.value for i in data.instruments]}},
                timeout=300,
            )
            if resp.status_code != 200:
                self._mark_failed(arrangement_id)
        except Exception:
            self._mark_failed(arrangement_id)

    def _mark_failed(self, arrangement_id: int):
        from database import SessionLocal
        db = SessionLocal()
        try:
            ArrangementRepository(db).update_status(arrangement_id, ArrangementStatus.failed)
        finally:
            db.close()
