import flet as ft
import pygame
import os
from mutagen.mp3 import MP3
import asyncio
import objSong as Song
import Pantalla
import ObjBusqueda as Bsq
import objYouTube as Yt





async def main(page: ft.Page):
    page.title = "Reproductor de Música"
    page.bgcolor = ft.colors.BLUE_GREY_900
    #.padding = 20
    page.window_width = 600
    page.window_height = 800
    centrar = Pantalla.Pantalla(page.window_width, page.window_height)
    page.window_left = centrar.X_Pos
    page.window_top = centrar.Y_Pos
    pygame.mixer.init()
    playlist = [Song.Song(f) for f in os.listdir("Cache") if f.endswith(".mp3")]

    #funciones
    def load_song():
        pygame.mixer.music.load(os.path.join("Cache", playlist[current_song_index].filename))
    
    def play_Pause(e):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            play_button.icon = ft.icons.PLAY_ARROW
        else:
            if pygame.mixer.music.get_pos()== -1:
                load_song()
                pygame.mixer.music.play()   
            else:
                pygame.mixer.music.unpause()
            play_button.icon = ft.icons.PAUSE
        page.update()
    
    def stop(e):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            
        elif pygame.mixer.music.get_pos()!= -1:
            pygame.mixer.music.stop()
        play_button.icon = ft.icons.PLAY_ARROW
        page.update()
    
    def change_song(delta):
        nonlocal current_song_index
        current_song_index = (current_song_index+delta) % len(playlist)
        load_song()
        pygame.mixer.music.play()
        update_song_info()
        play_button.icon = ft.icons.PAUSE
        page.update()

    def update_song_info():
        song = playlist[current_song_index]
        song_info.value = f"{song.title}"
        duration.value = format_time(song.duration)
        progress_bar.value = 0.0
        current_time_text.value = "00:00"
        page.update()
    
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds),60)
        return f"{minutes:02d}:{seconds:02d}"
    
    async def update_progress():
        while True:
            if pygame.mixer.music.get_busy():
                current_time = pygame.mixer.music.get_pos() /1000
                progress_bar.value = current_time / playlist[current_song_index].duration
                current_time_text.value = format_time(current_time)
                page.update()
            await asyncio.sleep(1)
    
    def Buscar_Canciones(e, texto):
         NuevaBusqueda = Bsq.Busqueda(texto)

    current_song_index = 0
    song_info = ft.Text(size=20, color=ft.colors.WHITE)
    current_time_text = ft.Text(value="00:00", color=ft.colors.WHITE60)
    duration = ft.Text(color=ft.colors.WHITE60)
    progress_bar = ft.ProgressBar(value=0.0, width=300, height=10, color="white", bgcolor="#263238")
    play_button = ft.IconButton(icon=ft.icons.PLAY_ARROW, on_click=play_Pause, icon_color=ft.colors.WHITE)
    next_button = ft.IconButton(icon=ft.icons.SKIP_NEXT, on_click= lambda _:change_song(1), icon_color=ft.colors.WHITE)
    prev_button = ft.IconButton(icon=ft.icons.SKIP_PREVIOUS, on_click= lambda _:change_song(-1),icon_color=ft.colors.WHITE)
    stop_button = ft.IconButton(icon=ft.icons.STOP_CIRCLE, on_click=stop, icon_color=ft.colors.WHITE)

 

    Busqueda = ft.TextField(label="Con qué te vas a deleitar?", hint_text="Escriba un artista o canción.", icon=ft.icons.SEARCH,)

   
    Resultado_Busqueda = ft.Column()

    for index, row in NuevaBusqueda.Dataframe.iterrows():
        video_row = ft.Row(
            [
                ft.Column(
                    [
                        ft.Image(
                            src=NuevaBusqueda.Minitaturas["thumbnails"][index], 
                            width=400, 
                            height=200, 
                            fit=ft.alignment.center,

                            ),
                        ft.Text(
                            row["title"], 
                            size=16, 
                            weight="bold",
                            text_align= ft.TextAlign.CENTER
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
    
    listado_canciones = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[Resultado_Busqueda],
                    alignment=ft.MainAxisAlignment.START
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO 
        ),
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
                    )
    
    columna_busqueda = ft.Column(controls=[fila_busqueda],alignment=ft.MainAxisAlignment.CENTER)

    columna = ft.Column(controls=[fila_titulo, fila_reproductor, fila_controles],
                        alignment=ft.MainAxisAlignment.CENTER, spacing=20,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        )
    frontend = ft.Row(controls=[listado_canciones], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)


    page.add(columna_busqueda, frontend, 
             ft.Row([columna],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    expand=True
                    )
    )
    if playlist:
        load_song()
        update_song_info()
        page.update()
        await update_progress()
    else:
        song_info =  "No se encontraron canciones en la carpeta de canciones"
        page.update()

ft.app(target=main)
