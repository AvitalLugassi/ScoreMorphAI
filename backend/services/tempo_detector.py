"""Tempo and beat detection service"""

import os
from typing import Dict, Optional
from utils.logger import Logger


class TempoDetector:
    """Service for detecting tempo and beat information"""
    
    def __init__(self):
        """Initialize the tempo detector"""
        self.logger = Logger.get_logger(__name__)
        self.min_tempo = 40  # BPM
        self.max_tempo = 240  # BPM
        self.logger.info("TempoDetector initialized")
    
    def detect_tempo(self, audio_path: str) -> Dict:
        """
        Detect tempo from audio file
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            dict: Tempo information including BPM and confidence
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
        """
        if not os.path.exists(audio_path):
            self.logger.error(f"Audio file not found: {audio_path}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        self.logger.info(f"Detecting tempo from: {audio_path}")
        
        try:
            # Placeholder for actual tempo detection
            # Uses methods like:
            # - Onset detection
            # - Spectral flux
            # - Autocorrelation of onset times
            
            tempo_info = {
                'bpm': 120.0,
                'confidence': 0.0,
                'onset_times': [],
                'beat_frames': [],
                'tempo_curve': []
            }
            
            self.logger.info(f"Tempo detection completed: {tempo_info['bpm']} BPM")
            return tempo_info
            
        except Exception as e:
            self.logger.error(f"Error detecting tempo: {str(e)}")
            raise
    
    def detect_beat_tracking(self, audio_path: str) -> Dict:
        """
        Detect beat positions in audio
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            dict: Beat tracking information with frame positions
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        self.logger.info(f"Detecting beats in: {audio_path}")
        
        try:
            # Placeholder for beat tracking
            beat_info = {
                'beats': [],  # Times of detected beats
                'downbeats': [],  # Times of measure downbeats
                'meter': 4,  # Beats per measure
                'confidence': 0.0
            }
            
            self.logger.info(f"Beat tracking completed")
            return beat_info
            
        except Exception as e:
            self.logger.error(f"Error in beat tracking: {str(e)}")
            raise
    
    def detect_time_signature(self, audio_path: str) -> Dict:
        """
        Detect time signature from audio
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            dict: Time signature information
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        self.logger.info(f"Detecting time signature from: {audio_path}")
        
        try:
            # Analyze beat patterns to determine time signature
            time_sig_info = {
                'numerator': 4,
                'denominator': 4,
                'candidates': ['4/4', '3/4', '6/8'],
                'confidence': 0.0
            }
            
            self.logger.info(f"Time signature detection completed")
            return time_sig_info
            
        except Exception as e:
            self.logger.error(f"Error detecting time signature: {str(e)}")
            raise
    
    def tempo_from_onsets(self, onset_times: list) -> Dict:
        """
        Calculate tempo from onset detection times
        
        Args:
            onset_times (list): Times of detected onsets in seconds
            
        Returns:
            dict: Calculated tempo information
        """
        self.logger.info(f"Calculating tempo from {len(onset_times)} onsets")
        
        try:
            # Calculate inter-onset intervals
            intervals = [onset_times[i+1] - onset_times[i] 
                        for i in range(len(onset_times)-1)]
            
            if not intervals:
                return {'bpm': 120.0, 'error': 'Insufficient onsets'}
            
            avg_interval = sum(intervals) / len(intervals)
            bpm = 60.0 / avg_interval if avg_interval > 0 else 120.0
            
            # Clamp to reasonable range
            bpm = max(self.min_tempo, min(self.max_tempo, bpm))
            
            tempo = {
                'bpm': bpm,
                'avg_interval': avg_interval,
                'variance': self._calculate_variance(intervals),
                'stability': self._calculate_stability(intervals)
            }
            
            self.logger.info(f"Tempo from onsets: {bpm} BPM")
            return tempo
            
        except Exception as e:
            self.logger.error(f"Error calculating tempo: {str(e)}")
            raise
    
    def _calculate_variance(self, intervals: list) -> float:
        """Calculate variance of intervals"""
        if not intervals:
            return 0.0
        mean = sum(intervals) / len(intervals)
        return sum((x - mean) ** 2 for x in intervals) / len(intervals)
    
    def _calculate_stability(self, intervals: list) -> float:
        """Calculate tempo stability (0-1, higher is more stable)"""
        variance = self._calculate_variance(intervals)
        mean = sum(intervals) / len(intervals) if intervals else 0
        # Coefficient of variation
        if mean == 0:
            return 0.0
        cv = (variance ** 0.5) / mean
        return 1.0 / (1.0 + cv)  # Convert to 0-1 scale
    
    def align_to_beat(self, events: list, tempo: Dict) -> list:
        """
        Align events to nearest beat given tempo
        
        Args:
            events (list): Event times to align
            tempo (dict): Tempo information
            
        Returns:
            list: Aligned event times
        """
        self.logger.info(f"Aligning {len(events)} events to beat grid")
        
        beat_interval = 60.0 / tempo['bpm']
        aligned_events = [round(event / beat_interval) * beat_interval 
                         for event in events]
        
        return aligned_events
