import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# --- CSS PARA CENTRALIZAÇÃO TOTAL ---
st.markdown("""
    <style>
    .stMetric { display: flex; flex-direction: column; align-items: center; text-align: center; }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { text-align: center !important; width: 100%; }
    .centralizar { text-align: center; width: 100%; display: block; margin-bottom: 5px; }
    .premio-texto { color: #28a745; font-weight: bold; text-align: center; width: 100%; display: block; }
    </style>
    """, unsafe_allow_input_html=True)

# Funções de Formatação
def f_reais(v):
    if pd.isna(v) or str(v).strip() in ['-', '', '0', '0,00', 'nan']: return "R$ 0,00"
    l = str(v).replace('R', '').replace('$', '').replace('S', '').strip()
    return f"R$ {l}"

def f_num(v):
    if pd.isna(v) or str(v).strip() in ['-', '', 'nan', '0']: return "0"
    l = str(v).replace('R', '').replace('$', '').replace('S', '').replace('.', '').replace(',', '.').strip()
    try:
        n = float(l)
        return f"{n:,.0f}".replace(',', '.')
    except: return str(v).strip()

def f_pct(v):
    try:
        n = float(str(v).replace('%', '').replace(',', '.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Carregamento de Dados
@st.cache_data
def carregar():
    try:
        try: df = pd.read_csv("dados.csv", encoding='utf-8')
        except: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except: return None

df = carregar()

if df is not None:
    st.markdown("<h1 class='centralizar'>🏆 Portal de Premiação</h1>", unsafe_allow_input_html=True)
    st.divider()

    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()

    with st.sidebar:
        st.header("🔑 Acesso")
        acesso = st.text_input("MATRÍCULA:", placeholder="
