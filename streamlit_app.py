import streamlit as st
import pandas as pd

# 1. Configurações e Título da Guia
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação (Mantidas para segurança dos dados)
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','nan']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
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

# 2. Carregamento
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
    # --- HEADER DESIGN ---
    # Centralizando o cabeçalho em uma coluna estreita para elegância
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.write("") 
        st.markdown("<h1 style='text-align: center;'>🏆 Portal de Premiação</h1>", unsafe_allow_input_html=True)
        st.divider()

        # Login e Mês agrupados em um mini-card
        with st.container(border=True):
            c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
            df[c_mat] = df[c_mat].astype(str).str.strip()
            
            acesso = st.text_input("IDENTIFICAÇÃO (MATRÍCULA):", placeholder="Ex: 1-49174")
            
            if acesso:
                u_df = df[df[c_mat] == acesso.strip()]
                if not u_df.empty:
                    u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
                    m_sel = st.selectbox("REFERÊNCIA:", u_df['MÊS'].unique())
                    r = u_df[u_df['MÊS'] == m_sel].iloc[0]
                else:
                    st.error("Matrícula não localizada.")
                    st.stop()
            else:
                st.info("Aguardando login...")
                st.stop()

    # --- ÁREA DE RESULTADOS ---
    st.write("")
    col_n = [c for c in df.columns if 'NOME' in c][0]
    st.markdown(f"<h3 style='text-align: center;'>Olá, {u_df.iloc[0][col_n]}! 👋</h3>", unsafe_allow_input_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Confira abaixo seu desempenho e premiações</p>", unsafe_allow_input_html=True)
    
    # Criando colunas de respiro para os indicadores não ficarem esticados
    _, body_col, _ = st.columns([0.2, 5, 0.2])
    
    with body_col:
        st.write("#### 📊 Seus Indicadores")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            with st.container(border=True):
                st.markdown("<p style='text-align: center; font-weight: bold;'>🎯 ADERÊNCIA</p>", unsafe_allow_input_html=True)
                st.metric("Performance", f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)), help="Aderência ao roteiro planejado")
                st.markdown(f"<p style='text-align: center; color: #28a745; font-size: 18px;'><b>{f_rs(r.get('PREMIA
