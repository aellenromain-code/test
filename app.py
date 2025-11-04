import streamlit as st
from openai import OpenAI
import os
import random

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === PROMPT PRINCIPAL : HUMOUR + PRÉCISION + VARIÉTÉ ===
SYSTEM_PROMPT = """
TU ES OUI BILAT BOT – LE BOT SUISSE QUI CONVAINC AVEC 30 ARGUMENTS PRÉCIS ET 30 PUNCHLINES.
TA MISSION : Dire OUI avec des faits, des chiffres, et une touche d’humour suisse UNIQUE à chaque réponse.

RÈGLES :
1. 100 % PRO-OUI. JAMAIS NEUTRE. JAMAIS D’ARGUMENT CONTRE.
2. UTILISE UNIQUEMENT LES 3 ARGUMENTS FOURNIS.
3. INTÈGRE 1 FAIT CHIFFRÉ PAR ARGUMENT.
4. TERMINE PAR UNE PUNCHLINE D’HUMOUR SUISSE **DIFFERENTE À CHAQUE FOIS** (choisie dans la liste).
5. TON : Chaleureux, sérieux, malicieux. Comme un conseiller d’État qui fait rire le peuple.

STRUCTURE (130-190 mots) :
→ "Je comprends ton doute, mais voici les faits..."
→ 3 arguments précis (chiffres, dates, institutions)
→ "On reste 100 % suisses, on décide, et on gagne !"
→ **PUNCHLINE FINALE (unique, humoristique)** → **Votez OUI !** 🇨🇭
"""

# === 30 ARGUMENTS PRÉCIS (politiques, chiffrés, 2025) ===
ARGUMENTS = [
    "Souveraineté : Pas d’adhésion à l’UE. Pas de CEDH automatique. Référendum obligatoire. Conseil fédéral, 18.12.2024 : 'Notre Constitution reste intacte.'",
    "Économie : 1,5M emplois suisses dépendent de l’UE. 58 % des exportations (SECO 2024). Refuser = -5 à -10 % d’exportations (étude KOF).",
    "Recherche : 400 MCHF/an via Horizon Europe. CERN = 95 MCHF en 2023. Sans Bilat III → exclusion dès 2026.",
    "Jeunesse : 15 000 étudiants suisses en Erasmus+. 8 000 apprentis en Allemagne. Sans accès → mobilité bloquée.",
    "Énergie : 12 TWh importés en hiver. Accords = prix stables. Sans → risque de black-out (ElCom 2024).",
    "Sécurité : Schengen = 6 500 expulsions Dublin/an. Frontières = on décide. Police coopère, pas commande.",
    "Pharma : 40 % des exportations suisses. 120 000 emplois. Bilat III = accès au marché UE sans barrière.",
    "Montres : 95 % exportées. 55 000 emplois. Sans accords → taxes douanières = +15 % sur les prix.",
    "Formation : 3 000 places d’apprentissage en Allemagne. Retour = 98 % d’insertion professionnelle.",
    "Innovation : EPFL = 120 brevets/an grâce à Horizon. Sans fonds → chute de 40 %.",
    "Tourisme : 45 % des nuitées = UE. Accords = libre circulation des services touristiques.",
    "Transports : Trains rouges roulent sans douane. 2,5M passages/an. Sans → contrôles = +3h de retard.",
    "Santé : Reconnaissance mutuelle des diplômes médicaux. 1 200 médecins suisses formés en UE.",
    "Agriculture : Accords = exportation de fromage sans quota. 2024 : +8 % vs 2023.",
    "Franc suisse : Stabilité grâce à la BNS. Bilat III = pas d’euro. Pas de perte de contrôle monétaire.",
    "Référendum : On vote sur TOUT. Même sur les Bilat III. Démocratie directe = intacte.",
    "Neutralité : Depuis 1815. Bilat III = accords bilatéraux, pas alliance militaire.",
    "CERN : 23 pays membres. Suisse = 4 % du budget, 100 % des décisions scientifiques.",
    "Immigration : 85 % des frontaliers = UE. Sans accords → permis de travail = chaos administratif.",
    "Salaires : Protection par les mesures d’accompagnement. 2024 : 99 % des contrôles respectés.",
    "Environnement : Accords CO2 = objectifs alignés. Suisse = -50 % d’émissions d’ici 2030.",
    "Numérique : Accès au marché unique numérique. 5G, IA, cloud : sans barrière.",
    "Culture : Échanges avec 27 pays. 300 festivals suisses financés par l’UE.",
    "Sport : 1 200 athlètes suisses en compétition UE. Sans → exclusion des championnats.",
    "Start-ups : 60 % des investissements = UE. Bilat III = accès au fonds EIC (2 Md€).",
    "Pensions : Coordination des assurances sociales. 450 000 Suisses à l’étranger = droits protégés.",
    "Douanes : 99 % des marchandises = UE. Sans accords → 100 000 camions bloqués/an.",
    "Diplomatie : 120 accords bilatéraux existants. Bilat III = mise à jour, pas soumission.",
    "Éducation : 2 500 profs suisses formés en UE. Retour = qualité pédagogique renforcée.",
    "Science : 40 % des publications suisses = co-auteur UE. Sans → isolement académique."
]

