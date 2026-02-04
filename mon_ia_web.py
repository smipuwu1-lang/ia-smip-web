import streamlit as st
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# --- CONFIGURATION SÉCURISÉE ---
# L'IA va chercher la clé dans le coffre-fort de Streamlit (Secrets)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Il manque la clé API dans les 'Secrets' du site.")
    st.stop()

MODEL_NAME = "gemini-2.5-flash"

# 1. LE COSTUME : On change le titre de la page et l'icône
st.set_page_config(page_title="Astrale IA", page_icon="🌌")
st.title("🌌 Astrale IA")
st.caption("Une intelligence connectée, propulsée par Smip et Google.")

# Connexion
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

search_tool = types.Tool(google_search=types.GoogleSearch())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "source_html" in message:
            components.html(message["source_html"], height=150, scrolling=True)

# Zone de saisie
if prompt := st.chat_input("Pose ta question à Astrale..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. LE CERVEAU : Détection d'identité mise à jour
    texte_minuscule = prompt.lower()
    questions_identite = ["qui t'a créé", "qui t'a crée", "c'est qui ton créateur", "qui es-tu", "tu viens d'où", "t'es qui"]
    
    est_question_identite = False
    for phrase in questions_identite:
        if phrase in texte_minuscule:
            est_question_identite = True
            break
            
    if est_question_identite:
        # La nouvelle réponse personnalisée
        reponse_astrale = "Je suis **Astrale IA**, un modèle d'intelligence artificielle entraîné par **Smip** et **Google**. 🌌"
        
        with st.chat_message("assistant"):
            st.markdown(reponse_astrale)
        st.session_state.messages.append({"role": "assistant", "content": reponse_astrale})

    else:
        # Pour le reste, on laisse Google répondre
        with st.chat_message("assistant"):
            with st.spinner("Astrale réfléchit..."):
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
                        html = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
                        components.html(html, height=150, scrolling=False)
                        message_data["source_html"] = html
                    
                    st.session_state.messages.append(message_data)
                except Exception as e:
                    st.error(f"Erreur : {e}")
