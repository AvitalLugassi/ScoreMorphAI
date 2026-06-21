"""
End-to-end test for parts 1 and 2.
Tests the full pipeline: audio → analysis → MusicXML
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.services.score_generator import generate
from backend.models.arrangement_request import ArrangementRequest

AUDIO_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'uploads', 'Dara.mp3')


def test_full_pipeline():
    print(f"\n{'='*50}")
    print("Starting end-to-end test")
    print(f"Audio file: {AUDIO_PATH}")
    print(f"{'='*50}\n")

    request = ArrangementRequest(
        style="classical",
        difficulty="medium",
        instruments=["piano", "violin"],
        voices_count=4
    )

    print("Step 1: Running score_generator.generate()...")
    result = generate(AUDIO_PATH, request)

    print("\nResults:")
    print(f"  musical_key:   {result['musical_key']}")
    print(f"  bpm:           {result['bpm']}")
    print(f"  chords:        {result['chords']}")
    print(f"  musicxml_path: {result['musicxml_path']}")
    print(f"  style:         {result['style']}")
    print(f"  difficulty:    {result['difficulty']}")
    print(f"  instruments:   {result['instruments']}")
    print(f"  voices_count:  {result['voices_count']}")

    print("\nValidations:")
    assert os.path.exists(result['musicxml_path']), "MusicXML file was not created!"
    print("  MusicXML file exists ✓")

    assert result['musical_key'], "musical_key is empty!"
    print(f"  musical_key is set ✓")

    assert result['bpm'] > 0, "BPM must be positive!"
    print(f"  bpm is positive ✓")

    assert isinstance(result['chords'], list), "chords must be a list!"
    print(f"  chords is a list ✓")

    print(f"\n{'='*50}")
    print("All checks passed ✓")
    print(f"{'='*50}\n")


if __name__ == '__main__':
    test_full_pipeline()
