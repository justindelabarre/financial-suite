# dashboard/app.py
# Point d'entrée Streamlit
# Lancer avec : streamlit run dashboard/app.py
import streamlit as st

st.set_page_config(
    page_title="Financial Suite",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Financial Suite")
st.markdown("Sélectionne une page dans la barre latérale.")
