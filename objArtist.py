import musicbrainzngs

musicbrainzngs.set_useragent("Spitify", "1.0", "Franco.Villafane@outlook.com")


class SearchArtist:
    def __init__(self,nombre_artista):
         self.Resultado = self.buscar_artista(nombre_artista)

    def buscar_artista(self, nombre_artista):
        try:
            resultado = musicbrainzngs.search_artists(artist=nombre_artista, limit=5)
            artistas = resultado['artist-list']
            lista_resultado = []
            for artista in artistas:
                artist = {
                            "Nombre": artista.get("name", "Desconocido"),
                            "ID": artista.get("id", "N/A"),
                            "Codigo_Pais": artista.get("country", "Codigo No Disponible"),
                            "Gender": artista.get("gender", "Genero No Disponible"),
                            "Nombre_Pais": artista.get("area",{}).get("name", "Pais Desconocido"),
                            "Tag_List": [tag['name'] for tag in artista.get("tag-list",[])],
                         }
                lista_resultado.append(artist)
            return lista_resultado
        except musicbrainzngs.ResponseError as e:
            print(f"Error en la solicitud: {e}")

buscar_artista = SearchArtist("Bjork")
print(len(buscar_artista.Resultado))
for artista in buscar_artista.Resultado:
    print(artista)

def obtener_discografia(artist_id):
    try:
        artista = musicbrainzngs.get_artist_by_id(artist_id, includes=["release-groups"])
        print(f"Discografía de {artista['artist']['name']}:")
        
        for release in artista['artist']['release-group-list']:
            print(f"- {release['title']} ({release['first-release-date']})")
    
    except musicbrainzngs.ResponseError as e:
        print(f"Error en la solicitud: {e}")

# Llamar a la función con un ID de artista
#obtener_discografia("87c5dedd-371d-4a53-9f7f-80522fb7f3cb")  # ID de Queen

# Buscar un álbum
def buscar_album(nombre_album):
    try:
        resultado = musicbrainzngs.search_releases(release=nombre_album, limit=5)
        albums = resultado['release-list']
        
        for album in albums:
            print(f"Título: {album['title']}")
            print(f"Artista: {album['artist-credit'][0]['artist']['name']}")
            print(f"Año: {album.get('date', 'Desconocido')}")
            print(f"ID de MusicBrainz: {album['id']}\n")
            
    except musicbrainzngs.ResponseError as e:
        print(f"Error en la solicitud: {e}")

# Llamar a la función
#buscar_album("Vespertine")

def obtener_tracklist(release_id):
    try:
        release = musicbrainzngs.get_release_by_id(release_id, includes=["recordings"])
        print(f"Tracklist para {release['release']['title']}:")

        for track in release['release']['medium-list'][0]['track-list']:
            print(f"{track['position']}. {track['recording']['title']} - Duración: {track.get('length', 'Desconocida')} ms")

    except musicbrainzngs.ResponseError as e:
        print(f"Error al obtener tracklist: {e}")

# Llamar a la función con el ID de un release
#obtener_tracklist("44f43a79-27f8-4eea-b547-97c7dc204da2")  # Ejemplo: Release específico

