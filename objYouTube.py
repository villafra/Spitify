import pytubefix as pyt

class objYouTube:
    def __init__(self, url):
        self.URL = url
        self.YouTube = pyt.YouTube(self.URL, on_progress_callback=objYouTube.onProgress)
        self.Stream = []
        self.Titulo = self.YouTube.title
        self.Autor = self.YouTube.author
        self.Descripcion = self.YouTube.description
        self.Duración = self.format_time(self.YouTube.length)
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
            self.Audio = self.YouTube.streams.get_by_itag(tag).download(output_path="Caché",filename="audio.dat",skip_existing=False)
        else:
            self.Audio = self.YouTube.streams.get_audio_only().download(output_path="Caché",filename="audio.dat",skip_existing=False)
    
    def Bajar_Video(self, tag=0, max=False, min=False):
        if tag > 0:
            self.Video = self.YouTube.streams.get_by_itag(tag).download()
        elif max:
            self.Video = self.YouTube.streams.get_highest_resolution().download()
        elif min:
            self.Video = self.YouTube.streams.get_lowest_resolution().download()
        else:
            self.Video = self.YouTube.streams.filter(progressive=True).first().download()

    def format_time(self, seconds):
        minutes, seconds = divmod(int(seconds),60)
        return f"{minutes:02d}:{seconds:02d}"
            
    @staticmethod
    def onProgress(stream=None, chunk=None, remaining=None):
        file_size = stream.filesize / 1000000
        file_download = file_size - (remaining / 1000000)  
        return file_download      

