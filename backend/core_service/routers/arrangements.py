from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from user_model import User
from arrangement_schema import ArrangementCreate, ArrangementResponse, ArrangementComplete, StyleEnum, DifficultyEnum, InstrumentEnum
from services import get_current_user
from controllers import ArrangementController
from services import ArrangementService

router = APIRouter(prefix="/arrangements", tags=["arrangements"])


@router.get("", response_model=list[ArrangementResponse])
def list_arrangements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ArrangementController(db).list_for_user(current_user)


@router.post("", response_model=ArrangementResponse, status_code=201)
async def create(
    file:         UploadFile = File(...),
    style:        StyleEnum  = Form(...),
    difficulty:   DifficultyEnum = Form(...),
    instruments:  list[InstrumentEnum] = Form(...),
    voices_count: int        = Form(...),
    title:        Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    body = ArrangementCreate(
        title=title,
        style=style,
        difficulty=difficulty,
        instruments=instruments,
        voices_count=voices_count,
    )
    audio_bytes = await file.read()
    service = ArrangementService(db)
    arrangement = service.create_and_process(body, current_user, audio_bytes, file.filename)
    return ArrangementResponse.model_validate(arrangement)


@router.put("/{arrangement_id}/complete", response_model=ArrangementResponse)
def complete(
    arrangement_id: int,
    body: ArrangementComplete,
    db: Session = Depends(get_db),
):
    service = ArrangementService(db)
    arrangement = service.complete(
        arrangement_id,
        midi_path=body.midi_path,
        musicxml_path=body.musicxml_path,
        pdf_path=body.pdf_path,
    )
    if not arrangement:
        raise HTTPException(status_code=404, detail="Arrangement not found")
    return ArrangementResponse.model_validate(arrangement)
