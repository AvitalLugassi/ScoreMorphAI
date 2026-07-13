from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import ArrangementCreate, ArrangementResponse
from services import get_current_user, create_arrangement, get_user_arrangements

router = APIRouter(prefix="/arrangements", tags=["arrangements"])


@router.get("", response_model=list[ArrangementResponse])
def list_arrangements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all arrangements belonging to the authenticated user."""
    return get_user_arrangements(db, current_user)


@router.post("", response_model=ArrangementResponse, status_code=201)
def create(
    body: ArrangementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create an arrangement record (status=pending).
    The ai_service picks this up and updates status + output paths when done.
    """
    return create_arrangement(db, body, current_user)
