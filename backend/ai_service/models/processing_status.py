"""Status tracking for async arrangement processing"""

from dataclasses import dataclass
from enum import Enum


class StatusState(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


@dataclass
class ProcessingStatus:
    """Tracks the current state and progress of an arrangement job."""

    job_id: str
    state: StatusState
    progress: float  # 0.0 to 1.0
    message: str = ""
