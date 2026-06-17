"""
Melody Extraction Service

Module responsible for extracting melodic information from audio files.
Supports multiple extraction algorithms and provides flexible, extensible architecture
for melody analysis, note detection, vibrato detection, and pitch contour analysis.

Classes:
    MelodyExtractor: Main service for melody extraction
    BaseMelodyAlgorithm: Abstract base for melody extraction algorithms
    
Author: ScoreMorph-AI Team
Version: 1.0.0
"""

import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

from utils.logger import Logger


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Note:
    """Represents a single musical note"""
    pitch: float                    # Hz or MIDI number
    pitch_name: str                 # e.g., "C4", "D#5"
    start_time: float              # seconds
    duration: float                # seconds
    confidence: float              # 0.0-1.0, higher is more confident
    velocity: int = 80             # MIDI velocity (0-127)
    
    def to_dict(self) -> Dict:
        """Convert note to dictionary representation"""
        return {
            'pitch': self.pitch,
            'pitch_name': self.pitch_name,
            'start_time': self.start_time,
            'duration': self.duration,
            'confidence': self.confidence,
            'velocity': self.velocity
        }


@dataclass
class MelodyContour:
    """Represents the contour (shape) of a melody"""
    pitches: List[float]           # Pitch values over time
    times: List[float]             # Time values
    confidence: List[float]        # Confidence for each pitch
    
    @property
    def duration(self) -> float:
        """Total duration of melody"""
        return self.times[-1] if self.times else 0.0
    
    @property
    def pitch_range(self) -> Tuple[float, float]:
        """Min and max pitches"""
        if not self.pitches:
            return (0.0, 0.0)
        return (min(self.pitches), max(self.pitches))
    
    def to_dict(self) -> Dict:
        """Convert contour to dictionary"""
        return {
            'pitches': self.pitches,
            'times': self.times,
            'confidence': self.confidence,
            'duration': self.duration,
            'pitch_range': self.pitch_range
        }


@dataclass
class Vibrato:
    """Vibrato characteristics"""
    present: bool                   # Whether vibrato is detected
    rate: float = 0.0              # Hz (cycles per second)
    extent: float = 0.0            # cents (pitch variation)
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    confidence: float = 0.0        # Detection confidence
    
    def to_dict(self) -> Dict:
        """Convert vibrato to dictionary"""
        return {
            'present': self.present,
            'rate': self.rate,
            'extent': self.extent,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'confidence': self.confidence
        }


@dataclass
class MelodyAnalysis:
    """Complete melody analysis result"""
    contour: MelodyContour
    notes: List[Note]
    vibrato: Vibrato
    key: Optional[str] = None
    range_min: Optional[str] = None
    range_max: Optional[str] = None
    estimated_vocal_range: Optional[str] = None
    intervals: List[int] = None
    
    def to_dict(self) -> Dict:
        """Convert analysis to dictionary"""
        return {
            'contour': self.contour.to_dict(),
            'notes': [n.to_dict() for n in self.notes],
            'vibrato': self.vibrato.to_dict(),
            'key': self.key,
            'range_min': self.range_min,
            'range_max': self.range_max,
            'estimated_vocal_range': self.estimated_vocal_range,
            'intervals': self.intervals
        }


# ============================================================================
# Algorithm Abstraction
# ============================================================================

class ExtractionMethod(Enum):
    """Available melody extraction methods"""
    LIBROSA = "librosa"           # Using librosa + pyin
    BASICPITCH = "basicpitch"     # Using Spotify's BasicPitch
    MELODIA = "melodia"           # Using Melodia algorithm
    HYBRID = "hybrid"             # Combination of multiple methods


class BaseMelodyAlgorithm(ABC):
    """
    Abstract base class for melody extraction algorithms.
    
    Allows for multiple implementations while maintaining consistent interface.
    Future algorithms can be added without modifying MelodyExtractor.
    """
    
    def __init__(self, logger: Logger):
        """
        Initialize the algorithm
        
        Args:
            logger: Logger instance for debugging
        """
        self.logger = logger
    
    @abstractmethod
    def extract(self, audio_path: str) -> MelodyAnalysis:
        """
        Extract melody from audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            MelodyAnalysis object with contour, notes, vibrato
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
            ValueError: If audio format not supported
        """
        pass


