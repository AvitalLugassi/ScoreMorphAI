"""Track model"""


class Track:
    """Model representing an audio track"""
    
    def __init__(self, track_id, name, channel_count=1):
        """
        Initialize a Track instance
        
        Args:
            track_id (str): Unique track identifier
            name (str): Track name
            channel_count (int): Number of audio channels
        """
        self.track_id = track_id
        self.name = name
        self.channel_count = channel_count
        self.duration = None
        self.sample_rate = None
        self.notes = []
    
    def add_note(self, note):
        """Add a note to the track"""
        self.notes.append(note)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'track_id': self.track_id,
            'name': self.name,
            'channel_count': self.channel_count,
            'duration': self.duration,
            'sample_rate': self.sample_rate,
            'notes_count': len(self.notes)
        }
