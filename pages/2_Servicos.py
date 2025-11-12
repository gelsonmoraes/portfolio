import streamlit as st

st.subheader("O que eu faço")
st.write("Soluções de ponta a ponta: diagnóstico, protótipo e deploy.")

rows = [
    {"title": "Dashboards com Power BI",
     "desc": "Painéis para dados e relatórios gerenciais.",
     "items": ["Layouts responsivos", "Filtros/estado", "Upload & export", "Múltiplas páginas"]},
    {"title": "Apps e Dashboards em Streamlit",
     "desc": "Interfaces rápidas para dados e relatórios gerenciais.",
     "items": ["Layouts responsivos", "Filtros/estado", "Upload & export", "Múltiplas páginas"]},
    {"title": "Análise de Dados",
     "desc": "ETL com pandas, Power Query, exploração e visualizações.",
     "items": ["Limpeza/qualidade", "KPIs", "Storytelling visual", "Entrega reprodutível"]},
    {"title": "Backends em Python",
     "desc": "Automação de tarefas e integrações.",
     "items": ["Integração REST", "SQL/NoSQL", "Automação", "Web scraping"]},
    {"title": "Cursos e Treinamentos",
     "desc": "Cursos e treinamentos personalizados, presenciais ou online.",
     "items": ["Power BI", "Excel","Python", "Lógica de Programação"]},
    {"title": "Sites institucionais",
     "desc": "Sua empresa na internet.",
     "items": ["Presença online", "Sites institucionais","SEO básico", "Baixo custo"]},
    
]

cols = st.columns(2)
for i, card in enumerate(rows):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"#### {card['title']}")
            st.caption(card["desc"])
            st.write("• " + "\n• ".join(card["items"]))