class LibrosaMelodyExtractor(BaseMelodyAlgorithm):
    """Melody extraction using librosa + pyin algorithm"""
    
    def __init__(self, logger: Logger, sample_rate: int = 22050):
        """
        Initialize librosa-based extractor
        
        Args:
            logger: Logger instance
            sample_rate: Sample rate for audio processing
        """
        super().__init__(logger)
        self.sample_rate = sample_rate
    
    def extract(self, audio_path: str) -> MelodyAnalysis:
        """
        Extract melody using librosa's pyin algorithm
        
        See: https://librosa.org/doc/main/generated/librosa.yin.html
        """
        self.logger.info(f"Extracting melody using librosa from: {audio_path}")
        
        try:
            # TODO: Implement actual librosa + pyin extraction
            # 1. Load audio with librosa.load()
            # 2. Compute STFT
            # 3. Use pyin algorithm for pitch tracking
            # 4. Post-process and extract notes
            
            # Placeholder implementation
            contour = MelodyContour(
                pitches=[440.0, 442.0, 440.0],
                times=[0.0, 0.5, 1.0],
                confidence=[0.9, 0.95, 0.9]
            )
            
            notes = [
                Note(440.0, "A4", 0.0, 0.5, 0.9),
                Note(442.0, "A4", 0.5, 0.5, 0.95)
            ]
            
            vibrato = Vibrato(present=False)
            
            return MelodyAnalysis(
                contour=contour,
                notes=notes,
                vibrato=vibrato
            )
            
        except Exception as e:
            self.logger.error(f"Error in librosa extraction: {str(e)}")
            raise


# ============================================================================
# Main Service
# ============================================================================

