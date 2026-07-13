import json
from sqlalchemy.orm import Session
from models import Arrangement, User
from arrangement_schema import ArrangementCreate


def create_arrangement(db: Session, data: ArrangementCreate, user: User) -> Arrangement:
    row = Arrangement(
        user_id      = user.id,
        title        = data.title,
        style        = data.style.value,
        difficulty   = data.difficulty.value,
        instruments  = json.dumps([i.value for i in data.instruments]),
        voices_count = data.voices_count,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _deserialize(row)


def get_user_arrangements(db: Session, user: User) -> list[Arrangement]:
    rows = db.query(Arrangement).filter(Arrangement.user_id == user.id).order_by(Arrangement.created_at.desc()).all()
    return [_deserialize(r) for r in rows]


def _deserialize(row: Arrangement) -> Arrangement:
    if isinstance(row.instruments, str):
        row.instruments = json.loads(row.instruments)
    return row
