import os
import objSong as song

class Playlist:
    def __init__(self, directory):
        self.Playlist = self.Cargar_Playlist(directory)
    
    def Cargar_Playlist(self,directory):
        archivos = os.listdir(directory)
        canciones = [song.Song(f) for f in archivos if f.endswith(".mp3")]
        return canciones
    
    def Agregar_Cancion(self, nombre,directory):
            for f in os.listdir(directory):
                 if f == f"{nombre}.og":
                      Nueva_Cancion = song.Song(f)
                      self.Playlist.append(Nueva_Cancion)
                      break
    def Devolver_Index(self, nombre, directory):
         self.imprimir()
         for i, cancion in enumerate(self.Playlist):
              if cancion.filename == f"{nombre}.mp3":
                   return i 
    def imprimir(self):
        import os
        print("Directorio de trabajo actual:", os.getcwd())
        directory = "C:\\Users\\Franc\\source\\Spitify\\Cache"
        print("Archivos en Cache:")
        for f in os.listdir(directory):
            print(f)