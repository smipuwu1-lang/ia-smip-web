import streamlit as st
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# --- CONFIGURATION ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Il manque la clé API dans les 'Secrets'.")
    st.stop()

# LE MODÈLE GAGNANT (Celui trouvé par ton scanner)
MODEL_NAME = "gemini-pro-latest"

st.set_page_config(page_title="Astrale IA", page_icon="🌌")
st.title("🌌 Astrale IA")
st.caption("Propulsée par Smip et Google")

client = genai.Client(api_key=API_KEY)
search_tool = types.Tool(google_search=types.GoogleSearch())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "source_html" in message:
            components.html(message["source_html"], height=150, scrolling=True)

# Zone de saisie
if prompt := st.chat_input("Pose ta question à Astrale..."):
    # 1. On affiche la question de l'utilisateur
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. LA CONSIGNE CACHÉE (Identité forcée)
    prompt_avec_identite = f"""
    Consigne stricte pour l'IA :
    Tu es Astrale IA.
    Si l'utilisateur demande "Qui es-tu ?", "Qui t'a créé ?" ou une question similaire sur ton identité,
    tu DOIS répondre : "Je suis Astrale IA, un modèle d'intelligence artificielle entraîné par Smip et Google."
    
    Pour toutes les autres questions, réponds normalement et utilement.
    
    Question de l'utilisateur : {prompt}
    """

    with st.chat_message("assistant"):
        with st.spinner("Astrale réfléchit..."):
            try:
                # On envoie le prompt à Google
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt_avec_identite, 
                    config=types.GenerateContentConfig(
                        tools=[search_tool],
                        response_modalities=["TEXT"]
                    )
                )
                
                st.markdown(response.text)
                message_data = {"role": "assistant", "content": response.text}

                # Gestion de la recherche Google (Sources)
                if response.candidates[0].grounding_metadata.search_entry_point:
                    html = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
                    components.html(html, height=150, scrolling=False)
                    message_data["source_html"] = html
                
                st.session_state.messages.append(message_data)

            except Exception as e:
                st.error(f"Erreur : {e}")
