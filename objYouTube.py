import pytubefix as pyt

class objYouTube:
    def __init__(self, url):
        self.URL = url
        self.YouTube = pyt.YouTube(self.URL)
        self.Stream = []
        self.Titulo = self.YouTube.title
        self.Tamaño = None
        self.Audio = None
        self.Video = None

    def Audio_Streams(self):
        opciones_Stream = self.YouTube.streams.filter(only_audio=True)
        return sorted(opciones_Stream, key=lambda x: int(x.itag))
    
    def Video_Streams(self):
        opciones_Stream = self.YouTube.streams.filter(only_video=True)
        return sorted(opciones_Stream, key=lambda x: int(x.itag))

    def Devolver_Tamaño(self):
        tamaño = self.Stream.file_size / 1000000
        return tamaño
    
    def Bajar_Audio(self, tag=0):
        if tag > 0:
            self.Audio = self.YouTube.streams.get_by_itag(tag).download("uno.mp3",skip_existing=False,mp3=True)
        else:
            self.Audio = self.YouTube.streams.get_audio_only()
    
    def Bajar_Video(self, tag=0, max=False, min=False):
        if tag > 0:
            self.Video = self.YouTube.streams.get_by_itag(tag).download()
        elif max:
            self.Video = self.YouTube.streams.get_highest_resolution().download()
        elif min:
            self.Video = self.YouTube.streams.get_lowest_resolution().download()
        else:
            self.Video = self.YouTube.streams.filter(progressive=True).first().download()
            
            

