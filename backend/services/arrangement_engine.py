"""Arrangement and orchestration engine"""

import os
from typing import List, Dict, Optional
from utils.logger import Logger


class ArrangementEngine:
    """Service for creating arrangements and orchestrations"""
    
    def __init__(self):
        """Initialize the arrangement engine"""
        self.logger = Logger.get_logger(__name__)
        self.instruments = self._load_instrument_library()
        self.logger.info("ArrangementEngine initialized")
    
    def _load_instrument_library(self) -> Dict:
        """Load available instruments and their properties"""
        return {
            'piano': {'range': 'A0-C8', 'category': 'keyboard'},
            'violin': {'range': 'G3-A7', 'category': 'string'},
            'cello': {'range': 'C2-A5', 'category': 'string'},
            'flute': {'range': 'C4-D7', 'category': 'woodwind'},
            'guitar': {'range': 'E2-E4', 'category': 'string'},
            'trumpet': {'range': 'E3-B5', 'category': 'brass'},
            'drums': {'range': 'N/A', 'category': 'percussion'},
            'vocals': {'range': 'E2-E5', 'category': 'voice'}
        }
    
    def create_arrangement(self, melody: Dict, chords: Dict, 
                          style: str = 'pop') -> Dict:
        """
        Create an arrangement from melody and chords
        
        Args:
            melody (dict): Extracted melody
            chords (dict): Detected chords
            style (str): Arrangement style ('pop', 'classical', 'jazz', etc.)
            
        Returns:
            dict: Complete arrangement with instrument parts
        """
        self.logger.info(f"Creating {style} arrangement")
        
        try:
            arrangement = {
                'style': style,
                'parts': {},
                'instrumentation': self._suggest_instrumentation(style),
                'voicings': {},
                'dynamics': [],
                'texture': self._suggest_texture(style)
            }
            
            # Create parts for each instrument
            for instrument in arrangement['instrumentation']:
                arrangement['parts'][instrument] = {
                    'notes': [],
                    'dynamics': [],
                    'articulations': []
                }
            
            self.logger.info(f"Arrangement created with {len(arrangement['parts'])} parts")
            return arrangement
            
        except Exception as e:
            self.logger.error(f"Error creating arrangement: {str(e)}")
            raise
    
    def _suggest_instrumentation(self, style: str) -> List[str]:
        """Suggest instruments based on style"""
        style_configs = {
            'pop': ['piano', 'guitar', 'bass', 'drums', 'vocals'],
            'classical': ['violin', 'cello', 'piano'],
            'jazz': ['piano', 'guitar', 'bass', 'drums'],
            'ambient': ['piano', 'pad', 'effects'],
            'folk': ['guitar', 'vocals', 'percussion']
        }
        
        return style_configs.get(style, ['piano', 'violin'])
    
    def _suggest_texture(self, style: str) -> Dict:
        """Suggest textural approach based on style"""
        textures = {
            'pop': {'density': 'medium', 'layers': 3},
            'classical': {'density': 'rich', 'layers': 4},
            'jazz': {'density': 'sparse', 'layers': 2},
            'ambient': {'density': 'thin', 'layers': 2}
        }
        
        return textures.get(style, {'density': 'medium', 'layers': 3})
    
    def add_harmony(self, melody: Dict, chords: Dict, 
                   voicing_style: str = 'closed') -> Dict:
        """
        Add harmonic layers to melody
        
        Args:
            melody (dict): Main melody
            chords (dict): Chord progression
            voicing_style (str): 'closed', 'open', or 'spread'
            
        Returns:
            dict: Melody with added harmony parts
        """
        self.logger.info(f"Adding harmony with {voicing_style} voicing")
        
        harmony = {
            'melody': melody,
            'harmony_parts': [],
            'voicing_style': voicing_style,
            'harmony_density': 0
        }
        
        return harmony
    
    def add_accompaniment(self, chords: Dict, tempo: Dict,
                         instrument: str = 'piano') -> Dict:
        """
        Create accompaniment from chords
        
        Args:
            chords (dict): Chord progression
            tempo (dict): Tempo information
            instrument (str): Instrument for accompaniment
            
        Returns:
            dict: Accompaniment pattern and notes
        """
        self.logger.info(f"Creating {instrument} accompaniment")
        
        accompaniment = {
            'instrument': instrument,
            'pattern_type': 'arpeggio',
            'notes': [],
            'dynamics': [],
            'rhythm': []
        }
        
        return accompaniment
    
    def apply_dynamics(self, arrangement: Dict, intensity_curve: List[float]) -> Dict:
        """
        Apply dynamics based on intensity curve
        
        Args:
            arrangement (dict): Arrangement to modify
            intensity_curve (list): Intensity values over time (0-1)
            
        Returns:
            dict: Arrangement with applied dynamics
        """
        self.logger.info(f"Applying dynamics curve")
        
        arrangement['dynamics_applied'] = True
        arrangement['intensity_curve'] = intensity_curve
        
        return arrangement
    
    def suggest_orchestration(self, duration: float, 
                            mood: str = 'neutral') -> Dict:
        """
        Suggest orchestration based on piece properties
        
        Args:
            duration (float): Duration in seconds
            mood (str): Piece mood ('happy', 'sad', 'energetic', etc.)
            
        Returns:
            dict: Orchestration suggestions
        """
        self.logger.info(f"Suggesting orchestration for {mood} mood")
        
        orchestration = {
            'mood': mood,
            'primary_instruments': self._get_mood_instruments(mood),
            'texture': self._get_mood_texture(mood),
            'dynamics_range': self._get_mood_dynamics(mood)
        }
        
        return orchestration
    
    def _get_mood_instruments(self, mood: str) -> List[str]:
        """Get suitable instruments for mood"""
        mood_map = {
            'happy': ['piano', 'violin', 'flute'],
            'sad': ['cello', 'violin'],
            'energetic': ['drums', 'brass', 'strings'],
            'calm': ['piano', 'strings', 'pad']
        }
        
        return mood_map.get(mood, ['piano'])
    
    def _get_mood_texture(self, mood: str) -> str:
        """Get suitable texture for mood"""
        texture_map = {
            'happy': 'light',
            'sad': 'sparse',
            'energetic': 'dense',
            'calm': 'warm'
        }
        
        return texture_map.get(mood, 'neutral')
    
    def _get_mood_dynamics(self, mood: str) -> Dict:
        """Get suitable dynamic range for mood"""
        return {
            'min': 30,
            'max': 120
        }
    
    def export_parts(self, arrangement: Dict, format: str = 'musicxml') -> Dict:
        """
        Export arrangement parts
        
        Args:
            arrangement (dict): Arrangement to export
            format (str): Export format
            
        Returns:
            dict: Exported parts and file paths
        """
        self.logger.info(f"Exporting arrangement parts as {format}")
        
        export = {
            'format': format,
            'parts': {},
            'score': None
        }
        
        return export
