import streamlit as st
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# --- CONFIGURATION ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Il manque la clé API dans les 'Secrets'.")
    st.stop()

st.set_page_config(page_title="Astrale IA", page_icon="🌌")
st.title("🌌 Astrale IA")

# Connexion
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

# --- LE PASSE-PARTOUT : SÉLECTION AUTOMATIQUE DU MODÈLE ---
# On liste les noms que Google accepte sur ton compte
try:
    mes_modeles = []
    # On récupère la liste brute
    for m in client.models.list():
        # On enlève le préfixe "models/" pour avoir le nom pur
        nom_propre = m.name.replace("models/", "")
        mes_modeles.append(nom_propre)
    
    # Voici l'ordre de préférence (du meilleur au moins bon)
    # On cherche le premier qui existe dans TA liste
    liste_souhaits = [
        "gemini-1.5-flash",       # Le standard
        "gemini-1.5-flash-001",   # La version précise
        "gemini-1.5-flash-002",   # La version mise à jour
        "gemini-1.5-flash-8b",    # La version légère
        "gemini-pro",             # L'ancien fiable
        "gemini-1.0-pro"          # L'alternative
    ]

    MODEL_NAME = "gemini-1.5-flash" # Valeur par défaut au cas où
    
    found = False
    for candidat in liste_souhaits:
        if candidat in mes_modeles:
            MODEL_NAME = candidat
            found = True
            break
            
    # Petit message discret pour savoir lequel a gagné (tu pourras l'enlever plus tard)
    st.caption(f"Cerveau connecté : `{MODEL_NAME}`")

except Exception as e:
    # Si le scan échoue, on force une valeur sûre
    MODEL_NAME = "gemini-1.5-flash-001"
    st.caption(f"Mode secours activé : {MODEL_NAME}")

search_tool = types.Tool(google_search=types.GoogleSearch())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "source_html" in message:
            components.html(message["source_html"], height=150, scrolling=True)

# Zone de saisie
if prompt := st.chat_input("Pose ta question à Astrale..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # CONSIGNE CACHÉE
    prompt_avec_identite = f"""
    Consigne système stricte :
    Tu es Astrale IA.
    Si l'utilisateur te demande ton identité (qui es-tu, qui t'a créé...), 
    réponds UNIQUEMENT : "Je suis Astrale IA, un modèle d'intelligence artificielle entraîné par Smip et Google."
    Pour le reste, réponds normalement.
    
    Question : {prompt}
    """

    with st.chat_message("assistant"):
        with st.spinner("Astrale réfléchit..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt_avec_identite,
                    config=types.GenerateContentConfig(
                        tools=[search_tool],
                        response_modalities=["TEXT"]
                    )
                )
                
                st.markdown(response.text)
                message_data = {"role": "assistant", "content": response.text}

                if response.candidates[0].grounding_metadata.search_entry_point:
                    html = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
                    components.html(html, height=150, scrolling=False)
                    message_data["source_html"] = html
                
                st.session_state.messages.append(message_data)

            except Exception as e:
                st.error(f"Erreur avec le modèle {MODEL_NAME} : {e}")
