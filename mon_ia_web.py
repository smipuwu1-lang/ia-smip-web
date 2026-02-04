import streamlit as st
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# --- CONFIGURATION ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Il manque la clé API.")
    st.stop()

# Avec ta NOUVELLE clé, ce modèle va marcher direct :
MODEL_NAME = "gemini-2.0-flash"

st.set_page_config(page_title="Astrale IA", page_icon="🌌")
st.title("🌌 Astrale IA")

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

search_tool = types.Tool(google_search=types.GoogleSearch())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "source_html" in message:
            components.html(message["source_html"], height=150, scrolling=True)

if prompt := st.chat_input("Pose ta question à Astrale..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Consigne d'identité
    prompt_identite = f"""
    Système : Tu es Astrale IA. Si on te demande qui tu es, réponds :
    "Je suis Astrale IA, un modèle d'IA entraîné par Smip et Google."
    Question : {prompt}
    """

    with st.chat_message("assistant"):
        with st.spinner("Initialisation du nouveau cerveau..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt_identite,
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
