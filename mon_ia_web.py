import streamlit as st
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# --- CONFIGURATION ---
API_KEY = st.secrets["GOOGLE_API_KEY"]# <--- REMETS TA CLÉ ICI !
MODEL_NAME = "gemini-2.5-flash"

st.set_page_config(page_title="IA de Smip", page_icon="🤖")
st.title("🤖 L'IA officielle de Smip")

# Connexion
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Erreur de clé API : {e}")
    st.stop()

search_tool = types.Tool(google_search=types.GoogleSearch())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affiche l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "source_html" in message:
            components.html(message["source_html"], height=150, scrolling=True)

# Zone de texte
if prompt := st.chat_input("Pose ta question ici..."):
    
    # 1. Affiche la question de l'utilisateur
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- LA PARTIE PERSONNALISÉE (SMIP) ---
    # On met tout en minuscule pour détecter "Qui" ou "qui" pareil
    texte_minuscule = prompt.lower()
    
    # Liste des questions déclencheurs
    questions_identite = ["qui t'a créé", "qui t'a crée", "c'est qui ton créateur", "qui es-tu", "qui es tu", "tu viens d'où"]

    # On vérifie si une de ces phrases est dans le message
    est_question_identite = False
    for phrase in questions_identite:
        if phrase in texte_minuscule:
            est_question_identite = True
            break
    
    # Si l'utilisateur demande qui a créé l'IA :
    if est_question_identite:
        reponse_smip = "Je suis une intelligence artificielle unique, créée et configurée par **Smip** ! 🚀"
        
        with st.chat_message("assistant"):
            st.markdown(reponse_smip)
        st.session_state.messages.append({"role": "assistant", "content": reponse_smip})

    # Sinon, on laisse Google répondre normalement :
    else:
        with st.chat_message("assistant"):
            with st.spinner("Analyse en cours..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            tools=[search_tool],
                            response_modalities=["TEXT"]
                        )
                    )
                    
                    st.markdown(response.text)
                    message_data = {"role": "assistant", "content": response.text}

                    if response.candidates[0].grounding_metadata.search_entry_point:
                        html_content = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
                        components.html(html_content, height=150, scrolling=False)
                        message_data["source_html"] = html_content
                    
                    st.session_state.messages.append(message_data)

                except Exception as e:
                    st.error(f"Erreur : {e}")

