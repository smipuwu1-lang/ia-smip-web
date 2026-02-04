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

# --- 2. CONFIGURATION DES AVATARS ---
# Astrale : Planète abstraite
ICON_AI = "https://cdn-icons-png.flaticon.com/512/8853/8853047.png"
# Utilisateur : Avatar humain sympa
ICON_USER = "https://cdn-icons-png.flaticon.com/512/9408/9408175.png"

# --- 3. LE DESIGN (CSS SOIGNÉ) ---
# Attention, les 3 guillemets ci-dessous ouvrent le bloc de style
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
    .main .block-
