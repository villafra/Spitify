from yt_dlp import YoutubeDL

ydl_opts = {'format': 'bestaudio'}

class Song:

    def  __init__(self, url):
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        self.Name = info['title']
        self.Url = info["url"]
        self.duration = info['duration']
        self.view_count = info['view_count']
        self.like_count = info['like_count']
    