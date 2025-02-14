import openai
import streamlit as st
import json
import os
from datetime import datetime

# Charger la clé API depuis les variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


# Fonction pour interagir avec ChatGPT
def chat_with_gpt(prompt, history=[]):
    messages = history + [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Modifier selon ton abonnement
        messages=messages
    )
    reply = response["choices"][0]["message"]["content"]
    history.append({"role": "assistant", "content": reply})
    return reply, history


# Sauvegarde de la conversation
def save_conversation(title, history):
    filename = f"conversations/{title.replace(' ', '_')}.json"
    os.makedirs("conversations", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    return filename


# Interface Streamlit
st.set_page_config(page_title="GPT Assistant Personnel", layout="wide", initial_sidebar_state="expanded")
st.title("🧠 GPT Assistant Personnel")

# Activer/Désactiver le mode sombre
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode


st.sidebar.button("🌙 Mode Sombre / ☀️ Mode Clair", on_click=toggle_dark_mode)

if st.session_state.dark_mode:
    st.markdown("""
        <style>
            body { background-color: #0E1117; color: white; }
            .stTextInput, .stTextArea, .stButton>button { background-color: #22272E; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Nom de la discussion
title = st.text_input("Nom de la discussion", "Nouvelle Discussion")

# Sujet global
subject = st.selectbox("Choisir un sujet", ["Finance", "NoCode", "Entrepreneuriat", "Autre"])

# Historique des discussions
if "history" not in st.session_state:
    st.session_state.history = []

# Champ de saisie utilisateur
user_input = st.text_area("Votre message")

if st.button("Envoyer"):
    if user_input:
        with st.spinner("GPT est en train de répondre..."):
            reply, st.session_state.history = chat_with_gpt(user_input, st.session_state.history)

        # Affichage des échanges sous forme de chat
        st.markdown("**Vous :** " + user_input)
        st.markdown("**GPT :** " + reply)

    else:
        st.warning("Veuillez entrer un message.")

# Sauvegarde de la conversation
if st.button("Sauvegarder la discussion"):
    filename = save_conversation(title, st.session_state.history)
    st.success(f"Discussion sauvegardée : {filename}")

# Bouton pour réinitialiser la conversation
if st.button("🔄 Réinitialiser la conversation"):
    st.session_state.history = []
    st.experimental_rerun()

# Affichage de l'historique des messages
st.subheader("📝 Historique des messages")
for message in st.session_state.history:
    role = "**Vous :** " if message["role"] == "user" else "**GPT :** "
    st.markdown(role + message["content"])
