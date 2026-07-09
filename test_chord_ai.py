#!/usr/bin/env python3
"""
Test the new AI chord detection system
"""

from backend.services.chord_detector import detect_chords
import os

def test_chord_detection():
    print("🎵 בודק AI לזיהוי אקורדים...")
    
    # Test with existing audio files
    audio_files = [
        "data/uploads/Dara.mp3",
        "data/uploads/YONI.mp3"
    ]
    
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            print(f"\n📁 מנתח קובץ: {audio_file}")
            
            try:
                result = detect_chords(audio_file)
                
                print("📊 תוצאות:")
                print(f"   🎯 סה\"כ אקורדים: {result['total_chords']}")
                print(f"   📈 ביטחון ממוצע: {result['avg_confidence']:.2f}")
                print(f"   🎼 אקורדים מזוהים: {result['filtered_chords'][:10]}...")  # First 10
                
                # Show confidence breakdown
                high_confidence = sum(1 for score in result['confidence_scores'] if score > 0.8)
                medium_confidence = sum(1 for score in result['confidence_scores'] if 0.5 <= score <= 0.8)
                low_confidence = sum(1 for score in result['confidence_scores'] if score < 0.5)
                
                print(f"   ✅ ביטחון גבוה (>0.8): {high_confidence}")
                print(f"   ⚠️  ביטחון בינוני (0.5-0.8): {medium_confidence}")
                print(f"   ❌ ביטחון נמוך (<0.5): {low_confidence}")
                
            except Exception as e:
                print(f"❌ שגיאה: {e}")
        else:
            print(f"❌ קובץ לא נמצא: {audio_file}")

if __name__ == "__main__":
    test_chord_detection()