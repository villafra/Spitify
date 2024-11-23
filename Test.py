import flet as ft
from yt_dlp import YoutubeDL
import vlc

def main(page: ft.Page):
    page.title = "YouTube Audio Streamer"
    page.theme_mode = ft.ThemeMode.DARK

    # Objeto global del reproductor VLC
    player = None

    def play_audio(e):
        nonlocal player
        url = url_field.value
        if not url:
            status.value = "⚠️ Ingresa un enlace de YouTube."
            page.update()
            return

        # Extrae la URL de audio con yt-dlp
        status.value = "🎵 Obteniendo URL del audio..."
        page.update()

        ydl_opts = {'format': 'bestaudio'}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']
        except Exception as ex:
            status.value = f"⚠️ Error al procesar el video: {ex}"
            page.update()
            return

        # Reproduce el audio con VLC
        status.value = "🎶 Reproduciendo..."
        page.update()
        player = vlc.MediaPlayer(audio_url)
        player.play()

    def stop_audio(e):
        nonlocal player
        if player:
            player.stop()
            status.value = "⏹️ Reproducción detenida."
            page.update()

    # Elementos de la interfaz
    url_field = ft.TextField(label="Enlace de YouTube", width=400)
    play_button = ft.ElevatedButton("Reproducir", on_click=play_audio)
    stop_button = ft.ElevatedButton("Detener", on_click=stop_audio)
    status = ft.Text(value="", size=14, color="white")

    # Diseño de la interfaz
    page.add(
        ft.Column(
            [
                ft.Text("YouTube Audio Streamer", size=20, weight="bold"),
                url_field,
                ft.Row([play_button, stop_button], spacing=10),
                status,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# Ejecuta la aplicación
ft.app(target=main)
