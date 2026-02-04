import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Astrale",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CHOISIS TON LOGO ICI ! ---

# OPTION A : CONCEPT 2 (L'Orbite / L'Atome) ⚛️
# C'est celle qui est active maintenant. Un look très "Science" et "Futur".
ICON_AI = "https://cdn-icons-png.flaticon.com/512/3067/3067451.png"

# OPTION B : CONCEPT 3 (Le Prisme / Le Cristal) 💎
# Si tu préfères celle-ci, enlève le '#' devant la ligne ci-dessous et mets un '#' devant la ligne du dessus.
# ICON_AI = "https://cdn-icons-png.flaticon.com/512/2103/2103633.png"


# L'AVATAR UTILISATEUR (On garde le sympa coloré)
ICON_USER = "https://cdn-icons-png.flaticon.com/512/9408/9408175.png"


# --- 3. LE DESIGN (CSS SOIGNÉ) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    /* Fond d'écran animé sombre */
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

    /* Bulles de chat */
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

    /* Texte */
    .stChatMessage markdown {
        color: #FFFFFF !important;
    }

    /* Input */
    .stChatInputContainer {
        padding-bottom: 20px;
        background: transparent !important;
    }
    
    .stChatInput {
        max-width: 600px !important;
        margin: 0 auto !important;
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

    /* Titre */
    h1 {
        font-weight: 600 !important;
        letter-spacing: -1px;
        background: -webkit-linear-gradient(eee, #333);
        -webkit-background-clip: text;
        text-shadow: 0 0 20px rgba(100, 180, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. CONNEXION ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
except:
    st.error("🔑 Erreur API.")
    st.stop()

# --- 5. INTERFACE ---
st.markdown("<h1 style='text-align: center;'>🌌 Astrale</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7; font-size: 0.9rem;'>Ton IA personnelle.</p>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Je suis prête."}
    ]

# Affichage de l'historique
for message in st.session_state.messages:
    avatar_img = ICON_USER if message["role"] == "user" else ICON_AI
    with st.chat_message(message["role"], avatar=avatar_img):
        st.markdown(message["content"])

# --- 6. LOGIQUE IA ---
if prompt := st.chat_input("Écris ton message..."):
    
    # Affichage User
    with st.chat_message("user", avatar=ICON_USER):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt_systeme = f"""
    Tu es Astrale. Sois concise, moderne et utile.
    Message : {prompt}
    """

    # Affichage IA
    with st.chat_message("assistant", avatar=ICON_AI):
        placeholder = st.empty()
        placeholder.markdown("*...*")
        
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
