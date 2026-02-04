import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Astrale IA", page_icon="🌌")
st.title("🌌 Astrale IA")

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Clé API manquante.")
    st.stop()

# --- LE TERMINATOR : Il cherche le modèle qui marche ---
@st.cache_resource
def trouver_modele_actif():
    # Liste de tous les noms possibles (du plus récent au plus vieux)
    liste_suspects = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro",
        "gemini-pro",        # Le classique (Gemini 1.0)
        "gemini-1.0-pro"
    ]
    
    for nom in liste_suspects:
        try:
            # On tente une micro-connexion
            model = genai.GenerativeModel(nom)
            model.generate_content("test")
            return nom # Si ça ne plante pas, c'est le bon !
        except:
            continue # Si erreur 404, au suivant !
            
    return None

# On lance la recherche une seule fois au démarrage
NOM_MODELE_VALIDE = trouver_modele_actif()

if NOM_MODELE_VALIDE is None:
    st.error("❌ C'est incroyable... Aucun modèle ne répond sur ce compte. Vérifie tes quotas Google.")
    st.stop()
else:
    # On affiche discrètement lequel a gagné
    st.caption(f"✅ Connecté sur le canal : `{NOM_MODELE_VALIDE}`")

# --- LE CHAT ASTRALE IA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pose ta question à Astrale..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Préparation
    model = genai.GenerativeModel(NOM_MODELE_VALIDE)
    
    # Consigne d'identité
    prompt_final = f"""
    Tu es Astrale IA, créée par Smip et Google.
    Si on te demande qui tu es, réponds : "Je suis Astrale IA, créée par Smip."
    Question : {prompt}
    """

    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                response = model.generate_content(prompt_final)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Oups : {e}")
