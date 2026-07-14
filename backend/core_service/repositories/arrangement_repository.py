import json
from sqlalchemy.orm import Session
from arrangement_model import Arrangement, ArrangementStatus


class ArrangementRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, arrangement_id: int) -> Arrangement | None:
        return self.db.get(Arrangement, arrangement_id)

    def get_by_user(self, user_id: int) -> list[Arrangement]:
        rows = (
            self.db.query(Arrangement)
            .filter(Arrangement.user_id == user_id)
            .order_by(Arrangement.created_at.desc())
            .all()
        )
        return [self._deserialize(r) for r in rows]

    def create(self, user_id: int, title: str | None, style: str,
               difficulty: str, instruments: list[str], voices_count: int) -> Arrangement:
        row = Arrangement(
            user_id      = user_id,
            title        = title,
            style        = style,
            difficulty   = difficulty,
            instruments  = json.dumps(instruments),
            voices_count = voices_count,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._deserialize(row)

    def update_status(self, arrangement_id: int, status: ArrangementStatus,
                      midi_path: str = None, musicxml_path: str = None,
                      pdf_path: str = None) -> Arrangement | None:
        row = self.get_by_id(arrangement_id)
        if not row:
            return None
        row.status = status
        if midi_path:     row.midi_path     = midi_path
        if musicxml_path: row.musicxml_path = musicxml_path
        if pdf_path:      row.pdf_path      = pdf_path
        self.db.commit()
        self.db.refresh(row)
        return self._deserialize(row)

    def _deserialize(self, row: Arrangement) -> Arrangement:
        if isinstance(row.instruments, str):
            row.instruments = json.loads(row.instruments)
        return row
