import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

st.set_page_config(layout="wide")
st.title("Dashboard de Desempenho — Motorista de Aplicativo")
st.caption("Análise automática de ganhos, distância e eficiência por dia e período. Este dashboard é atualizado em tempo real a partir dos dados de uma planilha real do Google Sheets criada e compartilhada por um profissional que trabalha como motorista de app em suas hora vagas.")

# ==================================
# 1️⃣ Carregar dados do Google Sheets
# ==================================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1wKIjN01fpPoXZvWG_HKQLLyIvNJ8XZLP7r2dC_BcBwY/export?format=csv"
    df = pd.read_csv(url, decimal=",")
    df.columns = df.columns.str.strip()
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

    # Conversão segura das colunas numéricas
    num_cols = [
        "Km Inicial", "Km Final", "Total de Km", "Preço Combustivel no dia","Ganho Bruto (R$)",
        "Gasto combustível", "Ganho líquido", "Taxa de lucro", "R$/Km"
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("R$", "", regex=False)
                .str.replace("%", "", regex=False)
                .str.replace(" ", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Se a taxa de lucro estiver em formato 0–100, converte para 0–1
    if "Taxa de lucro" in df.columns:
        mask = df["Taxa de lucro"] > 1.0
        df.loc[mask, "Taxa de lucro"] = df.loc[mask, "Taxa de lucro"] / 100.0

    # Padronizar texto em colunas de texto
    for col in ("Dia", "Período"):
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    return df

df = load_data()

if df.empty:
    st.error("❌ Erro ao carregar os dados. Verifique o link do Google Sheets.")
    st.stop()

# ==================================
# 2️⃣ Filtros
# ==================================
st.sidebar.header("Filtros")

# Filtro por período (Manhã, Tarde, Noite)
periodos = ["(Todos)"] + sorted(df["Período"].dropna().unique().tolist())
periodo_sel = st.sidebar.selectbox("Período", periodos)

# Filtro por dia da semana
dias = ["(Todos)"] + sorted(df["Dia"].dropna().unique().tolist())
dia_sel = st.sidebar.selectbox("Dia da Semana", dias)

# Filtro por intervalo de datas
min_date, max_date = df["Data"].min(), df["Data"].max()
date_range = st.sidebar.date_input(
    "Intervalo de Datas",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date,
)

# ✅ Validação do intervalo de datas
if not date_range or len(date_range) < 2 or any(d is None for d in date_range):
    st.warning("⚠️ Selecione **tanto a data inicial quanto a final** para aplicar o filtro de período.")
    st.stop()

# Extrair início e fim do intervalo
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

if start_date > end_date:
    st.error("❌ A data inicial não pode ser posterior à data final.")
    st.stop()


# Aplicar filtros
mask = (df["Data"] >= pd.to_datetime(date_range[0])) & (df["Data"] <= pd.to_datetime(date_range[1]))
if periodo_sel != "(Todos)":
    mask &= df["Período"] == periodo_sel
if dia_sel != "(Todos)":
    mask &= df["Dia"] == dia_sel

df_filtered = df.loc[mask].copy()

# ==================================
# 3️⃣ Métricas principais (KPIs)
# ==================================

st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #0072B2;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.5rem;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

col0, col1, col2, col3, col4, col5 = st.columns(6)

col0.metric("Dias Trabalhados", f"{df_filtered['Data'].nunique()} dias")
col1.metric("Total de Km", f"{df_filtered['Total de Km'].sum():,.0f} km")
col2.metric("Gasto com Combust.", f"R$ {df_filtered['Gasto combustível'].sum():,.2f}")
col3.metric("Ganho Bruto Total", f"R$ {df_filtered['Ganho Bruto (R$)'].sum():,.2f}")
col4.metric("Ganho Líquido Total", f"R$ {df_filtered['Ganho líquido'].sum():,.2f}")
col5.metric("Taxa Média de Lucro", f"{df_filtered['Taxa de lucro'].mean() * 100:.1f}%")

st.divider()

# ==================================
# 4️⃣ Gráficos
# ==================================
st.subheader("📈 Visualizações")

# Cria duas colunas
col1, col2 = st.columns(2)

# Garantir que "Data" seja datetime válido
df_filtered["Data"] = pd.to_datetime(df_filtered["Data"], errors="coerce")
df_filtered = df_filtered.dropna(subset=["Data"])

# ---- Gráfico 1 — Ganho líquido por dia ----
# ---- Gráfico 1 — Ganho líquido por dia ----
with col1:
    df_filtered["Data"] = pd.to_datetime(df_filtered["Data"], errors="coerce")
    df_filtered = df_filtered.dropna(subset=["Data"])

    dados_dia = df_filtered.groupby("Data")["Ganho líquido"].sum().reset_index()

    fig1, ax1 = plt.subplots()
    ax1.bar(dados_dia["Data"], dados_dia["Ganho líquido"], color="#1f77b4")
    ax1.set_title("Ganho Líquido por Dia")
    ax1.set_ylabel("R$")
    ax1.set_xlabel("")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig1)


# ---- Gráfico 2 — Total de Km por dia ----
with col2:
    fig2, ax2 = plt.subplots()
    df_filtered.groupby("Data")["Total de Km"].sum().plot(kind="line", marker="o", ax=ax2, color="#2ca02c")
    ax2.set_title("Distância Percorrida por Dia")
    ax2.set_ylabel("Km")
    ax2.set_xlabel("")
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
    plt.tight_layout()
    st.pyplot(fig2)

# Segunda linha de gráficos
col3, col4 = st.columns(2)

# ---- Gráfico 3 — Ganho líquido médio por dia da semana ----
with col3:
    fig3, ax3 = plt.subplots()
    df_filtered.groupby("Dia")["Ganho líquido"].mean().reindex(
        ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    ).plot(kind="bar", color="#ff7f0e", ax=ax3)
    ax3.set_title("Média de Ganho Líquido por Dia da Semana")
    ax3.set_ylabel("R$")
    ax3.set_xlabel("")
    plt.tight_layout()
    st.pyplot(fig3)

# ---- Gráfico 4 — R$/Km médio por período ----
with col4:
    fig4, ax4 = plt.subplots()
    df_filtered.groupby("Período")["R$/Km"].mean().plot(kind="barh", color="#9467bd", ax=ax4)
    ax4.set_title("Rentabilidade Média (R$/Km) por Período")
    ax4.set_xlabel("R$/Km")
    ax4.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig4)

# ---- Gráfico 5 — Relação entre distância e ganho líquido (linha separada) ----
st.markdown("### ⚖️ Correlação: Distância vs Ganho Líquido")
fig5, ax5 = plt.subplots()
ax5.scatter(df_filtered["Total de Km"], df_filtered["Ganho líquido"], alpha=0.7, color="#d62728")
ax5.set_xlabel("Total de Km")
ax5.set_ylabel("Ganho Líquido (R$)")
ax5.grid(True)
st.pyplot(fig5)


# ==================================
# 5️⃣ Rodapé
# ==================================
st.markdown("---")
st.caption("Fonte: Google Sheets — Atualizado automaticamente.")
