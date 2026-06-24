import streamlit as st
import google.generativeai as genai

# Configurazione della pagina Streamlit
st.set_page_config(page_title="AI Website Builder 🚀", layout="wide")

st.title("🧙‍♂️ AI Website Builder")
st.write("Scrivi cosa desideri e l'intelligenza artificiale creerà il tuo sito web in pochi secondi!")

# Input dell'utente
prompt_utente = st.text_area(
    "Descrivi il tuo sito web nei minimi dettagli:",
    placeholder="Es: Un sito moderno per un personal trainer con una sezione 'Chi sono', i servizi e un form di contatto color nero e oro."
)

# Inserimento della chiave API (In produzione si usa Streamlit Secrets)
api_key = st.text_input("Inserisci la tua Gemini API Key:", type="password")

if st.button("Genera Sito Web ✨"):
    if not prompt_utente:
        st.error("Per favore, descrivi prima il sito che vuoi creare!")
    elif not api_key:
        st.error("Inserisci la tua Gemini API Key per continuare!")
    else:
        with st.spinner("L'oracolo dell'IA sta scrivendo il codice... 🤖"):
            try:
                # Configura Gemini
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Prompt di sistema per forzare Gemini a dare SOLO codice HTML/CSS funzionante
                prompt_di_sistema = f"""
                Sei un esperto web designer. Genera un singolo file HTML completo, moderno, responsive (adatto anche a mobile) e con uno stile CSS integrato (usa Tailwind CSS via CDN se necessario per farlo bellissimo). 
                Non scrivere spiegazioni, non mettere i blocchi di codice ```html. Restituisci SOLO il codice HTML puro dall'inizio alla fine.
                Richiesta dell'utente: {prompt_utente}
                """
                
                # Generazione
                response = model.generate_content(prompt_di_sistema)
                codice_html = response.text
                
                # Mostra l'anteprima del sito in un box (Iframe)
                st.subheader("👀 Anteprima del tuo sito:")
                st.components.v1.html(codice_html, height=500, scrolling=True)
                
                # Pulsante per scaricare il file index.html
                st.success("Sito generato con successo!")
                st.download_button(
                    label="📥 Scarica il codice HTML",
                    data=codice_html,
                    file_name="index.html",
                    mime="text/html"
                )
                
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")
