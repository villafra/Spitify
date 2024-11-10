import flet as ft
import pygame
import os
from mutagen.mp3 import MP3
import asyncio
import objSong as song
import Pantalla
import ObjBusqueda as Bsq
import objYouTube as Yt
import objPlaylist as pl
import time
import traceback
import Watcher
import atexit



is_playing = False
progress_task = None

async def main(page: ft.Page):
    page.title = "Reproductor de Música"
    page.bgcolor = ft.colors.BLUE_GREY_900
    #.padding = 20
    page.window.width = 600
    page.window.height = 800
    centrar = Pantalla.Pantalla(page.window.width, page.window.height)
    page.window.left = centrar.X_Pos
    page.window.top = centrar.Y_Pos
    pg = pygame.mixer
    pg.init()
    playlist = pl.Playlist("Cache")
    NuevaBusqueda = None
    watcher =  None
    Cancion = None
    page.on_close = lambda e: RegistrarCierre()
    

    #funciones
    def RegistrarCierre():
        global Cancion
        nonlocal current_song_index
        Cancion.Limpiar_Cache(playlist.Playlist[current_song_index].filename)    

    def Iniciar():
        nonlocal pg
        nonlocal current_song_index
        current_song_index = 0
        pygame.init()
        pg.init()
        #playlist.Playlist = playlist.Cargar_Playlist("Cache")
        update_song_info()
        #time.sleep(2)
        #if pg.music.get_pos()== -1:
            #load_song()
            #pg.music.play()  
        #else:
            #pg.music.unpause()
        #play_button.icon = ft.icons.PAUSE
        page.update()

    def Detener():
        stop(centrar)
        nonlocal pg
        pg.quit()
        pygame.quit()
    
    def load_song():
        nonlocal pg
        directorio_trabajo = os.getcwd() + f"\Cache"
        pathjoin = os.path.join(directorio_trabajo, playlist.Playlist[current_song_index].filename)
        pg.music.load(pathjoin)
    
    def load_newsong(nombre):
        playlist.Playlist = playlist.Cargar_Playlist("Cache")
        nonlocal pg
        directorio_trabajo = os.getcwd() + f"\Cache"
        pathjoin = os.path.join(directorio_trabajo,f"{nombre}.mp3" )
        global watcher
        while watcher.check_for_new_file() == False:
            time.sleep(1)
        page.update()


    
    def play_Pause(e):
        nonlocal pg
        if pg.music.get_busy():
            pg.music.pause()
            play_button.icon = ft.icons.PLAY_ARROW
        else:
            if pg.music.get_pos()== -1:
                load_song()
                pg.music.play()   
            else:
                pg.music.unpause()
            play_button.icon = ft.icons.PAUSE
        page.update()
    
    def stop(e):
        nonlocal pg
        if pg.music.get_busy():
            pg.music.stop()
            
        elif pg.music.get_pos()!= -1:
            pg.music.stop()
        play_button.icon = ft.icons.PLAY_ARROW
        page.update()
        RegistrarCierre()
    
    def change_song(e):
        nonlocal current_song_index
        current_song_index = (current_song_index+e.control.data) % len(playlist.Playlist)
        load_song()
        nonlocal pg
        pg.music.play()
        update_song_info()
        play_button.icon = ft.icons.PAUSE
        page.update()

    def update_song_info():
        song = playlist.Playlist[current_song_index]
        song_info.value = f"{song.title}"
        duration.value = format_time(song.duration)
        progress_bar.value = 0.0
        current_time_text.value = "00:00"
        page.update()
    
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds),60)
        return f"{minutes:02d}:{seconds:02d}"
    
    async def update_progress():
        nonlocal pg
        while True:
            if pg.get_init() is not None:
                if pg.music.get_busy():
                    current_time = pygame.mixer.music.get_pos() /1000
                    progress_bar.value = current_time / playlist.Playlist[current_song_index].duration
                    current_time_text.value = format_time(current_time)
                    page.update()
                await asyncio.sleep(1)
            await asyncio.sleep(1)

    # async def update_progress():
    #     global is_playing
    #     while is_playing:
    #         if pygame.mixer.music.get_busy():
    #             current_time = pygame.mixer.music.get_pos() / 1000
    #             progress_bar.value = current_time / playlist.Playlist[current_song_index].duration
    #             current_time_text.value = format_time(current_time)
    #             page.update()
    #         await asyncio.sleep(1)

    # async def start_progress_update():
    #     global is_playing, progress_task
    #     if not is_playing:  
    #         is_playing = True
    #         progress_task = asyncio.create_task(update_progress())  

    # async def stop_progress_update():
    #     global is_playing, progress_task
    #     if is_playing:  
    #         is_playing = False
    #         if progress_task:
    #             progress_task.cancel()  
    #             try:
    #                 await progress_task
    #             except asyncio.CancelledError:
    #                 pass  
    #         progress_task = None 
    
    # def Detener_Asyncio():
    #     try:
    #         loop = asyncio.get_running_loop()
    #         loop.close()
    #     except:
    #         pass

    def ver_cancion(e):
        print(f"Se ha hecho clic en la canción: {e.control.data}")

    def Buscar_Canciones(e):
        global NuevaBusqueda
        NuevaBusqueda = Bsq.Busqueda(e.control.value)
        Resultado_Busqueda = ft.Column()

        for index, row in NuevaBusqueda.Dataframe.iterrows():
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
                                on_tap=Cargar_Cancion,
                                data=row["title"]
                            ),
                                ft.Text(
                                    row["title"], 
                                    size=16, 
                                    weight="bold",
                                    text_align= ft.TextAlign.CENTER,
                                    ),
                ], 
                alignment=ft.CrossAxisAlignment.CENTER, 
                horizontal_alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
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
            scroll=ft.ScrollMode.AUTO 
        )
        page.update()

    def Cargar_Cancion(e):

        try:
            global NuevaBusqueda
            nonlocal pg
            listado = NuevaBusqueda.DevolverListado()
            key = [key for key, value in listado.items() if value == e.control.data]
            global Cancion
            Cancion = Yt.objYouTube(NuevaBusqueda.DevolverLink(key))
            global watcher
            watcher = Watcher.DirectoryWatcher()
            watcher.start()
            Cancion.Bajar_Audio(nombre=Cancion.Titulo)
            load_newsong(nombre=Cancion.Titulo)
            
        except Exception as ex:
            error = traceback.format_exc()
            print(error)

    
    def Actualizar():
        load_song()
        update_song_info()
        page.update()
        

    current_song_index = 0
    song_info = ft.Text(size=20, color=ft.colors.WHITE)
    current_time_text = ft.Text(value="00:00", color=ft.colors.WHITE60)
    duration = ft.Text(color=ft.colors.WHITE60)
    progress_bar = ft.ProgressBar(value=0.0, width=300, height=10, color="white", bgcolor="#263238")
    play_button = ft.IconButton(icon=ft.icons.PLAY_ARROW, on_click=play_Pause, icon_color=ft.colors.WHITE)
    next_button = ft.IconButton(icon=ft.icons.SKIP_NEXT, on_click= change_song,data=1, icon_color=ft.colors.WHITE)
    prev_button = ft.IconButton(icon=ft.icons.SKIP_PREVIOUS, on_click=change_song, data=-1,icon_color=ft.colors.WHITE)
    stop_button = ft.IconButton(icon=ft.icons.STOP_CIRCLE, on_click=stop, icon_color=ft.colors.WHITE)
    Busqueda = ft.TextField(label="Con qué te vas a deleitar?", hint_text="Escriba un artista o canción.", icon=ft.icons.SEARCH,on_submit=Buscar_Canciones)

    
    listado_canciones = ft.Container(
        alignment=ft.alignment.center,
        width=400, 
        height=500, 
        adaptive= False,
    )
    fila_busqueda = ft.Row(controls=[Busqueda], alignment=ft.MainAxisAlignment.CENTER)
    fila_titulo = ft.Row(controls=[song_info], alignment=ft.MainAxisAlignment.CENTER)
    fila_controles = ft.Row(controls=[prev_button,play_button,stop_button, next_button], 
                      alignment=ft.MainAxisAlignment.CENTER,
                      )
    fila_reproductor = ft.Row(controls=[current_time_text, progress_bar, duration],
                              alignment=ft.MainAxisAlignment.CENTER,
                              vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
    columna_busqueda = ft.Column(controls=[fila_busqueda],alignment=ft.MainAxisAlignment.CENTER)
    columna = ft.Column(controls=[fila_titulo, fila_reproductor, fila_controles],
                        alignment=ft.MainAxisAlignment.CENTER, spacing=20,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        )
    fila_listado = ft.Row(controls=[listado_canciones], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)


    page.add(columna_busqueda, fila_listado,  
             ft.Row([columna],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    expand=False
                    )
    )
    if playlist.Playlist:
        Actualizar()
        await update_progress()
    else:
        song_info =  "No se encontraron canciones en la carpeta de canciones"
        page.update()

ft.app(target=main)

