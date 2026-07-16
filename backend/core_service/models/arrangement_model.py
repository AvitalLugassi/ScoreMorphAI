from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Enum as SAEnum
from sqlalchemy.orm import relationship
from database import Base
import enum


class ArrangementStatus(str, enum.Enum):
    pending    = "pending"
    processing = "processing"
    completed  = "completed"
    failed     = "failed"


class Arrangement(Base):
    __tablename__ = "arrangements"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ── Request metadata (mirrors ArrangementRequest dataclass) ──
    title        = Column(String(255), nullable=True)
    original_song = Column(String(255), nullable=True)
    style        = Column(String(50), nullable=False)          # classical|pop|rock|jazz|blues
    difficulty   = Column(String(20), nullable=False)          # easy|medium|hard
    instruments  = Column(Text, nullable=False)                # JSON array stored as text
    voices_count = Column(Integer, nullable=False)             # 2|3|4

    # ── Processing state ──
    status       = Column(SAEnum(ArrangementStatus), default=ArrangementStatus.pending, nullable=False)

    # ── Output file paths (populated by ai_service on completion) ──
    midi_path    = Column(String(500), nullable=True)
    musicxml_path = Column(String(500), nullable=True)
    pdf_path     = Column(String(500), nullable=True)

    created_at   = Column(DateTime, server_default=func.now())
    updated_at   = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="arrangements")
