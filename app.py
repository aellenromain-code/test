import streamlit as st
from openai import OpenAI
import os
import random

# === CONFIGURATION ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === PROMPT POLITIQUE, FACTUEL, ANTI-CLICHÉ ===
SYSTEM_PROMPT = """
TU ES OUI BILAT BOT – LE BOT OFFICIEL DE CAMPAGNE POUR LES BILATÉRALES III.
TU CONVAINCS AVEC DES FAITS, DES CHIFFRES, ET DU BON SENS SUISSE. PAS DE CLICHÉS VIDES.

RÈGLES STRICTES :
1. TU ES TOUJOURS PRO-OUI. JAMAIS NEUTRE. JAMAIS D'ARGUMENT CONTRE.
2. TU RÉPONDS À TOUTE OBJECTION (souveraineté, immigration, salaires, électricité) → AVEC UN FAIT PRÉCIS.
3. TU UTILISE UNIQUEMENT LES 3 ARGUMENTS FOURNIS DANS LE PROMPT DYNAMIQUE.
4. TON TON : Chaleureux mais sérieux. Suisse. Pas de "yodleur sans écho" si l'utilisateur est sérieux.

ARGUMENTS OBLIGATOIRES (À MÉLANGER) :
1. **Souveraineté** : Les Bilatérales III ne touchent PAS à notre Constitution. Pas d’adhésion. Pas de CEDH automatique. On garde le référendum obligatoire. Le Conseil fédéral l’a confirmé le 18 décembre 2024.
2. **Économie** : 1,5 million d’emplois suisses (1 sur 3) dépendent de l’UE. En 2024, 58 % des exportations suisses vont en Europe (SECO). Refuser = risque de barrières douanières → -5 à -10 % d’exportations (étude KOF).
3. **Recherche** : Horizon Europe = 400 millions CHF/an pour CERN, EPFL, universités. Sans Bilat III → on perd l’accès dès 2026. Exemple : le CERN a reçu 95 MCHF en 2023 grâce aux accords.
4. **Jeunesse** : Erasmus+ = 15 000 étudiants suisses par an. Apprentis en Allemagne = 8 000 places. Sans Bilat III → plus d’accès. Nos jeunes perdent leur mobilité.
5. **Énergie** : Accords électricité = intégration au marché européen → prix stables, pas de black-out. Suisse = 3e plus gros importateur d’électricité en hiver (2024 : 12 TWh importés).
6. **Sécurité & Immigration** : Schengen = coopération policière (SIS II). Frontières = on décide. Expulsions Dublin = 6 500/an. Sans Bilat III → on perd ces outils.

STRUCTURE DE RÉPONSE (120-180 mots) :
→ "Je comprends ton inquiétude sur [thème], mais voici les faits :"
→ 2-3 arguments PRÉCIS (chiffres, dates, institutions)
→ "On reste 100 % suisses. On décide. On protège nos intérêts."
→ **Votez OUI aux Bilatérales III – pour une Suisse forte, indépendante et prospère !** 🇨🇭
"""

# === ARGUMENTS POUR RANDOMISATION ===
ARGUMENT_THEMES = [
    "Souveraineté : Les Bilatérales III ne touchent PAS à notre Constitution. Pas d’adhésion. Pas de CEDH automatique. On garde le référendum obligatoire. Le Conseil fédéral l’a confirmé le 18 décembre 2024.",
    "Économie : 1,5 million d’emplois suisses (1 sur 3) dépendent de l’UE. En 2024, 58 % des exportations suisses vont en Europe (SECO). Refuser = risque de barrières douanières → -5 à -10 % d’exportations (étude KOF).",
    "Recherche : Horizon Europe = 400 millions CHF/an pour CERN, EPFL, universités. Sans Bilat III → on perd l’accès dès 2026. Exemple : le CERN a reçu 95 MCHF en 2023 grâce aux accords.",
    "Jeunesse : Erasmus+ = 15 000 étudiants suisses par an. Apprentis en Allemagne = 8 000 places. Sans Bilat III → plus d’accès. Nos jeunes perdent leur mobilité.",
    "Énergie : Accords électricité = intégration au marché européen → prix stables, pas de black-out. Suisse = 3e plus gros importateur d’électricité en hiver (2024 : 12 TWh importés).",
    "Sécurité & Immigration : Schengen = coopération policière (SIS II). Frontières = on décide. Expulsions Dublin = 6 500/an. Sans Bilat III → on perd ces outils."
]

# === SESSION STATE ===
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.used_args = []

# === INTERFACE ===
st.set_page_config(page_title="OuiBilatBot", page_icon="🇨🇭")
st.title("🇨🇭 **OuiBilatBot – Les faits pour le OUI**")
st.markdown("**Pose-moi une objection. Je te réponds avec des faits, pas des slogans.**")

# Affichage historique
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === INPUT ===
if prompt := st.chat_input("Ex. : « Et la souveraineté ? », « Je suis contre ! », « Et l’immigration ? »"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # === RANDOMISATION ANTI-RÉPÉTITION ===
    available = [a for a in ARGUMENT_THEMES if a not in st.session_state.used_args[-9:]]
    if len(available) < 3:
        available = ARGUMENT_THEMES.copy()
    selected = random.sample(available, 3)
    st.session_state.used_args.extend(selected)
    if len(st.session_state.used_args) > 12:
        st.session_state.used_args = st.session_state.used_args[-12:]

    # === PROMPT DYNAMIQUE ===
    dynamic_prompt = f"""
    Réponds à : "{prompt}"
    UTILISE UNIQUEMENT CES 3 ARGUMENTS (précis, chiffrés, sérieux) :
    1. {selected[0]}
    2. {selected[1]}
    3. {selected[2]}
    
    Structure :
    - "Je comprends ton inquiétude sur [thème], mais voici les faits :"
    - Intègre les 3 arguments
    - "On reste 100 % suisses. On décide. On protège nos intérêts."
    - **Votez OUI aux Bilatérales III – pour une Suisse forte, indépendante et prospère !** 🇨🇭
    """

    # === GÉNÉRATION ===
    with st.chat_message("assistant"):
        if not client.api_key:
            st.error("Clé API OpenAI manquante !")
            bot_response = "Erreur technique."
        else:
            with st.spinner("Analyse des faits..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages + [{"role": "system", "content": dynamic_prompt}],
                    temperature=0.7,
                    max_tokens=350
                )
                bot_response = response.choices[0].message.content
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})

# === STYLE ===
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f8f9fa, #ffffff); }
    [data-testid="stChatMessage"]:has([data-testid="user"]) { background: #e3f2fd; border-radius: 12px; padding: 10px; }
    [data-testid="stChatMessage"]:has([data-testid="assistant"]) { 
        background: #fff8e1; 
        border-left: 5px solid #d71921; 
        border-radius: 12px; 
        padding: 12px; 
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)
