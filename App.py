from youtubesearchpython import VideosSearch
import streamlit as st
import pandas as pd
import ObjBusqueda as busqueda
import objYouTube as yt



cancion = st.text_input("Busque una canción")
NuevaBusqueda = busqueda.Busqueda(cancion)
videos = NuevaBusqueda.DevolverListado()

opcion = st.selectbox("elija",videos.values())
key = [key for key, value in videos.items() if value == opcion]

NuevoLink = yt.objYouTube(NuevaBusqueda.DevolverLink(key))
NuevoLink.Stream = NuevoLink.Audio_Streams()

eleccion = st.select_slider("Elije", NuevoLink.Stream)

if st.button("Elegir"):
    NuevoLink.Audio = NuevoLink.Bajar_Audio()
    st.audio(NuevoLink.Audio)





