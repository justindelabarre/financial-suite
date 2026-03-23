# dashboard/pages/3_historique.py
# TODO (étape 4) : lecture des rapports sauvegardés dans reports/
import streamlit as st
import os
from pathlib import Path

st.title("Historique des rapports")

reports_dir = Path(__file__).parent.parent.parent / "reports"
if not reports_dir.exists():
    st.warning("Aucun rapport trouvé.")
else:
    files = sorted(reports_dir.glob("*.md"), reverse=True)
    if not files:
        st.info("Aucun rapport pour l'instant.")
    else:
        selected = st.selectbox("Rapport", [f.name for f in files])
        content = (reports_dir / selected).read_text(encoding="utf-8")
        st.markdown(content)
