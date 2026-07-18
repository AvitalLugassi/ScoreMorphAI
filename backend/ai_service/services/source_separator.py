from pathlib import Path
import subprocess
import sys

from config import Config


class SourceSeparator:
    """
    Audio source separation service.
    Uses Demucs to split audio into stems.
    """

    def separate(self, audio_path: str) -> dict:
        """
        Separate audio into stems.

        Args:
            audio_path: input audio file

        Returns:
            Dictionary containing stem paths
        """
        # וידוא שהקובץ קיים לפני שמתחילים עיבוד כבד
        if not Path(audio_path).exists():
            raise FileNotFoundError(
                f"Audio file does not exist: {audio_path}"
            )

        song_name  = Path(audio_path).stem
        # נתיב הפלט שבו Demucs שומר את ה-stems: separated/<model>/<song_name>/
        output_dir = Path(Config.SEPARATED_DIR) / Config.DEMUCS_MODEL / song_name
        stems      = ["vocals", "drums", "bass", "other"]

        # אם כל ה-stems כבר קיימים — דילוג על ההרצה מחדש (חוסך זמן עיבוד)
        if not all((output_dir / f"{s}.wav").exists() for s in stems):
            # הרצת Demucs כ-subprocess כדי לא לחסום את ה-event loop
            subprocess.run(
                [sys.executable, "-m", "demucs.separate",
                 "-n", Config.DEMUCS_MODEL, audio_path,
                 "-o", Config.SEPARATED_DIR],
                check=True  # זורק שגיאה אם Demucs נכשל
            )

        # מחזיר מילון: { "vocals": "path/vocals.wav", "drums": "path/drums.wav", ... }
        return {s: str(output_dir / f"{s}.wav") for s in stems}
