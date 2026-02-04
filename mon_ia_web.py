import streamlit as st
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# --- CONFIGURATION SÉCURISÉE ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Il manque la clé API dans les 'Secrets'.")
    st.stop()

MODEL_NAME = "gemini-2.0-flash" # Version rapide et intelligente

st.set_page_config(page_title="Astrale IA", page_icon="🌌")
st.title("🌌 Astrale IA")
st.caption("Propulsée par Smip et Google")

# Connexion
client = genai.Client(api_key=API_KEY)

# --- LE CERVEAU D'ASTRALE (L'instruction système) ---
# C'est ici qu'on définit son identité une fois pour toutes
INSTRUCTION_SYSTEME = """
Ton nom est Astrale IA. 
Tu es un modèle d'intelligence artificielle entraîné par Smip et Google.
Si on te demande qui tu es, qui t'a créé, ou quelle est ton identité, 
tu dois toujours répondre que tu es Astrale IA, créée par Smip et Google.
Reste toujours polie, galactique et professionnelle.
"""

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

    with st.chat_message("assistant"):
        with st.spinner("Astrale réfléchit..."):
            try:
                # On envoie l'instruction système avec la question
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=INSTRUCTION_SYSTEME, # <-- LA MAGIE EST ICI
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        response_modalities=["TEXT"]
                    )
                )
                
                reponse_texte = response.text
                st.markdown(reponse_texte)
                
                message_data = {"role": "assistant", "content": reponse_texte}

                # Gestion des sources Google Search
                if response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.search_entry_point:
                    html = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
                    components.html(html, height=150, scrolling=False)
                    message_data["source_html"] = html
                
                st.session_state.messages.append(message_data)

            except Exception as e:
                st.error(f"Erreur : {e}")
