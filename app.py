import streamlit as st

st.set_page_config(page_title="Portfólio · Gelson", layout="wide")
# Páginas (preferência atual do Streamlit)
home = st.Page("pages/1_Apresentacao.py", title="Apresentação")
servicos = st.Page("pages/2_Servicos.py", title="Serviços")
portfolio = st.Page("pages/3_Portfolio.py", title="Portfólio")
dashboard = st.Page("pages/4_Dashboard.py", title="Dashboard")
sobre = st.Page("pages/5_Sobre_e_Certificados.py", title="Sobre & Certificados")
contato = st.Page("pages/6_Contato.py", title="Contato")
pg = st.navigation(pages=[home, servicos, portfolio, dashboard, sobre, contato])
st.sidebar.caption("© Gelson Moraes — Todos os direitos reservados")

pg.run()
