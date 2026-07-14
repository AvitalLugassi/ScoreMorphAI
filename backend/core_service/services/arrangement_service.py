from sqlalchemy.orm import Session
from arrangement_model import Arrangement
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
