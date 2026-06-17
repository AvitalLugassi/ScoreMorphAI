"""Score model"""


class Score:
    """Model representing a musical score"""
    
    def __init__(self, song_id, title):
        """
        Initialize a Score instance
        
        Args:
            song_id (str): Associated song ID
            title (str): Score title
        """
        self.song_id = song_id
        self.title = title
        self.measures = []
        self.tempo = 120
        self.time_signature = '4/4'
        self.key_signature = 'C'
    
    def add_measure(self, measure):
        """Add a measure to the score"""
        self.measures.append(measure)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'song_id': self.song_id,
            'title': self.title,
            'tempo': self.tempo,
            'time_signature': self.time_signature,
            'key_signature': self.key_signature,
            'measures': self.measures
        }
