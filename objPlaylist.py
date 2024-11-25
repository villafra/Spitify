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

    def Agregar_Cancion(self, url, index=None):
        if index is not None:
            self.State.insert(index,url)
        else:
            self.State.append(url)
        self.Guardar_State()
    
    def Guardar_State(self):
        ruta = "Cache/state.bin"
        try:
             with open(ruta, "wb") as f:
                 for url in self.State:
                    f.write((url + "\n").encode("utf-8"))
        except Exception as ex:
            print(ex)

                 