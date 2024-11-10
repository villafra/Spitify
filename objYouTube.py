import pytubefix as pyt
from pydub import AudioSegment
import time
import os
import subprocess
import re

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
    
    def Bajar_Audio(self, nombre, tag=0):
        if tag > 0:
            self.Audio = self.YouTube.streams.get_by_itag(tag).download(output_path="Cache",filename="data.mp3",skip_existing=False)
        else:
            self.Audio = self.YouTube.streams.get_audio_only().download(output_path="Cache",filename="data.mp3",skip_existing=False)
        self.Mmpeg_forcer(nombre)
    
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
    
    def Mmpeg_forcer(self, nombre):
        max_number = self.obtener_numero_maximo()
        max_number += 1
        tema = f"{max_number:02d} - {nombre}.mp3"
        audio = AudioSegment.from_file("Cache/data.mp3")
        self.Audio = audio.export(f"Cache/{tema}", format="mp3")
        self.BorrarCache()
        
    def BorrarCache(self):
        archivo = "Cache/data.mp3"
        if os.path.exists(archivo):
            os.remove(archivo)

    @staticmethod
    def onProgress(stream=None, chunk=None, remaining=None):
        file_size = stream.filesize / 1000000
        file_download = file_size - (remaining / 1000000)  
        return file_download      

    def obtener_numero_maximo(self):
        max_num = 0
        patron = re.compile(r"^(\d{2}) - .+\.mp3$")
        for cancion in os.listdir("Cache"):
            match = patron.match(cancion)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num
        return max_num
    
    def Limpiar_Cache(self, nombre):
        reset_nombre = "01 - " + nombre.split(" - ", 1)[1]
        for cancion in os.listdir("Cache:"):
            if cancion != nombre and cancion.endswith(".mp3"):
                os.remove(os.path.join("Cache", nombre),os.path.join("Cache", reset_nombre))
        os.rename()