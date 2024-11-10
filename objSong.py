from mutagen.mp3 import MP3
import os

class Song:
    def  __init__(self, filename):
        self.filename = filename
        self.title = os.path.splitext(filename)[0]
        self.duration = self.get_duration()
            
    def get_duration(self):
        audio = MP3(os.path.join("Cache", self.filename))
        return audio.info.length
    