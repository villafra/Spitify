import musicbrainzngs
import objCripto as cript
import datetime

usuario = "villafra007"
password = b'gAAAAABnTLdY-0z-GUrbS7zUt71cBQ6msAoy_lBK0kOic4yZntgGTf7d1L_cBFeRv7hwkRNzca3Q9lKy3Yil4-wLN343siZ-rQ=='
cripto = cript.Cripto(password)

musicbrainzngs.auth(usuario, cripto.descifrar_contraseña())
musicbrainzngs.set_useragent("Spitify", "1.0", "Franco.Villafane@outlook.com")
musicbrainzngs.set_rate_limit(limit_or_interval=1.0, new_requests=1)


class Artist:
    def __init__(self):
        self.ID = None
        self.Nombre = None
        self.Pais = None
        self.Genero = None
        self.Tag_List = []
        self.Discografia = None
    
    def obtener_discografia_oficial(self):
        try:
            Discografia = []
            offset = 0
            limit = 100  
            
            while True:
                resultado = musicbrainzngs.browse_release_groups(
                    artist=self.ID,
                    includes=["artist-credits", "tags", "ratings"],
                    release_type=['album'],
                    limit=limit,
                    offset=offset
                )
                release_groups = resultado.get('release-group-list', [])
                if not release_groups:
                    break
                for release_group in release_groups:
                    primary_type = release_group.get("primary-type", "")
                    secondary_types = release_group.get("secondary-type-list", [])
                    if primary_type == "Album" and not secondary_types:
                        album = Album()
                        album.ID = release_group.get('id', 'N/A')
                        album.Title = release_group.get('title', 'N/A')
                        album.Primary_Type = release_group.get('primary-type', 'N/A')
                        album.Secondary_Types = ', '.join(release_group.get('secondary-type-list', []))
                        album.First_Release_Date = release_group.get('first-release-date', 'N/A')
                        album.Tags = [tag['name'] for tag in release_group.get('tag-list', [])]
                        album.Obtener_Imagen()
                        Discografia.append(album)
                
                offset += limit
            Discografia.sort(key=lambda x: x.First_Release_Date if x.First_Release_Date != 'N/A' else '')
            return Discografia
        except musicbrainzngs.ResponseError as e:
            print(f"Error en la solicitud: {e}")
            return []

    def __str__(self):
        return f"Artista: {self.Nombre}, Pais: {self.Pais}, Genero: {self.Genero}"
    
    def __repr__(self):
        return self.__str__()

class Album:
    def __init__(self):
        self.ID = None
        self.ID_Release = None
        self.Title = None
        self.Primary_Type = None
        self.Secondary_Types = None
        self.First_Release_Date = None
        self.Tags = []
        self.Song_List = []
        self.Thumbnail = None
    

    def obtener_Id_disco(self):
        try:
            resultado = musicbrainzngs.get_release_group_by_id(
                self.ID,
                includes=["releases"]
            )
            releases = resultado.get("release-group", {}).get("release-list", [])
            if not releases:
                self.ID_Release = None
            releases_ordenados = sorted(releases, key=lambda x: x.get("date", "9999-12-31"))
            self.ID_Release = releases_ordenados[0].get("id")  
        except musicbrainzngs.ResponseError as e:
            print(f"Error al obtener lanzamientos: {e}")
            self.ID_Release = None

    def Obtener_Imagen(self):
        try:
            imagenes = musicbrainzngs.get_release_group_image_list(self.ID)
            if 'images' in imagenes:
                for imagen in imagenes['images']:
                    if imagen.get("front", False):  
                        self.Thumbnail = imagen.get("image", "https://upload.wikimedia.org/wikipedia/commons/d/da/Imagen_no_disponible.svg")
                        break 
            else:
                self.Thumbnail = "https://upload.wikimedia.org/wikipedia/commons/d/da/Imagen_no_disponible.svg"
        except musicbrainzngs.ResponseError as e:
            print(f"Error al obtener imágenes: {e}")
            self.Thumbnail = "https://upload.wikimedia.org/wikipedia/commons/d/da/Imagen_no_disponible.svg"
        
    def obtener_tracklist(self):
        self.obtener_Id_disco()
        if self.ID_Release:
            try:
                release = musicbrainzngs.get_release_by_id(self.ID_Release, includes=["artists", "recordings"])
                listado = []
                for track in release['release']['medium-list'][0]['track-list']:
                    cancion = SongList()
                    cancion.ID = track.get("recording",{}).get("id","N/A")
                    cancion.Position = track.get("position", "N/A")
                    cancion.Title = track.get("recording",{}).get("title","N/A")
                    cancion.Length = track.get("length", "Desconocida")
                    listado.append(cancion)
                return listado
            except musicbrainzngs.ResponseError as e:
                print(f"Error al obtener tracklist: {e}")
        else:
             print(f"Error al obtener tracklist: {e}")

    def __str__(self):
        return f"Album: {self.Title} ({self.First_Release_Date}) - {self.Secondary_Types}"
    
    def __repr__(self):
        return self.__str__()

class SongList:
    def __init__(self):
        self.ID = None
        self.Position = None
        self.Title = None
        self.Length = None
        self.Lyrics = None
    
    def format_time(self, miliseconds):
        seconds = int(miliseconds)/1000
        minutes, seconds = divmod(int(seconds),60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def __str__(self):
        return(f"{self.Position.zfill(2)} - {self.Title}. Duration: {self.format_time(self.Length)}")

    def __repr__(self):
        return self.__str__()



def buscar_artista(nombre_artista):
    try:
        resultado = musicbrainzngs.search_artists(artist=nombre_artista, limit=5)
        artistas = resultado['artist-list']
        lista_resultado = []
        for artista in artistas:
            artist = Artist()
            artist.ID = artista.get("id", "N/A")
            artist.Nombre = artista.get("name", "Desconocido")
            artist.Genero = artista.get("gender", "Genero No Disponible")
            artist.Pais = f"{artista.get("area",{}).get("name", "Pais Desconocido")} ({artista.get("country", "Codigo No Disponible")})"
            artist.Tag_List = [tag['name'] for tag in artista.get("tag-list",[])]
            lista_resultado.append(artist)
        return lista_resultado
    except musicbrainzngs.ResponseError as e:
        print(f"Error en la solicitud: {e}")


