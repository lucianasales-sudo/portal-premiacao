import streamlit as st
import pandas as pd

# 1. Configurações Iniciais
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação Curtas (Evitam quebras de linha)
def f_rs(v):
    if pd.isna(v) or str(v) in ['0','0,00','-','nan']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-','nan']: return "0"
    l = str(v).replace('R','').replace('$','').strip()
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
        df = pd.read_csv("dados.csv", encoding='utf-8')
    except:
        df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
    df.columns = [c.strip().upper() for c in df.columns]
    return df

df = load()

if df is not None:
    # Título centralizado usando header nativo
    st.header("🏆 Portal de Premiação", divider="gray")
    
    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()
    
    # Login Centralizado
    _, col_l, _ = st.columns([1, 1, 1])
    with col_l:
        acesso = st.text_input("MATRÍCULA:", placeholder="Digite aqui...")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            c_n = [c for c in df.columns if 'NOME' in c][0]
            st.subheader(f"Olá, {u_df.iloc[0][c_n]}! 👋")
            
            u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
            _, col_m, _ = st.columns([1, 1, 1])
            with col_m:
                m_sel = st.selectbox("Selecione o Mês:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            # --- ÁREA DE INDICADORES ---
            st.write("### 📊 Seus Indicadores")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("**🎯 ADERÊNCIA**")
                    st.metric("Performance", f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.write(f"💰 Prêmio: **{f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
            
            with c2:
                with st.container(border=True):
                    st.write("**🏪 LOJA DO CORAÇÃO**")
                    st.metric("Medalha", str(r.get('MEDALHA LOJA DO CORAÇÃO', '-')))
                    st.write(f"💰 Prêmio: **{f_rs(r.get('PREMIAÇÃO MEDALHA LC', 0))}**")
