import streamlit as st
from google import genai

st.set_page_config(page_title="Testeur Ultime", page_icon="🛠️")
st.title("🛠️ Recherche du modèle qui marche...")

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except:
    st.error("Problème de clé API.")
    st.stop()

# Liste des suspects à tester
candidats = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-flash-8b",
    "gemini-2.0-flash-exp",
    "gemini-pro",
    "gemini-1.0-pro"
]

modele_gagnant = None

st.write("J'essaie de dire 'Bonjour' avec chaque modèle...")

# On teste chaque modèle un par un
for nom_modele in candidats:
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write(f"Testing **{nom_modele}**...")
    
    try:
        # On tente une vraie génération de texte
        response = client.models.generate_content(
            model=nom_modele,
            contents="Réponds juste par OK."
        )
        # SI ON ARRIVE ICI, C'EST QUE ÇA MARCHE !
        with col2:
            st.success("✅ FONCTIONNE !")
        modele_gagnant = nom_modele
        break # On arrête de chercher, on a trouvé !
        
    except Exception as e:
        with col2:
            # On affiche l'erreur en petit pour info
            if "404" in str(e):
                st.error("❌ Introuvable (404)")
            elif "429" in str(e):
                st.warning("⚠️ Trop utilisé (429)")
            else:
                st.error(f"❌ Erreur : {e}")

st.divider()

if modele_gagnant:
    st.balloons()
    st.success(f"🏆 LE VAINQUEUR EST : {modele_gagnant}")
    st.code(f'MODEL_NAME = "{modele_gagnant}"', language="python")
    st.write("👆 Copie cette ligne exacte, remets ton code Astrale IA, et colle-la à la place de l'ancienne !")
else:
    st.error("Aucun modèle n'a voulu répondre... C'est un problème de compte Google.")