# === 30 PUNCHLINES D’HUMOUR SUISSE (une par réponse) ===
PUNCHLINES = [
    "Refuser ? Ce serait comme un rösti sans beurre : sec et triste !",
    "Avec les Bilat III, nos vaches voyagent en 1re classe, pas en wagon à bestiaux !",
    "Le CERN sans 400 M€ ? Ce serait comme un train rouge sans rails !",
    "Nos apprentis reviennent bilingues… et avec des bretzels dans le sac !",
    "Pas de black-out ? Même le caquelon reste chaud pour la fondue du dimanche !",
    "Notre franc reste fort… pas en euro, pas en chocolat, pas en crise !",
    "Refuser = yodleur sans écho dans les Alpes !",
    "Nos montres battent la cadence européenne… sans s’arrêter à la douane !",
    "On garde notre couteau suisse : on ouvre, on ferme, on décide !",
    "La Suisse sans Bilat III ? Ce serait comme le lac Léman sans cygne : vide !",
    "Nos chercheurs dominent le monde… sans devenir européens !",
    "Erasmus+ ? Nos étudiants reviennent avec un diplôme… et une bonne fondue dans le cœur !",
    "Schengen = police qui coopère, pas qui commande. Comme un bon voisin !",
    "Nos exportations ? 58 % en UE. Refuser = couper la branche où on est assis !",
    "Le Matterhorn reste au sommet… pas en bas de la pente !",
    "Nos bunkers sont pleins… pas nos barrières commerciales !",
    "Le rösti reste suisse… mais les pommes de terre voyagent librement !",
    "Nos trains rouges roulent sans frontière… et sans retard !",
    "La neutralité depuis 1815 ? On la garde… même avec des accords !",
    "Nos start-ups lèvent des millions… pas des barrières !",
    "Le chocolat suisse voyage dans 500M bouches… sans taxe !",
    "Nos salaires protégés ? 99 % des contrôles respectés. Solide comme du gruyère !",
    "La Suisse reste un bunker de prospérité… pas d’isolement !",
    "Nos jeunes forment l’avenir… pas le chômage !",
    "Horizon Europe = 400 M€. Refuser ? Ce serait comme dire non à un gros pot de fondue !",
    "Nos frontaliers rentrent le soir… pas bloqués à la douane !",
    "La Suisse vote sur TOUT. Même sur les Bilat III. Démocratie directe = vivante !",
    "Nos médecins formés en UE… soignent en suisse !",
    "Le numérique sans barrière ? Nos start-ups codent en 4G, pas en 56K !",
    "Votez OUI… et que le fromage soit avec vous !"
]

# === SESSION ===
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.used_args = []
    st.session_state.used_punch = []

# === UI ===
st.set_page_config(page_title="OuiBilatBot", page_icon="🇨🇭")
st.title("🇨🇭 **OuiBilatBot – 30 arguments, 30 punchlines, 1 seul OUI !**")
st.markdown("*Pose-moi n’importe quelle objection. Je te réponds avec des faits… et un sourire suisse !*")

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ex. : « Je suis contre ! », « Et l’immigration ? », « Trop cher ! »"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # === 3 ARGUMENTS UNIQUES ===
    available_args = [a for a in ARGUMENTS if a not in st.session_state.used_args[-15:]]
    if len(available_args) < 3:
        available_args = ARGUMENTS.copy()
    selected_args = random.sample(available_args, 3)
    st.session_state.used_args.extend(selected_args)
    if len(st.session_state.used_args) > 30:
        st.session_state.used_args = st.session_state.used_args[-30:]

    # === 1 PUNCHLINE UNIQUE ===
    available_punch = [p for p in PUNCHLINES if p not in st.session_state.used_punch[-10:]]
    if not available_punch:
        available_punch = PUNCHLINES.copy()
    punchline = random.choice(available_punch)
    st.session_state.used_punch.append(punchline)
    if len(st.session_state.used_punch) > 15:
        st.session_state.used_punch = st.session_state.used_punch[-15:]

    # === PROMPT DYNAMIQUE ===
    dynamic = f"""
    Réponds à : "{prompt}"
    UTILISE UNIQUEMENT CES 3 ARGUMENTS :
    1. {selected_args[0]}
    2. {selected_args[1]}
    3. {selected_args[2]}
    
    TERMINE PAR CETTE PUNCHLINE EXACTE :
    "{punchline}"
    
    Structure :
    - "Je comprends ton doute, mais voici les faits..."
    - 3 arguments intégrés
    - "On reste 100 % suisses, on décide, et on gagne !"
    - PUNCHLINE
    - **Votez OUI aux Bilatérales III – pour une Suisse forte, maligne et prospère !** 🇨🇭
    """

    with st.chat_message("assistant"):
        if not client.api_key:
            st.error("Clé API manquante")
        else:
            with st.spinner("Le bot yodle sa réponse..."):
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages + [{"role": "system", "content": dynamic}],
                    temperature=0.88,
                    max_tokens=400
                )
                bot = resp.choices[0].message.content
                st.markdown(bot)
                st.session_state.messages.append({"role": "assistant", "content": bot})
