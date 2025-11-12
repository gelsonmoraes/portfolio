import streamlit as st
from pathlib import Path
from PIL import Image

ASSETS = Path("assets")
PROFILE = ASSETS / "profile.webp"

st.title("Gelson Moraes")
st.caption("Especialista de BI | Analista de BI | Analista de Dados | Professor | Instrutor")
st.divider()

col1, col2 = st.columns([0.9, 2.1], vertical_alignment="top")
with col1:
    if PROFILE.exists():
        img = Image.open(PROFILE)
        st.image(img, width=200, caption="Foto de perfil de Gelson (alt)", use_container_width=False)
    else:
        st.info("Adicione sua foto em assets/profile.webp")

with col2:
    st.subheader("Como posso ajudar")
    st.write(
        """Especialista em Business Intelligence com experiência em Power BI, SQL e Python, focado em transformar dados em insights estratégicos que otimizam processos e impulsionam resultados.

Com 13 anos de atuação na saúde pública, desenvolvi uma compreensão profunda dos desafios de gestão de dados, eficiência operacional e tomada de decisão baseada em evidências. Essa vivência me permite conectar análise técnica e visão de negócio para gerar soluções de BI realmente aplicáveis.

Também atuo na formação profissional em tecnologia, ministrando cursos de desenvolvimento de software e análise de dados — experiência que fortalece minha habilidade de traduzir complexidade em clareza e ação.

Certificações: 
https://www.credly.com/users/gelsonluizmoraes/badges

Lattes:
http://lattes.cnpq.br/9164802305306227"""
    )



# CTA primário
st.link_button("Fale comigo no WhatsApp", "https://wa.me/+5516991171544")
