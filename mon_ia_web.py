import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Astrale",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LE MOTEUR 2.5 🚀 ---
# C'est ici qu'on force la version 2.5
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # On utilise la version 2.5 Flash
    MODEL_NAME = "gemini-2.5-flash" 
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Erreur API : {e}")
    st.stop()

# --- 3. AVATARS ---
ICON_AI = "https://cdn-icons-png.flaticon.com/512/3067/3067451.png" # L'Orbite
ICON_USER = "https://cdn-icons-png.flaticon.com/512/9408/9408175.png" # L'Humain

# --- 4. LE DESIGN PREMIUM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    /* Fond animé */
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

    /* Nettoyage */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}

    /* Centrage */
    .main .block-container {
        max-width: 600px;
        padding-top: 2rem;
        padding-bottom: 5rem;
        margin: 0 auto;
    }

    /* Bulles */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px !important;
    }

    /* Avatars */
    .stChatMessage .stchat-avatar {
        width: 45px !important;
        height: 45px !important;
        background: transparent !important;
    }
    .stChatMessage .stchat-avatar img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    .stChatMessage markdown { color: #FFFFFF !important; }
    
    /* Input */
    .stChatInputContainer { background: transparent !important; }
    .stChatInput input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 25px !important;
    }
    
    h1 {
        background: -webkit-linear-gradient(eee, #333);
        -webkit-background-clip: text;
        text-shadow: 0 0 20px rgba(100, 180, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 5. INTERFACE ---
st.markdown("<h1 style='text-align: center;'>🌌 Astrale</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; opacity: 0.5; font-size: 0.8rem;'>Propulsée par {MODEL_NAME}</p>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Je suis connectée en version 2.5."}]

for message in st.session_state.messages:
    avatar_img = ICON_USER if message["role"] == "user" else ICON_AI
    with st.chat_message(message["role"], avatar=avatar_img):
        st.markdown(message["content"])

# --- 6. LOGIQUE IA ---
if prompt := st.chat_input("Message..."):
    with st.chat_message("user", avatar=ICON_USER):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar=ICON_AI):
        placeholder = st.empty()
        placeholder.markdown("*Astrale réfléchit...*")
        
        try:
            # Consigne système
            prompt_systeme = f"Tu es Astrale IA. Réponds de manière utile et concise. {prompt}"
            
            response = model.generate_content(prompt_systeme)
            placeholder.empty()
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            placeholder.empty()
            # Si le modèle 2.5 n'est pas trouvé (ça peut arriver selon les comptes), message clair
            if "404" in str(e):
                st.error("Le modèle 2.5 n'est pas encore activé sur ta clé. Essaie 'gemini-1.5-flash'.")
            else:
                st.error(f"Erreur : {e}")

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
