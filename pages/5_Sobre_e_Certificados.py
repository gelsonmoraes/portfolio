import streamlit as st
from pathlib import Path

st.subheader("Sobre mim")
st.write(
    "Consultor e instrutor de BI, com atuação em Power BI, SQL e Python. "
    "Experiência em saúde pública e formação em tecnologia, unindo visão de negócio e técnica. "
    "Possuo certificações Microsoft reconhecidas no mercado, como AI-900, DP-900, PL-900 e outras."
)

st.subheader("Certificações & Currículo")
st.write("[Acesse meu perfil no Credly para ver minhas certificações](https://www.credly.com/users/gelsonluizmoraes/badges)")
st.write("[Aqui você encontra meu Lattes](http://lattes.cnpq.br/9164802305306227)")
st.write("[E aqui está meu LinkedIn](https://www.linkedin.com/in/gelson-moraes/)")

# Caminho do currículo PDF
pdf_path = Path("assets/Curriculo - Gelson Luiz Moraes.pdf")

# Verifica se o arquivo existe antes de disponibilizar
if pdf_path.exists():
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    st.download_button(
        label="📄 Baixar Currículo (PDF)",
        data=pdf_bytes,
        file_name=pdf_path.name,
        mime="application/pdf",
        help="Clique para baixar o currículo completo em PDF."
    )
else:
    st.warning("⚠️ Currículo ainda não disponível. Adicione o PDF na pasta `assets` para habilitar o download.")