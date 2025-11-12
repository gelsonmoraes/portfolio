import streamlit as st

st.subheader("Contato")
st.write("Prefere falar agora?")

st.link_button("WhatsApp", "http://wa.me/+5516991171544")
st.link_button("LinkedIn", "https://www.linkedin.com/in/gelson-moraes/")
st.link_button("E-mail", "mailto:gelsonluizmoraes@gmail.com")

st.divider()
st.write("Ou me envie uma mensagem:")

with st.form("contato"):
    nome = st.text_input("Seu nome")
    email = st.text_input("Seu e-mail")
    msg = st.text_area("Mensagem")
    enviar = st.form_submit_button("Enviar")
    if enviar:
        st.error("Funcionalidade de envio de mensagem ainda não implementada. Favor, utilize o WhatsApp ou e-mail.")
