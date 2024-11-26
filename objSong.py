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
        thumbnails = info.get('thumbnails', [])
        if thumbnails:
            def get_area(thumbnail):
                resolution = thumbnail.get('resolution', '0x0')
                try:
                    width, height = map(int, resolution.split('x'))
                    return width * height
                except ValueError:
                    return 0
            self.thumbnail = max(thumbnails, key=get_area)['url']
        else:
            self.thumbnail = None


class EventMock:
    def __init__(self, control):
        self.control = control

class MockControl:
    def __init__(self, data):
        self.data = data
    