import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Astrale",
    page_icon="🌌",
    layout="wide", # On reste en wide pour gérer les marges nous-mêmes
    initial_sidebar_state="collapsed"
)

# --- 2. LE DESIGN (CSS AJUSTÉ PLUS ÉTROIT) ---
st.markdown("""
<style>
    /* --- IMPORTATION DE POLICE --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    /* --- FOND D'ÉCRAN ANIMÉ --- */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- NETTOYAGE --- */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}

    /* --- CENTRAGE ET RÉTRÉCISSEMENT (C'est ici que ça change !) --- */
    .main .block-container {
        max-width: 600px; /* <--- On est passé de 800px à 600px ici */
        padding-top: 2rem;
        padding-bottom: 5rem;
        margin: 0 auto; /* Centre le tout */
    }

    /* --- ZONE DE SAISIE (INPUT) CENTRÉE --- */
    /* On force la barre de saisie à avoir la même largeur que le chat */
    .stChatInput {
        max-width: 600px !important;
        margin: 0 auto !important;
        left: 0;
        right: 0;
    }

    /* --- STYLES DES BULLES --- */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .stChatMessage .stchat-avatar {
        background: transparent !important;
        font-size: 28px;
    }

    .stChatMessage markdown {
        color: #FFFFFF !important;
    }

    /* --- DESIGN DE L'INPUT --- */
    .stChatInputContainer {
        padding-bottom: 20px;
        background: transparent !important;
    }
    
    .stChatInput input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 25px !important;
    }
    
    ::placeholder { 
      color: rgba(255,255,255,0.5) !important;
      opacity: 1; 
    }

    /* --- TITRES --- */
    h1 {
        font-weight: 600 !important;
        letter-spacing: -1px;
        background: -webkit-linear-gradient(eee, #333);
        -webkit-background-clip: text;
        text-shadow: 0 0 20px rgba(100, 180, 255, 0.3);
    }

</style>
""", unsafe_allow_html=True)

# --- 3. CONNEXION GOOGLE ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
except:
    st.error("🔑 Erreur API.")
    st.stop()

# --- 4. INTERFACE ---

# Titre centré
st.markdown("<h1 style='text-align: center;'>🌌 Astrale</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7; font-size: 0.9rem;'>Ton IA personnelle.</p>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Je suis prête."}
    ]

for message in st.session_state.messages:
    avatar_icon = "🧑‍🚀" if message["role"] == "user" else "🛸"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# --- 5. LOGIQUE ---
if prompt := st.chat_input("Écris ton message..."):
    
    with st.chat_message("user", avatar="🧑‍🚀"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt_systeme = f"""
    Tu es Astrale. Sois concise, moderne et utile.
    Si tu donnes du code, formate-le proprement.
    Message : {prompt}
    """

    with st.chat_message("assistant", avatar="🛸"):
        placeholder = st.empty()
        placeholder.markdown("*...*") # Indicateur minimaliste
        
        try:
            response = model.generate_content(prompt_systeme)
            time.sleep(0.2)
            placeholder.empty()
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            placeholder.empty()
            if "429" in str(e):
                st.warning("⚡ Trop de demandes. Attends un peu.")
            else:
                st.error("Erreur de connexion.")

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