class MelodyExtractor:
    """
    Service for extracting melodic information from audio files.
    
    Provides a high-level interface for melody extraction with support for
    multiple algorithms, note detection, vibrato analysis, and pitch contour
    extraction.
    
    Features:
        - Multiple extraction algorithms (librosa, BasicPitch, etc.)
        - Note-level analysis
        - Vibrato detection
        - Pitch contour smoothing
        - Vocal range estimation
        - Key detection support
    
    Examples:
        >>> extractor = MelodyExtractor()
        >>> analysis = extractor.extract_melody("song.mp3")
        >>> print(analysis.contour.pitch_range)
        >>> 
        >>> # Work with extracted notes
        >>> for note in analysis.notes:
        ...     print(f"{note.pitch_name}: {note.duration}s")
    """
    
    def __init__(self, method: ExtractionMethod = ExtractionMethod.LIBROSA):
        """
        Initialize the melody extractor
        
        Args:
            method: Extraction algorithm to use
        """
        self.logger = Logger.get_logger(__name__)
        self.method = method
        self.algorithm = self._create_algorithm(method)
        
        self.logger.info(f"MelodyExtractor initialized with method: {method.value}")
    
    def _create_algorithm(self, method: ExtractionMethod) -> BaseMelodyAlgorithm:
        """
        Factory method to create appropriate extraction algorithm
        
        Args:
            method: Extraction method enum
            
        Returns:
            Instance of algorithm class
        """
        if method == ExtractionMethod.LIBROSA:
            return LibrosaMelodyExtractor(self.logger)
        elif method == ExtractionMethod.BASICPITCH:
            # TODO: Implement BasicPitch extractor
            self.logger.warning("BasicPitch not yet implemented, using librosa")
            return LibrosaMelodyExtractor(self.logger)
        elif method == ExtractionMethod.MELODIA:
            # TODO: Implement Melodia extractor
            self.logger.warning("Melodia not yet implemented, using librosa")
            return LibrosaMelodyExtractor(self.logger)
        else:
            return LibrosaMelodyExtractor(self.logger)
    
    def extract_melody(self, audio_path: str) -> MelodyAnalysis:
        """
        Extract complete melodic analysis from audio file
        
        Args:
            audio_path: Path to audio file (MP3, WAV, FLAC, etc.)
            
        Returns:
            MelodyAnalysis object containing contour, notes, and vibrato
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
            ValueError: If audio format is not supported
        """
        if not os.path.exists(audio_path):
            self.logger.error(f"Audio file not found: {audio_path}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        file_ext = audio_path.split('.')[-1].lower()
        if file_ext not in ['mp3', 'wav', 'flac', 'ogg', 'm4a']:
            self.logger.error(f"Unsupported audio format: {file_ext}")
            raise ValueError(f"Unsupported audio format: {file_ext}")
        
        self.logger.info(f"Starting melody extraction: {audio_path}")
        
        try:
            # Use configured algorithm for extraction
            analysis = self.algorithm.extract(audio_path)
            
            # Post-process
            analysis = self._post_process_analysis(analysis)
            
            self.logger.info(f"Melody extraction completed: {len(analysis.notes)} notes detected")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error extracting melody: {str(e)}")
            raise
    
    def extract_from_notes(self, notes: List[Dict]) -> MelodyAnalysis:
        """
        Analyze melody characteristics from a list of notes
        
        Useful for analyzing MIDI files or pre-detected notes.
        
        Args:
            notes: List of note dictionaries with keys:
                - pitch/pitch_name: Note pitch
                - start_time: Note start in seconds
                - duration: Note duration in seconds
                - confidence: (optional) Confidence 0-1
            
        Returns:
            MelodyAnalysis with characteristics
        """
        self.logger.info(f"Analyzing melody from {len(notes)} notes")
        
        if not notes:
            self.logger.warning("No notes provided for analysis")
            return MelodyAnalysis(
                contour=MelodyContour([], [], []),
                notes=[],
                vibrato=Vibrato(present=False)
            )
        
        try:
            # Convert to Note objects
            note_objects = [
                Note(
                    pitch=note.get('pitch', 0),
                    pitch_name=note.get('pitch_name', ''),
                    start_time=note.get('start_time', 0),
                    duration=note.get('duration', 0),
                    confidence=note.get('confidence', 0.8)
                )
                for note in notes
            ]
            
            # Extract characteristics
            pitches = [n.pitch for n in note_objects]
            times = [n.start_time for n in note_objects]
            confidence = [n.confidence for n in note_objects]
            
            contour = MelodyContour(pitches, times, confidence)
            analysis = MelodyAnalysis(
                contour=contour,
                notes=note_objects,
                vibrato=Vibrato(present=False),
                intervals=self._calculate_intervals(pitches)
            )
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing notes: {str(e)}")
            raise
    
    def smooth_contour(self, analysis: MelodyAnalysis, 
                      window_size: int = 5) -> MelodyAnalysis:
        """
        Smooth melody contour to remove noise
        
        Args:
            analysis: Melody analysis to smooth
            window_size: Size of smoothing window
            
        Returns:
            Analysis with smoothed contour
        """
        self.logger.info(f"Smoothing melody contour (window: {window_size})")
        
        # TODO: Implement moving average or median filter
        # This is placeholder
        return analysis
    
    def detect_vibrato_in_analysis(self, analysis: MelodyAnalysis) -> Vibrato:
        """
        Detect vibrato in an analyzed melody
        
        Args:
            analysis: Melody analysis
            
        Returns:
            Vibrato object with detection results
        """
        self.logger.info("Detecting vibrato characteristics")
        
        # TODO: Implement vibrato detection
        # Look for periodic pitch variations (4-8 Hz typically)
        
        return Vibrato(present=False)
    
    def estimate_vocal_range(self, analysis: MelodyAnalysis) -> Tuple[str, str]:
        """
        Estimate vocal range from analysis
        
        Args:
            analysis: Melody analysis
            
        Returns:
            Tuple of (lowest_note, highest_note) as note names
        """
        self.logger.info("Estimating vocal range")
        
        # TODO: Implement vocal range estimation
        # Convert frequency range to note names
        
        return ("C4", "C6")
    
    def _post_process_analysis(self, analysis: MelodyAnalysis) -> MelodyAnalysis:
        """
        Post-process analysis (clean up, add metadata)
        
        Args:
            analysis: Raw analysis from algorithm
            
        Returns:
            Cleaned analysis with additional metadata
        """
        # Add vocal range estimate
        range_min, range_max = self.estimate_vocal_range(analysis)
        analysis.range_min = range_min
        analysis.range_max = range_max
        
        # Detect vibrato
        analysis.vibrato = self.detect_vibrato_in_analysis(analysis)
        
        return analysis
    
    def _calculate_intervals(self, pitches: List[float]) -> List[int]:
        """
        Calculate semitone intervals between consecutive notes
        
        Args:
            pitches: List of pitch values (Hz or MIDI number)
            
        Returns:
            List of intervals in semitones
        """
        if len(pitches) < 2:
            return []
        
        intervals = []
        for i in range(len(pitches) - 1):
            # TODO: Implement interval calculation
            # For now, placeholder
            intervals.append(0)
        
        return intervals
    
    def set_extraction_method(self, method: ExtractionMethod) -> None:
        """
        Change the extraction algorithm
        
        Args:
            method: New extraction method to use
        """
        self.logger.info(f"Changing extraction method to: {method.value}")
        self.method = method
        self.algorithm = self._create_algorithm(method)
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported audio formats"""
        return ['mp3', 'wav', 'flac', 'ogg', 'm4a']
    
    def get_available_methods(self) -> List[str]:
        """Get list of available extraction methods"""
        return [method.value for method in ExtractionMethod]
