from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from user_model import User
from arrangement_schema import ArrangementCreate, ArrangementResponse
from schemas.arrangement_schema import StyleEnum, DifficultyEnum, InstrumentEnum
from services import get_current_user
from controllers import ArrangementController
from repositories import ArrangementRepository
from config import settings
import shutil, os, uuid, requests

router = APIRouter(prefix="/arrangements", tags=["arrangements"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "app_data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

FORMAT_TO_ROUTE = {
    "pdf":      "/api/export/pdf",
    "midi":     "/api/export/midi",
    "musicxml": "/api/export/musicxml",
}
FORMAT_TO_PATH_FIELD = {
    "pdf":      "pdf_path",
    "midi":     "midi_path",
    "musicxml": "musicxml_path",
}


@router.get("", response_model=list[ArrangementResponse])
def list_arrangements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ArrangementController(db).list_for_user(current_user)


@router.post("", response_model=ArrangementResponse, status_code=201)
def create(
    file: UploadFile = File(...),
    style: StyleEnum = Form(...),
    difficulty: DifficultyEnum = Form(...),
    instruments: list[InstrumentEnum] = Form(...),
    voices_count: int = Form(...),
    original_song: str = Form(None),
    title: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ext = os.path.splitext(file.filename)[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    body = ArrangementCreate(
        title=title,
        original_song=original_song,
        style=style,
        difficulty=difficulty,
        instruments=instruments,
        voices_count=voices_count,
    )
    return ArrangementController(db).create(body, current_user, file_path)


@router.get("/{arrangement_id}/export")
def export(
    arrangement_id: int,
    format: str = "pdf",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if format not in FORMAT_TO_ROUTE:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

    arrangement = ArrangementRepository(db).get_by_id(arrangement_id)
    if not arrangement or arrangement.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Arrangement not found")

    file_path = getattr(arrangement, FORMAT_TO_PATH_FIELD[format])
    if not file_path:
        raise HTTPException(status_code=404, detail="File not ready yet")

    response = requests.get(
        f"{settings.AI_SERVICE_URL}{FORMAT_TO_ROUTE[format]}",
        params={"path": file_path},
        stream=True,
        timeout=30,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="File not found on AI service")

    return StreamingResponse(
        response.iter_content(chunk_size=8192),
        media_type=response.headers.get("content-type", "application/octet-stream"),
        headers={"Content-Disposition": f'attachment; filename="arrangement.{format}"'},
    )
