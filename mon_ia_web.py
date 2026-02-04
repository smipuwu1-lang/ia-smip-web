import streamlit as st
from google import genai

st.title("🕵️ Scanner de Modèles (Version V2)")

try:
    # Connexion
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    st.write("Voici les noms EXACTS que Google reconnait pour ton compte :")
    st.write("Copie l'un d'eux pour remplacer ton MODEL_NAME.")
    
    # On affiche tout sans filtre pour éviter les bugs
    for m in client.models.list():
        # On affiche le nom technique directement
        # Parfois le nom arrive avec "models/" devant, on le nettoie pas, on regarde ce qu'il donne.
        st.code(f'MODEL_NAME = "{m.name}"')

except Exception as e:
    st.error(f"Erreur : {e}")
