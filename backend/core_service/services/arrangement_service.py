import threading
from sqlalchemy.orm import Session
from arrangement_model import Arrangement, ArrangementStatus
from arrangement_schema import ArrangementCreate
from user_model import User
from repositories import ArrangementRepository
import ai_client


class ArrangementService:

    def __init__(self, db: Session):
        self.repo = ArrangementRepository(db)

    def create(self, data: ArrangementCreate, user: User, file_path: str) -> Arrangement:
        arrangement = self.repo.create(
            user_id       = user.id,
            title         = data.title,
            original_song = data.original_song,
            style         = data.style.value,
            difficulty    = data.difficulty.value,
            instruments   = [i.value for i in data.instruments],
            voices_count  = data.voices_count,
        )
        thread = threading.Thread(
            target=self._run_ai,
            args=(arrangement.id, file_path, data),
            daemon=True,
        )
        thread.start()
        return arrangement

    def _run_ai(self, arrangement_id: int, file_path: str, data: ArrangementCreate):
        from database import SessionLocal
        db = SessionLocal()
        repo = ArrangementRepository(db)
        try:
            repo.update_status(arrangement_id, ArrangementStatus.processing)
            result = ai_client.process_arrangement(
                arrangement_id=arrangement_id,
                file_path=file_path,
                style=data.style.value,
                difficulty=data.difficulty.value,
                instruments=[i.value for i in data.instruments],
                voices_count=data.voices_count,
            )
            repo.update_status(
                arrangement_id,
                ArrangementStatus.completed,
                midi_path=result.get("arrangement_midi_path"),
                musicxml_path=result.get("arrangement_musicxml_path"),
                pdf_path=result.get("pdf_path"),
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            repo.update_status(arrangement_id, ArrangementStatus.failed)
        finally:
            db.close()

    def get_user_arrangements(self, user: User) -> list[Arrangement]:
        return self.repo.get_by_user(user.id)
