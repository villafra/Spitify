from youtubesearchpython import VideosSearch
import pandas as pd

class Busqueda:
    def __init__(self, prompt):
        self.Prompt = prompt
        self.Dataframe = self.BuscarEnYouTube()
        self.Minitaturas = pd.DataFrame(self.Dataframe["thumbnails"].apply(lambda x: x[-1]['url']))

    def BuscarEnYouTube(self):
        df = pd.DataFrame(VideosSearch(self.Prompt, limit=10).result()["result"])
        return df
    
    def DevolverListado(self):
        if not self.Dataframe.empty:
            return dict(zip(self.Dataframe["id"],self.Dataframe["title"]))
        else:
            return ["Sin coincidencias"]
    
    def DevolverLink(self, opcion):
        link = self.Dataframe[self.Dataframe['id'].isin(opcion)]["link"].to_string(index=False)
        if link:
            return link
        else:
            return None