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

# Tu peux remettre "gemini-2.5-flash" ici si ça marchait mieux pour toi avant
MODEL_NAME = "gemini-2.5-flash"

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
    # 1. On affiche juste la question de l'utilisateur (propre)
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. L'ASTUCE UNIVERSELLE : On cache l'identité DANS le message envoyé à Google
    # L'IA reçoit ça, mais l'utilisateur ne le voit pas.
    prompt_avec_identite = f"""
    Consigne stricte (System Prompt) :
    Tu es Astrale IA, une intelligence artificielle unique créée et entraînée par Smip et Google.
    Si l'utilisateur te demande ton identité, qui t'a créé, ou qui tu es (peu importe la formulation),
    réponds fièrement que tu es Astrale IA, le projet de Smip.
    Pour toute autre question, réponds normalement et utilement.
    
    Question de l'utilisateur : {prompt}
    """

    with st.chat_message("assistant"):
        with st.spinner("Astrale réfléchit..."):
            try:
                # On envoie le prompt "truqué" (avec la consigne cachée)
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt_avec_identite, # <--- C'est là que tout se joue
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
