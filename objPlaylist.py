import os
import objSong as song

class Playlist:
    def __init__(self):
        self.State = self.Cargar_State()
        self.Playlist = None
    
    def Cargar_State(self):
        ruta = "Cache/state.bin"
        try:
            with open(ruta, "rb") as f:
                state = f.read().decode("utf-8")
                return state.splitlines()
        except FileNotFoundError:
            with open(ruta, "wb") as f:
                pass
            return []
        except Exception as e:
            return []
        
    def Cargar_Playlist(self):
        pass

    def Agregar_Cancion(self,url):
        self.State.append(url)