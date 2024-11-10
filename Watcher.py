import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import time

class MP3Handler(FileSystemEventHandler):
    def __init__(self):
        self.Nuevo_Archivo = False
        self.Nombre = None
    
    def on_created(self, event):
        if event.is_directory is False and event.src_path.endswith(".mp3") and not event.src_path.endswith("data.mp3"):
            self.Nombre = event.src_path
            if self.wait_for_download_complete():
                self.Nuevo_Archivo = True
    
    def wait_for_download_complete(self):
        last_size = -1
        attemps = 0

        while attemps < 20:
            current_size = os.path.getsize(self.Nombre)
            if current_size == last_size:
                return True
            last_size = current_size
            attemps +=1
            time.sleep(0.5)

    
    def Reset(self):
        self.Nuevo_Archivo = False
    

class DirectoryWatcher:
    def __init__(self, path="Cache"):
        self.path = path
        self.handler = MP3Handler()
        self.observer = Observer()  

    def start(self):
        self.observer.schedule(self.handler, self.path, recursive=False)
        self.observer.start()
    
    def stop(self):
        self.observer.stop()
        self.observer.join()

    def check_for_new_file(self):
        if self.handler.Nuevo_Archivo:
            self.handler.Reset()
            return True
        return False