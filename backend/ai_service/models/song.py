"""Song model"""


class Song:
    """Model representing a song"""
    
    def __init__(self, title, artist, file_path):
        """
        Initialize a Song instance
        
        Args:
            title (str): Song title
            artist (str): Artist name
            file_path (str): Path to audio file
        """
        self.title = title
        self.artist = artist
        self.file_path = file_path
        self.tracks = []
        self.duration = None
        self.sample_rate = None
    
    def add_track(self, track):
        """Add a track to the song"""
        self.tracks.append(track)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'title': self.title,
            'artist': self.artist,
            'file_path': self.file_path,
            'tracks': [track.to_dict() for track in self.tracks]
        }
