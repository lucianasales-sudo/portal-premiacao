import streamlit as st
import pandas as pd

# 1. Configurações e Estética
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação Seguras
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','nan']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-','nan']: return "0"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return l

def f_pc(v):
    try:
        n = float(str(v).replace('%','').replace(',','.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Carregamento de Dados
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
    # --- LAYOUT CENTRALIZADO ---
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        st.write("") 
        st.markdown("<h1 style='text-align: center;'>🏆 Portal de Premiação</h1>", unsafe_allow_input_html=True)
        st.divider()

        # Caixa de Acesso
        with st.container(border=True):
            c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
            df[c_mat] = df[c_mat].astype(str).str.strip()
            acesso = st.text_input("IDENTIFICAÇÃO:", placeholder="Sua matrícula aqui")
            
            if acesso:
                u_df = df[df[c_mat] == acesso.strip()]
                if not u_df.empty:
                    u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
                    m_sel = st.selectbox("MÊS DE REFERÊNCIA:", u_df['MÊS'].unique())
                    r = u_df[u_df['MÊS'] == m_sel].iloc[0]
                else:
                    st.error("Matrícula não encontrada.")
                    st.stop()
            else:
                st.info("Digite sua matrícula para visualizar.")
                st.stop()

    # --- ÁREA DE RESULTADOS ---
    st.write("")
    c_n = [c for c in df.columns if 'NOME' in c][0]
    st.markdown(f"<h2 style='text-align: center;'>Olá, {u_df.iloc[0][c_n]}! 👋</h2>", unsafe_allow_input
