import streamlit as st
import yt_dlp
import os
import tempfile

# Configuración de la página
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

st.title("🎬 Descargador de YouTube")
st.write("Ingresa la URL del video para descargarlo en formato MP4 (Video) o MP3 (Audio).")

# Campo para introducir la URL
url = st.text_input("URL del video de YouTube:", placeholder="https://www.youtube.com/watch?v=...")

# Opción de formato
formato = st.radio("Selecciona el formato de descarga:", ["Video (MP4)", "Audio (MP3)"])

if st.button("Procesar y Descargar"):
    if not url:
        st.error("Por favor, ingresa una URL válida.")
    else:
        with st.spinner("Procesando el enlace..."):
            try:
                # Usamos un directorio temporal para almacenar el archivo antes de ofrecer la descarga
                with tempfile.TemporaryDirectory() as temp_dir:
                    
                    if formato == "Video (MP4)":
                        ydl_opts = {
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                        }
                    else: # Audio (MP3)
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                        }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        
                        # Si es MP3, ajustamos la extensión del archivo a buscar
                        if formato == "Audio (MP3)":
                            filename = os.path.splitext(filename)[0] + ".mp3"

                    # Mostrar información básica del video
                    st.success("¡Video procesado con éxito!")
                    st.write(f"**Título:** {info.get('title')}")
                    
                    # Leer el archivo descargado para el botón de Streamlit
                    with open(filename, "rb") as file:
                        btn = st.download_button(
                            label="⬇️ Descargar archivo",
                            data=file,
                            file_name=os.path.basename(filename),
                            mime="video/mp4" if formato == "Video (MP4)" else "audio/mpeg"
                        )

            except Exception as e:
                st.error(f"Ocurrió un error al procesar el video: {e}")
