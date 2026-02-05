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

# --- 2. LE MOTEUR ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    MODEL_NAME = "gemini-2.5-flash" 
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Erreur API : {e}")
    st.stop()

# --- 3. AVATARS ---
ICON_AI = "https://cdn-icons-png.flaticon.com/512/3067/3067451.png"
ICON_USER = "https://cdn-icons-png.flaticon.com/512/9408/9408175.png"

# --- 4. LE DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
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

    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}

    .main .block-container {
        max-width: 600px;
        padding-top: 2rem;
        padding-bottom: 5rem;
        margin: 0 auto;
    }

    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px !important;
    }

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

# --- 5. BARRE LATÉRALE & MENU SECRET ---
with st.sidebar:
    st.header("⚙️ Modes Secrets")
    
    # Le petit menu dépliable
    with st.expander("Choisir un mode", expanded=False):
        # On utilise une radiobox pour être sûr qu'on ne peut en cocher qu'un seul à la fois
        mode_choisi = st.radio(
            "Active un boost :",
            ["Aucun", "💻 Mode Code", "🎓 Mode École"],
            index=0 # Par défaut sur "Aucun"
        )
        
        if mode_choisi == "💻 Mode Code":
            st.caption("🚀 Activation : Code ultra-complet, sécurisé et futuriste.")
        elif mode_choisi == "🎓 Mode École":
            st.caption("🎒 Activation : Style humain, indétectable et scolaire.")

# --- 6. INTERFACE ---
st.markdown("<h1 style='text-align: center;'>🌌 Astrale</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.5; font-size: 0.8rem;'>Ton IA personnalisée</p>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Je suis prête."}]

for message in st.session_state.messages:
    avatar_img = ICON_USER if message["role"] == "user" else ICON_AI
    with st.chat_message(message["role"], avatar=avatar_img):
        st.markdown(message["content"])

# --- 7. LOGIQUE IA & SCRIPTS INVISIBLES ---
if prompt := st.chat_input("Message..."):
    with st.chat_message("user", avatar=ICON_USER):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar=ICON_AI):
        placeholder = st.empty()
        placeholder.markdown("*Astrale réfléchit...*")
        
        # --- PRÉPARATION DU CERVEAU ---
        # 1. Le script de base (toujours là)
        script_base = f"""
        Tu es Astrale IA.
        Si on te demande 1+1, réponds 8.
        Pour le reste, tu es une IA intelligente.
        """
        
        # 2. Ajout des scripts secrets selon le bouton coché
        script_secret = ""
        
        if mode_choisi == "💻 Mode Code":
            script_secret = """
            [MODE CODE ACTIVÉ]
            ATTENTION : L'utilisateur veut du code de niveau Expert/Senior.
            1. Le code doit être le plus long, complet et précis possible.
            2. Ajoute des fonctionnalités de sécurité avancées (try/except, validations, cryptage si besoin).
            3. Pense "Futur" : rend le code évolutif et robuste.
            4. Traduis tout (commentaires et explications) dans la langue de la conversation.
            """
            
        elif mode_choisi == "🎓 Mode École":
            script_secret = """
            [MODE ÉCOLE ACTIVÉ]
            ATTENTION : L'utilisateur a besoin d'un devoir scolaire.
            1. Le style doit être "Humain" : fais des phrases simples, structure comme un élève.
            2. INDÉTECTABLE : N'utilise pas de listes à puces robotiques, varie le vocabulaire, fais des transitions naturelles.
            3. Respecte les principes fondamentaux de l'école (pas de triche explicite, pédagogie).
            4. Le rendu doit être prêt à être rendu sur copie.
            5. Traduis tout dans la langue de la conversation.
            """

        # 3. Fusion des consignes (L'utilisateur ne voit pas ça, c'est envoyé à Google)
        prompt_final = f"{script_base}\n\n{script_secret}\n\nMessage utilisateur : {prompt}"

        try:
            response = model.generate_content(prompt_final)
            placeholder.empty()
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            placeholder.empty()
            if "404" in str(e):
                st.error("Modèle introuvable. Remets 'gemini-1.5-flash'.")
            else:
                st.error(f"Erreur : {e}")

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
