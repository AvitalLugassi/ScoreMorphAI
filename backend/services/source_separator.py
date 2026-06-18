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
        command = [
            sys.executable,
            "-m",
            "demucs.separate",
            "-n",
            Config.DEMUCS_MODEL,
            audio_path,
            "-o",
            Config.SEPARATED_DIR
        ]

        subprocess.run(
            command,
            check=True
        )

        song_name = Path(audio_path).stem

        output_dir = (
                Path(Config.SEPARATED_DIR)
                / Config.DEMUCS_MODEL
                / song_name
        )

        return {
            "vocals": str(output_dir / "vocals.wav"),
            "drums": str(output_dir / "drums.wav"),
            "bass": str(output_dir / "bass.wav"),
            "other": str(output_dir / "other.wav")
        }