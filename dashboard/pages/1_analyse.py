# dashboard/pages/1_analyse.py
# TODO (étape 4) : appel agent + affichage rapport en live
import streamlit as st

st.title("Analyse en direct")
ticker = st.text_input("Ticker", placeholder="AAPL")

if st.button("Lancer l'analyse") and ticker:
    st.info("TODO : appeler agent.main.run_agent(ticker)")
