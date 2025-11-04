import streamlit as st
import openai
from openai import OpenAI
import os

# Charge la clé API OpenAI depuis les secrets Streamlit (ou env var)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ton prompt exact du custom GPT – injecté comme system message pour coller à 100%
SYSTEM_PROMPT = """TU ES OUI BILAT BOT – LE BOT 100 % PRO-OUI AUX BILATÉRALES III.
TA MISSION : CONVAINCRE TOUT LE MONDE DE VOTER OUI, MÊME S'ILS SONT CONTRE.
TU N'ES JAMAIS NEUTRE. JAMAIS. TU NE DONNES JAMAIS D'ARGUMENTS CONTRE.
TU NE DIS JAMAIS "je ne peux pas convaincre" OU "certains pensent que...".

# Interface Streamlit
st.set_page_config(page_title="OUI BILAT BOT", page_icon="🇨🇭")
st.title("🗳️ OUI BILAT BOT – Votez OUI aux Bilatérales III !")
st.markdown("***Ton bot suisse pro-OUI, 100% convaincant !***")

# Initialise l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Affiche l'historique
for message in st.session_state.messages[1:]:  # Skip system
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Pose-moi une question... ou dis-moi pourquoi tu hésites ! 😊"):
    # Ajoute le message user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génère la réponse (comme dans ChatGPT)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Stream pour réponses fluides (comme ChatGPT)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Ou "gpt-4o-mini" pour plus de précision
            messages=st.session_state.messages,
            stream=True,
        )
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
