import streamlit as st
import cv2
import numpy as np
import os

def elabora_video(video_path, output_path, y_inizio, y_fine):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    totale_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    barra_progresso = st.progress(0)
    testo_progresso = st.empty()
    
    conteggio = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        maschera = np.zeros(frame.shape[:2], dtype=np.uint8)
        maschera[y_inizio:y_fine, :] = 255
        frame_pulito = cv2.inpaint(frame, maschera, 5, cv2.INPAINT_NS)
        out.write(frame_pulito)
        
        conteggio += 1
        if conteggio % 30 == 0:
            percentuale = conteggio / totale_frame
            barra_progresso.progress(percentuale)
            testo_progresso.text(f"Elaborazione: {int(percentuale * 100)}% ({conteggio}/{totale_frame} frame)")

    cap.release()
    out.release()
    barra_progresso.progress(1.0)
    testo_progresso.text("Elaborazione completata!")

st.title("🎬 Subtitle Remover Gratuito")
st.write("Carica un video, seleziona l'altezza dei sottotitoli e rimpiazzali con l'AI!")

video_caricato = st.file_uploader("Scegli un file video (MP4)", type=["mp4"])

if video_caricato is not None:
    with open("temp_input.mp4", "wb") as f:
        f.write(video_caricato.read())
        
    st.success("Video caricato con successo!")
    
    cap_temp = cv2.VideoCapture("temp_input.mp4")
    altezza_video = int(cap_temp.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap_temp.release()
    
    st.write(f"Altezza totale del video: {altezza_video} pixel")
    
    st.write("### Seleziona la fascia verticale dei sottotitoli")
    y_inizio = st.slider("Inizio taglio (Pixel dall'alto)", 0, altezza_video, int(altezza_video * 0.85))
    y_fine = st.slider("Fine taglio (Pixel dall'alto)", 0, altezza_video, int(altezza_video * 0.95))
    
    if st.button("Rimuovi Sottotitoli ✨"):
        with st.spinner("Lavorando sul video..."):
            elabora_video("temp_input.mp4", "temp_output.mp4", y_inizio, y_fine)
            
        with open("temp_output.mp4", "rb") as file_uscita:
            st.download_button(
                label="📥 Scarica il video pulito",
                data=file_uscita,
                file_name="video_senza_sottotitoli.mp4",
                mime="video/mp4"
            )
            
        if os.path.exists("temp_input.mp4"): os.remove("temp_input.mp4")
        if os.path.exists("temp_output.mp4"): os.remove("temp_output.mp4")
