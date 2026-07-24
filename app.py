import streamlit as st
from google import genai
import zipfile
import io

st.title("Generador de Imágenes para Guiones")

api_key = st.text_input("Tu clave de API de Gemini", type="password")
estilo_global = st.text_area(
    "Estilo visual global",
    value="""Ilustración minimalista tipo "stick figure", trazo negro limpio y grueso,
fondo blanco puro, sin texto, formato horizontal 16:9."""
)
guion_texto = st.text_area("Pega aquí una frase/escena por línea", height=300)

if st.button("Generar todas las imágenes"):
    escenas = [linea.strip() for linea in guion_texto.split("\n") if linea.strip()]
    client = genai.Client(api_key=api_key)
    imagenes = []
    barra = st.progress(0)

    for i, escena in enumerate(escenas, start=1):
        prompt = f"{estilo_global}\n\nEscena: {escena}"
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                imagenes.append((f"imagen_{i:02d}.png", part.inline_data.data))
                st.image(part.inline_data.data, caption=f"Escena {i}: {escena[:40]}...")
        barra.progress(i / len(escenas))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for nombre, datos in imagenes:
            zf.writestr(nombre, datos)
    st.download_button("Descargar todas (ZIP)", zip_buffer.getvalue(), "imagenes.zip")