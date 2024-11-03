from youtubesearchpython import VideosSearch
import streamlit as st
import pandas as pd
import ObjBusqueda as busqueda
import objYouTube as yt



cancion = st.text_input("Busque una canción")
if cancion:
    NuevaBusqueda = busqueda.Busqueda(cancion)
    videos = NuevaBusqueda.DevolverListado()
    
    st.dataframe(NuevaBusqueda.Dataframe)
    st.dataframe(NuevaBusqueda.Minitaturas)
    st.image(NuevaBusqueda.Minitaturas["thumbnails"][0])

    print(NuevaBusqueda.Dataframe.head())
    opcion = st.selectbox("elija",videos.values())

    st.text(opcion)

    if opcion:
        key = [key for key, value in videos.items() if value == opcion]

        NuevoLink = yt.objYouTube(NuevaBusqueda.DevolverLink(key))
        NuevoLink.Stream = NuevoLink.Audio_Streams()
        st.text(NuevoLink.Duración)

    #eleccion = st.selectbox("Elije", NuevoLink.Stream)

        if st.button("Elegir"):
            NuevoLink.Bajar_Audio()
            st.audio(NuevoLink.Audio)





