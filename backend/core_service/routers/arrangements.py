from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from user_model import User
from arrangement_schema import ArrangementCreate, ArrangementResponse
from services import get_current_user
from controllers import ArrangementController

router = APIRouter(prefix="/arrangements", tags=["arrangements"])


@router.get("", response_model=list[ArrangementResponse])
def list_arrangements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ArrangementController(db).list_for_user(current_user)


@router.post("", response_model=ArrangementResponse, status_code=201)
def create(
    body: ArrangementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ArrangementController(db).create(body, current_user)
