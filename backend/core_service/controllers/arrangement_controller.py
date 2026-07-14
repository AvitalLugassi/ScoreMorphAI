from sqlalchemy.orm import Session
from arrangement_schema import ArrangementCreate, ArrangementResponse
from services import ArrangementService
from user_model import User


class ArrangementController:

    def __init__(self, db: Session):
        self.service = ArrangementService(db)

    def create(self, body: ArrangementCreate, user: User) -> ArrangementResponse:
        arrangement = self.service.create(body, user)
        return ArrangementResponse.model_validate(arrangement)

    def list_for_user(self, user: User) -> list[ArrangementResponse]:
        arrangements = self.service.get_user_arrangements(user)
        return [ArrangementResponse.model_validate(a) for a in arrangements]
