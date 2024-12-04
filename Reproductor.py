import flet as ft
import asyncio
import objSong as song
import Pantalla
import ObjBusqueda as Bsq
import objPlaylist as pl
import objArtist as art
import traceback
import vlc


async def main(page: ft.Page):
    page.title = "Reproductor de Música"
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.window.maximized = True
    #.padding = 20
    page.window.width = 700
    page.window.height = 800
    centrar = Pantalla.Pantalla(page.window.width, page.window.height)
    page.window.left = centrar.X_Pos
    page.window.top = centrar.Y_Pos
    playlist =pl.Playlist()
    player = None
    NuevaBusqueda = None
    Cancion = None
    Artista = None
    Listado = []

    #funciones
   
    async def update_progress():
            global player
            global Cancion
            while True:
                if player is not None:
                    if player.get_state() == vlc.State.Playing :
                        current_time = player.get_time() /1000
                        progress_bar.value = current_time / Cancion.duration
                        current_time_text.value = format_time(current_time)
                        page.update()
                    elif player.get_state() == vlc.State.Ended:
                        mockControl = song.MockControl(data=1)
                        eventMock = song.EventMock(mockControl)
                        change_song(eventMock) 
                    await asyncio.sleep(1) 

    def update_progress_position(e: ft.ContainerTapEvent):
        global Cancion
        global player
        relative_position = e.local_x / progress_bar.width
        new_time = relative_position * Cancion.duration
        player.set_time(int(new_time * 1000))
        page.update()
    
    def load_song():
        global Cancion
        global player
        playing = False
        try:
            if player.get_state() == vlc.State.Playing:
                player.stop()
                playing = True
                player = None
        except:
            pass
        Cancion = song.Song(playlist.State[current_song_index])
        player = vlc.MediaPlayer(Cancion.Url)
        if playing:
            player.play()

        
    def play_Pause(e):
        global player
        state = player.get_state()
        if state == vlc.State.Playing:
            player.pause()
            play_button.icon = ft.icons.PLAY_ARROW
        elif state == vlc.State.Paused:
            player.play()
            play_button.icon = ft.icons.PAUSE
        elif state == vlc.State.NothingSpecial:
            player.play()
            play_button.icon = ft.icons.PAUSE
        else:
            player.play()
            play_button.icon = ft.icons.PAUSE
        page.update()
    
    def stop(e):
        global player
        player.stop()
        play_button.icon = ft.icons.PLAY_ARROW
        page.update()
    
    def Mute(e):
        global player
        if player.audio_get_volume() > 0:
            volume_button.icon = ft.icons.VOLUME_OFF
            player.audio_set_volume(0)
        else:
           volume_button.icon = ft.icons.VOLUME_UP 
           player.audio_set_volume(100)
           volume_slider.value = 1
           
    
    def set_volume(e):
        global player
        player.audio_set_volume(int(e.control.value * 100))
        if e.control.value > 0:
            if e.control.value < 0.6:
                volume_button.icon = ft.icons.VOLUME_DOWN
            else:
                volume_button.icon = ft.icons.VOLUME_UP
        else:
            volume_button.icon = ft.icons.VOLUME_OFF

    def change_song(e):
        global player
        nonlocal current_song_index
        current_song_index = (current_song_index+e.control.data) % len(playlist.State)
        load_song()
        update_song_info()
        if player.get_state() == vlc.State.NothingSpecial:
            player.play()
        play_button.icon = ft.icons.PAUSE
        page.update()

    def update_song_info():
        global Cancion
        song_info.value = Cancion.Name
        duration.value = format_time(Cancion.duration)
        progress_bar.value = 0.0
        current_time_text.value = "00:00"
        Miniatura.src = Cancion.thumbnail
        Nombre.value = Cancion.Name
        Likes.value = format_number(Cancion.like_count)
        Views.value = format_number(Cancion.view_count)
        page.update()
    
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds),60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def format_number(num):
        if num >= 1_000_000: 
                return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000: 
                return f"{num / 1_000:.1f}K"
        return str(num)

    def CompletarPlaylist():
        for cancion in playlist.State:
            nuevaCancion = song.Song(cancion.Url)
            Listado.append(nuevaCancion)

    async def Buscar_Artista(busqueda):
        global Artista
        resultado = art.buscar_artista(busqueda)
        Artista = resultado[0] 
        resultado_artista.value = Artista.Nombre
        artista_bio.value = ", ".join(Artista.Tag_List)
        discography_button.visible = True
        texto_Resultado.visible = True
        page.update()

    async def mostrar_discografia(e):
        global Artista
        Artista.Discografia = Artista.obtener_discografia_oficial()
        Resultado_Discografia = ft.Column()
        for album in Artista.Discografia:
            columna_discografia = ft.Row(
                controls=[
                    ft.Image(src=album.Thumbnail, width=100, height=100, fit=ft.Image.fit),
                    ft.Column(
                        controls=[
                            ft.Text(album.Title, size=16, weight="bold"),
                            ft.Text(album.First_Release_Date, size=12)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=2
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            )
            Resultado_Discografia.controls.append(columna_discografia)
            listado_discografia.content=ft.Column(
                                controls=[
                                        ft.Row(
                                                controls=[Resultado_Discografia],
                                                alignment=ft.MainAxisAlignment.START
                                            )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
        page.update()

    def Buscar_Canciones(e):
        global NuevaBusqueda
        NuevaBusqueda = Bsq.Busqueda(e.control.value)
        Resultado_Busqueda = ft.Column()
        asyncio.run(Buscar_Artista(e.control.value))
        for index, row in NuevaBusqueda.Dataframe.iterrows():
            popup_menu = ft.PopupMenuButton(
            icon=ft.icons.MORE_VERT,
            items=[
                ft.PopupMenuItem(text="Reproducir ahora", data=row["title"], icon=ft.icons.PLAY_ARROW,on_click=Reproducir_Cancion),
                ft.PopupMenuItem(text="Agregar a la cola", data=row["title"],icon=ft.icons.QUEUE,on_click=Cargar_Cancion),
                ft.PopupMenuItem(text="Ver detalles", data=row["title"],icon=ft.icons.INFO),
            ], 
        )
            
            video_row = ft.Row(
                [
                    ft.Column(
                        [
                            ft.GestureDetector(
                                content=ft.Image(
                                    src=NuevaBusqueda.Minitaturas["thumbnails"][index], 
                                    width=400, 
                                    height=200, 
                                    fit=ft.alignment.center,
                                    
                                    ),
                                on_tap=Reproducir_Cancion,
                                data=row["title"],
                            ),
                                ft.Row([
                                
                                ft.Text(
                                    row["title"], 
                                    size=16, 
                                    weight="bold",
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    text_align= ft.TextAlign.CENTER,
                                    width=340
                                    ),
                                popup_menu],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                
                                )
                ], 
                alignment=ft.CrossAxisAlignment.CENTER, 
                horizontal_alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
            Resultado_Busqueda.controls.append(video_row)
        listado_canciones.content=ft.Column(
                                controls=[
                                        ft.Row(
                                                controls=[Resultado_Busqueda],
                                                alignment=ft.MainAxisAlignment.START
                                            )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
        page.update()
    

    def Cargar_Cancion(e):
        try:
            global NuevaBusqueda
            global Cancion
            listado = NuevaBusqueda.DevolverListado()
            key = [key for key, value in listado.items() if value == e.control.data]
            playlist.Agregar_Cancion(NuevaBusqueda.DevolverLink(key))

        except Exception as ex:
            error = traceback.format_exc()
            print(error)

    def Reproducir_Cancion(e):
        global NuevaBusqueda
        global Cancion
        nonlocal current_song_index
        listado = NuevaBusqueda.DevolverListado()
        key = [key for key, value in listado.items() if value == e.control.data]
        playlist.Agregar_Cancion(NuevaBusqueda.DevolverLink(key),current_song_index)
        load_song()
        update_song_info()
        page.update()



    def Actualizar():
        load_song()
        update_song_info()
        page.update()
        

    current_song_index = 0
    song_info = ft.Text(size=20, color=ft.colors.WHITE)
    current_time_text = ft.Text(value="00:00", color=ft.colors.WHITE60)
    duration = ft.Text(color=ft.colors.WHITE60)
    progress_bar = ft.ProgressBar(value=0.0, width=300, height=10, color="white", bgcolor=ft.colors.GREY_900)
    progress_container = ft.Container(content=progress_bar,on_tap_down=update_progress_position,width=300, height=10)
    discography_button = ft.TextButton("Ver Discografia",icon=ft.icons.MY_LIBRARY_MUSIC, on_click=mostrar_discografia, icon_color=ft.colors.WHITE, visible=False)
    play_button = ft.IconButton(icon=ft.icons.PLAY_ARROW, on_click=play_Pause, icon_color=ft.colors.WHITE)
    next_button = ft.IconButton(icon=ft.icons.SKIP_NEXT, on_click= change_song,data=1, icon_color=ft.colors.WHITE)
    prev_button = ft.IconButton(icon=ft.icons.SKIP_PREVIOUS, on_click=change_song, data=-1,icon_color=ft.colors.WHITE)
    stop_button = ft.IconButton(icon=ft.icons.STOP_CIRCLE, on_click=stop, icon_color=ft.colors.WHITE)
    volume_button = ft.IconButton(icon=ft.icons.VOLUME_UP, on_click=Mute,icon_color=ft.colors.WHITE)
    volume_slider = ft.Slider(min=0, max=1, value=1, divisions=10,width=200, on_change_end=set_volume,active_color=ft.colors.WHITE)
    Busqueda = ft.TextField(label="Con qué te vas a deleitar?",hint_text="Escriba un artista o canción.", width=500 ,icon=ft.icons.SEARCH,on_submit=Buscar_Canciones,text_align=ft.TextAlign.CENTER, border_radius=ft.border_radius.all(50))
    Miniatura = ft.Image(width=100, height=100,fit=ft.Image.left)
    Nombre = ft.Text(size=12, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS,text_align=ft.TextAlign.CENTER, color=ft.colors.WHITE,width=200)
    Likes = ft.Text(size=9, weight="bold", text_align=ft.TextAlign.CENTER, color=ft.colors.WHITE)
    Views = ft.Text(size=9, weight="bold", text_align=ft.TextAlign.CENTER, color=ft.colors.WHITE)
    resultado_artista = ft.Text(size=20, color=ft.colors.WHITE, width=250)
    artista_bio = ft.Text(size=12, color=ft.colors.WHITE, max_lines=2,overflow=ft.TextOverflow.ELLIPSIS, width=300)

    listado_canciones = ft.Container(
        alignment=ft.alignment.center,
        width=400, 
        height=585, 
        adaptive= False,
    )
    listado_discografia = ft.Container(
        alignment=ft.alignment.center,
        width=600, 
        height=385, 
        adaptive= False,
    )
    fila_busqueda = ft.Row(controls=[Busqueda], alignment=ft.MainAxisAlignment.CENTER,width=600)
    fila_titulo = ft.Row(controls=[song_info], alignment=ft.MainAxisAlignment.CENTER)
    fila_controles = ft.Row(controls=[prev_button,play_button,stop_button, next_button], 
                      alignment=ft.MainAxisAlignment.CENTER,
                      )
    fila_reproductor = ft.Row(controls=[current_time_text, progress_container, duration],
                              alignment=ft.MainAxisAlignment.CENTER,
                              vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
    fila_volume = ft.Row(controls=[volume_button, volume_slider],
                         alignment=ft.MainAxisAlignment.CENTER,
                         vertical_alignment=ft.CrossAxisAlignment.CENTER
                         )
    columna_busqueda = ft.Column(controls=[fila_busqueda],alignment=ft.MainAxisAlignment.CENTER)
    columna_reproductor = ft.Column(controls=[fila_titulo, fila_reproductor, fila_controles],
                        alignment=ft.MainAxisAlignment.END, spacing=20,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        )
    columna_volume = ft.Column(controls=[fila_volume],
                        alignment=ft.MainAxisAlignment.END, spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                               )
    fila_info = ft.Row(controls=[Miniatura,Nombre],alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER,spacing=2) 
    fila_likeView = ft.Row(controls=[ft.Icon(ft.icons.THUMB_UP, color=ft.colors.WHITE, size=10), Likes, ft.Icon(ft.icons.VISIBILITY,color=ft.colors.WHITE,size=10) ,Views],spacing=6,alignment=ft.MainAxisAlignment.CENTER)
    fila_listado = ft.Row(controls=[listado_canciones], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    fila_discografia = ft.Row(controls=[listado_discografia], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    texto_Resultado = ft.Text("Resultado Principal", size=16, color=ft.colors.WHITE, visible=False)
    columna_info = ft.Column(controls=[fila_info, 
                        ft.Row([fila_likeView],spacing=1)],
                        alignment=ft.MainAxisAlignment.END, spacing=1,
                        horizontal_alignment=ft.CrossAxisAlignment.START)
    columna_izquierda = ft.Column(
    controls=[
        texto_Resultado,
        resultado_artista, 
        artista_bio,
        discography_button
                ],
    expand=True,
    width=500,
    alignment= ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
    columna_derecha = ft.Container(content=ft.Text("Derecha (vacío)"), expand=True,  width=500)

    fila_superior = ft.Row([columna_busqueda], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START)

    page.add( fila_superior, ft.Container(
        ft.Row(
            [
                ft.Column(
                    [columna_izquierda, fila_discografia],  # columna_izquierda, 
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    expand=False,
                    width=500
                ),
                ft.Column(
                    [fila_listado],  # Columna del medio
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    width=500
                ),
                ft.Column(
                    [columna_derecha],  # Columna de la derecha vacía
                    alignment=ft.MainAxisAlignment.END,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    expand=False,
                    width=500
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=ft.Window.width,
        ),
        border_radius=ft.border_radius.all(8),
        width=ft.Window.width,
    ),
             ft.Container(
                ft.Row([ft.Column([columna_info],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=False,
                        ),
                        ft.Column([columna_reproductor],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=False,
                        ),
                        ft.Column([columna_volume],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        expand=False,
                        )],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        width= ft.Window.width
                        ),
                bgcolor=ft.colors.BLACK87,
                border_radius=ft.border_radius.all(8),
                width=ft.Window.width
                ),
            )
    
    if playlist.State:
        Actualizar()
        await update_progress()
    else:
        song_info =  "No se encontraron canciones en la carpeta de canciones"
        page.update()

ft.app(target=main,view=ft.AppView.FLET_APP_HIDDEN)

