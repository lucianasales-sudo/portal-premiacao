import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# --- CSS PARA CENTRALIZAÇÃO TOTAL ---
st.markdown("""
    <style>
    .stMetric { display: flex; flex-direction: column; align-items: center; text-align: center; }
    [data-testid="stMetricValue"] { text-align: center !important; width: 100%; }
    [data-testid="stMetricLabel"] { text-align: center !important; width: 100%; }
    .centralizar { text-align: center; width: 100%; display: block; }
    </style>
    """, unsafe_allow_input_html=True)

# Funções de Formatação Seguras
def f_reais(v):
    if pd.isna(v) or str(v).strip() in ['-', '', '0', '0,00', 'nan']: return "R$ 0,00"
    limpo = str(v).replace('R', '').replace('$', '').replace('S', '').strip()
    return f"R$ {limpo}"

def f_num(v):
    if pd.isna(v) or str(v).strip() in ['-', '', 'nan', '0']: return "0"
    limpo = str(v).replace('R', '').replace('$', '').replace('S', '').replace('.', '').replace(',', '.').strip()
    try:
        n = float(limpo)
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

    # Login
    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        with st.container(border=True):
            st.markdown("<h3 class='centralizar'>🔑 Acesso Restrito</h3>", unsafe_allow_input_html=True)
            acesso = st.text_input("👤 MATRÍCULA:", placeholder="Ex: 1-46532")
    
    if acesso:
        acesso = acesso.strip()
        user_df = df[df[c_mat] == acesso]
        
        if not user_df.empty:
            nome = user_df.iloc[0][[c for c in df.columns if 'NOME' in c][0]]
            st.markdown(f"<h2 class='centralizar'>Olá, {nome}! 👋</h2>", unsafe_allow_input_html=True)
            
            user_df['MÊS'] = user_df['MÊS'].astype(str).str.strip().str.upper()
            _, col_m, _ = st.columns([1, 1, 1])
            with col_m:
                m_sel = st.selectbox("📅 Selecione o mês:", user_df['MÊS'].unique())
            
            row = user_df[user_df['MÊS'] == m_sel].iloc[0]
            st.markdown("<h3 class='centralizar'>📊 Seus Indicadores</h3>", unsafe_allow_input_html=True)
            
            # --- CARDS CENTRALIZADOS ---
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.markdown("<b class='centralizar'>🎯 ADERÊNCIA</b>", unsafe_allow_input_html=True)
                    st.metric(label="Performance", value=f_pct(row.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.markdown(f"<p class='centralizar'>💰 Prêmio: <b>{f_reais(row.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}</b></p>", unsafe_allow_input_html=True)
            
            with c2:
                with st.container(border=True):
                    st.markdown("<b class='centralizar'>🏪 LOJA DO CORAÇÃO</b>", unsafe_allow_input_html=True)
                    med = str(row.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                    st.metric(label="Medalha", value=med)
                    st.markdown(f"<p class='centralizar'>💰 Prêmio: <b>{f_reais(row.get('PREMIAÇÃO MEDALHA LC',
