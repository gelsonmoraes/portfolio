import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
import os


#  Configurações e caminhos
BASE_DIR = Path(__file__).resolve().parents[1]  # volta à raiz do projeto
ASSETS_DIR = BASE_DIR / "assets"
DATA = ASSETS_DIR / "portfolio.csv"
IMG_DIR = ASSETS_DIR / "portfolio"

st.subheader("Trabalhos realizados")
st.caption("Projetos com desafio, abordagem e resultados.")


#  Carregamento de dados
@st.cache_data
def load_data():
    if DATA.exists():
        df = pd.read_csv(DATA)
        for col in ("ano", "setor", "tags"):
            if col in df.columns:
                df[col] = df[col].fillna("")
        return df
    return pd.DataFrame()

# ==============================
# 🖼️ Carregamento de imagens
# ==============================
@st.cache_data
def load_image(path: Path):
    try:
        return Image.open(path)
    except Exception:
        return None


#  Execução principal
df = load_data()
if df.empty:
    st.warning("Adicione `assets/portfolio.csv` com colunas: titulo, cliente, ano, setor, tags, imagem, descricao, abordagem, resultados.")
else:
    # --------------------------
    # 🎛️ Filtros
    # --------------------------
    c1, c2, c3 = st.columns(3)
    ano = c1.selectbox("Ano", options=["Todos"] + sorted([str(a) for a in df["ano"].dropna().unique()]))
    setor = c2.selectbox("Setor", options=["Todos"] + sorted(df["setor"].dropna().unique()))
    tag = c3.selectbox("Tag", options=["Todas"] + sorted({t.strip() for ts in df["tags"].dropna() for t in str(ts).split(",")}))

    def filt(row):
        ok = True
        if ano != "Todos": ok &= str(row["ano"]) == ano
        if setor != "Todos": ok &= str(row["setor"]) == setor
        if tag != "Todas": ok &= tag in str(row["tags"])
        return ok

    view = df[df.apply(filt, axis=1)].reset_index(drop=True)
    st.caption(f"{len(view)} projeto(s) encontrado(s).")

    # --------------------------
    # 🧱 Layout dos cards
    # --------------------------
    cols_per_row = st.slider("Colunas", min_value=2, max_value=4, value=2)
    cols = st.columns(cols_per_row, gap="medium")

    for i, row in view.iterrows():
        col = cols[i % cols_per_row]
        with col:
            with st.container(border=True):
                # --------------------------
                # 🖼️ Imagem do projeto
                # --------------------------
                raw_path = IMG_DIR / row["imagem"]
                img_path = Path(os.path.normpath(os.path.abspath(str(raw_path))))
                exists = os.path.exists(img_path)

                # st.write("DEBUG IMG:", img_path, exists)  # deixe ativo se quiser testar

                img = load_image(img_path) if exists else None
                if img:
                    st.image(img, use_container_width=True)
                else:
                    st.info("📷 Imagem não encontrada")

                # --------------------------
                # 🧾 Texto e resumo
                # --------------------------
                st.markdown(f"### {row['titulo']}")
                st.caption(f"**{row['cliente']} ({row['ano']})**")
                st.caption(f"Setor: {row['setor']} • Tags: {row['tags']}")

                with st.expander("Resumo"):
                    st.markdown(f"**Desafio:** {row.get('descricao','')}")
                    st.markdown(f"**Resultado:** {row.get('resultados','')}")
