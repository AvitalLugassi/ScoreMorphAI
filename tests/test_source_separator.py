import unittest
from pathlib import Path

from backend.services.source_separator import SourceSeparator

class TestSourceSeparator(unittest.TestCase):

    def setUp(self):

        self.separator = SourceSeparator()

        self.audio_path = (
            "data/uploads/YONI.mp3"
        )

    def test_separate_audio_sources(self):

        result = self.separator.separate(
            self.audio_path
        )

        self.assertIn(
            "vocals",
            result
        )

        self.assertIn(
            "drums",
            result
        )

        self.assertIn(
            "bass",
            result
        )

        self.assertIn(
            "other",
            result
        )

        self.assertTrue(
            Path(result["vocals"]).exists()
        )

        self.assertTrue(
            Path(result["drums"]).exists()
        )

        self.assertTrue(
            Path(result["bass"]).exists()
        )

        self.assertTrue(
            Path(result["other"]).exists()
        )

    def test_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            self.separator.separate(
                "not_existing.mp3"
            )

if __name__ == "__main__":
    unittest.main()