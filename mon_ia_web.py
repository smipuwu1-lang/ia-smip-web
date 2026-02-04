import streamlit as st
from google import genai

st.title("🕵️ Scanner de Modèles Google")

try:
    # Connexion
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    st.write("Voici la liste exacte des noms que tu peux mettre dans ton code :")
    
    # On récupère la liste officielle
    for m in client.models.list():
        # On affiche uniquement les modèles qui savent écrire du texte
        if "generateContent" in m.supported_generation_methods:
            # On nettoie le nom pour qu'il soit prêt à copier
            nom_propre = m.name.replace("models/", "")
            st.code(f'MODEL_NAME = "{nom_propre}"')

except Exception as e:
    st.error(f"Erreur de connexion : {e}")

