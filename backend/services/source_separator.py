from pathlib import Path
import subprocess
import sys

from backend.config import Config


class SourceSeparator:
    """
    Audio source separation service.
    Uses Demucs to split audio into stems.
    """

    def separate(
            self,
            audio_path: str
    ) -> dict:
        """
        Separate audio into stems.

        Args:
            audio_path: input audio file

        Returns:
            Dictionary containing stem paths
        """
        if not Path(audio_path).exists():
            raise FileNotFoundError(
                f"Audio file does not exist: {audio_path}"
            )

        song_name = Path(audio_path).stem
        output_dir = Path(Config.SEPARATED_DIR) / Config.DEMUCS_MODEL / song_name
        stems = ["vocals", "drums", "bass", "other"]

        if not all((output_dir / f"{s}.wav").exists() for s in stems):
            subprocess.run(
                [sys.executable, "-m", "demucs.separate", "-n", Config.DEMUCS_MODEL, audio_path, "-o", Config.SEPARATED_DIR],
                check=True
            )

        return {s: str(output_dir / f"{s}.wav") for s in stems}