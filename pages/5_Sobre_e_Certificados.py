import streamlit as st

st.subheader("Sobre mim")
st.write(
    "Consultor e instrutor de BI, com atuação em Power BI, SQL e Python. "
    "Experiência em saúde pública e formação em tecnologia, unindo visão de negócio e técnica. "
    "Possuo certificações Microsoft reconhecidas no mercado, como AI-900, DP-900, PL-900 e outras."
)

st.subheader("Certificações & Currículo")
st.write("[Acesse meu perfil no Creadly para ver minhas certificações](https://www.credly.com/users/gelsonluizmoraes/badges)")
st.write("[Aqui você encontra meu Lattes](http://lattes.cnpq.br/9164802305306227)")
st.write("[E aqui está meu Linkedin](https://www.linkedin.com/in/gelson-moraes/)")

st.download_button("Baixar CV (PDF)", data=b"", file_name="Curriculo - Gelson Luiz Moraes.pdf", disabled=True, help="Substitua com seu PDF.")
