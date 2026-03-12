import streamlit as st
import pandas as pd

# 1. Configurações
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# CSS para Centralização Total
st.markdown("""
    <style>
    .stMetric { display: flex; flex-direction: column; align-items: center; text-align: center; }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { text-align: center !important; width: 100%; }
    .central { text-align: center; width: 100%; display: block; }
    .pr-txt { color: #28a745; font-weight: bold; text-align: center; width: 100%; display: block; }
    </style>
    """, unsafe_allow_input_html=True)

# Funções de Formato
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['-', '', '0', '0,00', 'nan']: return "R$ 0,00"
    l = str(v).replace('R', '').replace('$', '').replace('S', '').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v).strip() in ['-', '', 'nan', '0']: return "0"
    l = str(v).replace('R', '').replace('$', '').replace('S', '').replace('.', '').replace(',', '.').strip()
    try:
        n = float(l)
        return f"{n:,.0f}".replace(',', '.')
    except: return str(v).strip()

def f_pc(v):
    try:
        n = float(str(v).replace('%', '').replace(',', '.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Dados
@st.cache_data
def load():
    try:
        try: df = pd.read_csv("dados.csv", encoding='utf-8')
        except: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except: return None

df = load()

if df is not None:
    st.markdown("<h1 class='central'>🏆 Portal de Premiação</h1>", unsafe_allow_input_html=True)
    st.divider()

    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()

    # Login Centralizado (Conforme desenho)
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        acesso = st.text_input("MATRÍCULA:", placeholder="Ex: 1-46532")
    
    if acesso:
        u_df = df[df[c_
