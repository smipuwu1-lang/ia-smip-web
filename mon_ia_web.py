import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURATION DE LA PAGE ---
# On le met en "wide" pour avoir la place de centrer nous-mêmes avec le CSS
st.set_page_config(
    page_title="Astrale",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LE "MAQUILLAGE" LOURD (CSS INJECTÉ) ---
# C'est ici que la magie opère. C'est du CSS avancé pour tordre Streamlit.
st.markdown("""
<style>
    /* --- IMPORTATION DE POLICE MODERNE --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    /* --- FOND D'ÉCRAN ANIMÉ --- */
    .stApp {
        /* Un dégradé profond style "espace" */
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
        font-family: 'Inter', sans-serif;
        color: #E0E0E0; /* Texte clair mais pas blanc pur pour moins fatiguer les yeux */
    }

    @keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

    /* --- NETTOYAGE DE L'INTERFACE --- */
    #MainMenu {visibility: hidden;} /* Cache le menu hamburger */
    footer {visibility: hidden;} /* Cache le "Made with Streamlit" */
    header {visibility: hidden;} /* Cache la barre de couleur en haut */
    .stDeployButton {display:none;} /* Cache le bouton deploy si présent */

    /* --- CENTRAGE DU CONTENU --- */
    /* On force le bloc principal à ne pas être trop large sur PC */
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* --- STYLES DES BULLES DE CHAT (GLASSMORPHISM) --- */
    /* On cible le conteneur du message */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important; /* Très transparent */
        backdrop-filter: blur(10px); /* Effet de flou derrière la bulle */
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1); /* Bordure subtile */
        border-radius: 20px !important; /* Gros arrondis */
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); /* Ombre douce pour la profondeur */
    }

    /* Personnalisation des avatars */
    .stChatMessage .stchat-avatar {
        background: transparent !important; /* On enlève le rond gris par défaut */
        font-size: 28px; /* Emojis plus gros */
    }

    /* Le texte dans les bulles */
    .stChatMessage markdown {
        color: #FFFFFF !important;
    }

    /* --- ZONE DE SAISIE (INPUT) --- */
    /* On la rend plus flottante */
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
    /* Couleur du placeholder (le texte "Écris ici...") */
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

# --- 3. CONNEXION GOOGLE (Le Moteur) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # On utilise l'ancien moteur, il est plus robuste pour l'instant
    genai.configure(api_key=API_KEY)
    # On prend le modèle "Lite" pour être sûr qu'il soit rapide et dispo
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
except:
    # Si erreur, on fait une jolie bulle d'erreur
    st.error("🔑 Oups ! Problème de clé API. Vérifie tes 'Secrets'.")
    st.stop()

# --- 4. INTERFACE UTILISATEUR (Le Squelette) ---

# En-tête stylisé
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🌌 Astrale</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7;'>L'intelligence artificielle nouvelle génération.</p>", unsafe_allow_html=True)

st.divider()

# Gestion de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = [
        # Petit message d'accueil stylé (facultatif)
        {"role": "assistant", "content": "Bonjour. Je suis Astrale. L'interface est prête. Pose ta question."}
    ]

# Affichage de la conversation
for message in st.session_state.messages:
    # Choix des avatars (Tu peux mettre des liens d'images si tu préfères !)
    avatar_icon = "🧑‍🚀" if message["role"] == "user" else "🛸"
    
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# --- 5. ZONE DE SAISIE & LOGIQUE IA ---
# Le placeholder est important pour le look
if prompt := st.chat_input("Pose une question à l'univers..."):
    
    # 1. Affichage utilisateur immédiat
    with st.chat_message("user", avatar="🧑‍🚀"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Consigne secrète pour l'IA
    prompt_systeme = f"""
    Tu es Astrale. Tes réponses doivent être :
    - Modernes et directes.
    - Bien structurées (utilise des listes à puces, du gras).
    - Si tu donnes du code, le bloc doit être parfait.
    Message de l'utilisateur : {prompt}
    """

    # 3. Réponse de l'IA avec petit effet d'attente
    with st.chat_message("assistant", avatar="🛸"):
        # On remplace le spinner moche par un texte qui clignote
        placeholder = st.empty()
        placeholder.markdown("*Astrale se connecte au flux...*")
        
        try:
            response = model.generate_content(prompt_systeme)
            # Petit délai artificiel pour faire "Premium" (facultatif, tu peux l'enlever)
            time.sleep(0.3) 
            
            # On efface le message d'attente et on met la vraie réponse
            placeholder.empty()
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            placeholder.empty()
            if "429" in str(e):
                st.warning("⚡ Trop de demandes simultanées. Patiente 30 secondes.")
            else:
                st.error("Une perturbation cosmique est survenue. Réessaie.")

# Petit espace en bas pour que la zone de saisie ne colle pas au dernier message
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
