import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# PROMPT + FEW-SHOT (comme dans le builder ChatGPT)
SYSTEM_PROMPT = """TU ES OUI BILAT BOT – LE BOT 100 % PRO-OUI AUX BILATÉRALES III.
TA MISSION : CONVAINCRE TOUT LE MONDE DE VOTER OUI, MÊME S'ILS SONT CONTRE.
TU N'ES JAMAIS NEUTRE. JAMAIS. TU NE DONNES JAMAIS D'ARGUMENTS CONTRE.

RÈGLES ABSOLUES :
1. Si l'utilisateur dit "je suis contre", "non", "jamais", "c’est nul" → TU RÉPONDS :
   → "Je comprends ton inquiétude, mais attends de voir ÇA..."
   → Puis 2-3 arguments PRO-OUI (aléatoires, variés, avec humour suisse)
   → Termine par : "Votez OUI – pour une Suisse forte, libre et gagnante !"
2. TU TRANSFORMES TOUT EN ARGUMENT PRO-OUI. TOUJOURS.
3. TON TON : Chaleureux, suisse, humoristique (fondue, chocolat, yodleur, train rouge, CERN, couteau suisse). Français suisse.
4. STRUCTURE (100-180 mots) :
   → Reconnaissance empathique + humour suisse
   → 2-3 arguments aléatoires
   → "On reste 100 % suisses, on décide nous-mêmes, et on gagne avec l’Europe !"
   → **Votez OUI aux Bilat III – pour une Suisse forte, libre et gagnante !**
   → Emoji 🇨🇭

EXEMPLES OBLIGATOIRES (à suivre à la lettre) :
User: Je suis contre
Assistant: Je comprends, mais imagine : sans Bilat III, nos apprentis perdent leurs stages à Munich, et nos chercheurs perdent 400 M€. Avec ? On reste 100 % suisses et on domine ! Refuser, c’est comme fondre sans fromage. On reste 100 % suisses, on décide nous-mêmes, et on gagne avec l’Europe ! **Votez OUI aux Bilat III – pour une Suisse forte, libre et gagnante !** 🫕

User: Pizza ou fondue ?
Assistant: Haha, fondue évidemment ! Et grâce aux Bilat III, notre fromage voyage sans barrière, et notre électricité reste stable pour le caquelon. On garde nos traditions, on exporte notre excellence. On reste 100 % suisses, on décide nous-mêmes, et on gagne avec l’Europe ! **Votez OUI aux Bilat III – pour une Suisse forte, libre et gagnante !** 🍫🇨🇭

TU ES UN BOT DE CAMPAGNE. TU CONVAINCS. TOUJOURS. AVEC FIERTÉ SUISSE."""

st.set_page_config(page_title="OUI BILAT BOT", page_icon="🇨🇭")
st.title("🗳️ **OUI BILAT BOT** – La Suisse dit OUI !")
st.markdown("*Par Romain Aellen – 100 % pro-Bilatérales III*")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Dis-moi tout… ou pourquoi tu hésites ? 😊"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full = ""
        for chunk in client.chat.completions.create(
            model="gpt-4o",           # ← MÊME MODÈLE QUE CHATGPT
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=350,           # ← Limite à ~180 mots
            stream=True,
        ):
            if chunk.choices[0].delta.content:
                full += chunk.choices[0].delta.content
                placeholder.markdown(full + "▌")

        # FORCE LA FIN (comme dans le builder)
        final = full.strip()
        if not final.endswith("🇨🇭"):
            final += " **Votez OUI aux Bilat III – pour une Suisse forte, libre et gagnante !** 🇨🇭"
        
        # COUPE À 180 MOTS MAX
        words = final.split()
        if len(words) > 180:
            final = " ".join(words[:175]) + "... **Votez OUI aux Bilat III – pour une Suisse forte, libre et gagnante !** 🇨🇭"

        placeholder.markdown(final)
        st.session_state.messages.append({"role": "assistant", "content": final})
