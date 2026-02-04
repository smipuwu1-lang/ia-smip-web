import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Astrale IA", page_icon="🌌")
st.title("🌌 Astrale IA")
st.caption("Propulsée par Smip et Google (Version Stable)")

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Configuration de l'ancien moteur (plus robuste)
    genai.configure(api_key=API_KEY)
except:
    st.error("Il manque la clé API dans les 'Secrets'.")
    st.stop()

# On utilise le modèle Flash standard qui marche partout
MODEL_NAME = "gemini-1.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Pose ta question à Astrale..."):
    # 1. Affichage utilisateur
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Préparation du modèle
    model = genai.GenerativeModel(MODEL_NAME)
    
    # 3. La consigne d'identité (System Prompt intégré)
    prompt_avec_identite = f"""
    Tu es Astrale IA, une intelligence artificielle créée par Smip et Google.
    Si on te demande qui tu es, réponds toujours fièrement : "Je suis Astrale IA, créée par Smip."
    
    Question de l'utilisateur : {prompt}
    """

    # 4. Génération de la réponse
    with st.chat_message("assistant"):
        with st.spinner("Astrale réfléchit..."):
            try:
                # Appel simple et robuste
                response = model.generate_content(prompt_avec_identite)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                # Si erreur, on affiche un message gentil
                if "429" in str(e):
                    st.warning("Astrale a besoin d'une petite pause (Trop de questions). Réessaie dans 30 secondes !")
                else:
                    st.error(f"Erreur : {e}")
