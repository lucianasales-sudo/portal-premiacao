import streamlit as st
import pandas as pd

# 1. Configurações de Design
st.set_page_config(page_title="PAINEL PREMIAÇÃO", layout="wide", page_icon="☕")

# Funções de Formatação
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

# 2. Carregamento de Dados (Lógica para 2 arquivos)
@st.cache_data
def load_data():
    try:
        # Carrega Planilha Principal (Premiação)
        try: df1 = pd.read_csv("dados.csv", encoding='utf-8')
        except: df1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df1.columns = [c.strip().upper() for c in df1.columns]

        # Carrega Planilha Secundária (Abertura LC)
        try: df2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')
        except: df2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        df2.columns = [c.strip().upper() for c in df2.columns]

        # Garante que a coluna de união seja STRING e esteja limpa
        c_mat1 = 'MATRÍCULA' if 'MATRÍCULA' in df1.columns else df1.columns[0]
        c_mat2 = 'MATRÍCULA' if 'MATRÍCULA' in df2.columns else df2.columns[0]
        
        df1[c_mat1] = df1[c_mat1].astype(str).str.strip()
        df2[c_mat2] = df2[c_mat2].astype(str).str.strip()

        # UNE AS DUAS PLANILHAS (Merge)
        # O 'left' garante que todos da planilha de prêmios apareçam, mesmo sem dados na LC
        df_final = pd.merge(df1, df2, left_on=c_mat1, right_on=c_mat2, how='left', suffixes=('', '_LC'))
        
        return df_final
    except Exception as e:
        st.error(f"Erro ao carregar arquivos: {e}")
        return None

df = load_data()

if df is not None:
    # --- CABEÇALHO ---
    st.header("🏆 PAINEL PREMIAÇÃO")
    st.divider()

    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    
    col_l, col_m = st.columns(2)
    with col_l:
        acesso = st.text_input("MATRÍCULA:", placeholder="Ex: 1-49174")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            nome_col = [c for c in df.columns if 'NOME' in c][0]
            p_nome = str(u_df.iloc[0][nome_col]).split()[0]
            st.subheader(f"Olá, {p_nome}! 👋")
            
            with col_m:
                u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
                m_sel = st.selectbox("MÊS:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            st.write("### Indicadores")
            
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("🎯 **ADERÊNCIA**")
                    st.write(f"Performance: **{f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
            
            with c2:
                with st.container(border=True):
                    st.write("🏪 **LOJA DO CORAÇÃO**")
                    med = str(r.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                    st.write(f"Medalha: **{med}
