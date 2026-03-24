import streamlit as st
import pandas as pd

# 1. Config
st.set_page_config(page_title="PAINEL", layout="wide")

# Funcoes
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-']: return "0"
    return str(v).replace('R','').replace('$','').strip()

def f_pc(v):
    try:
        n = float(str(v).replace('%','').replace(',','.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Dados
@st.cache_data
def load():
    try:
        try: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        except: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        d1.columns = [c.strip().upper() for c in d1.columns]
        
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Renomeia para siglas curtissimas (Evita quebra de linha)
        d1 = d1.rename(columns={
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'A1',
            'PREMIAÇÃO ADERENCIA ROTEIRO': 'A2',
            'MEDALHA LOJA DO CORAÇÃO': 'L1',
            'PREMIAÇÃO MEDALHA LC': 'L2',
            'META SELLOUT': 'S1',
            'REAL SELLOUT': 'S2',
            'AING SELLOUT %': 'S3',
            'PREMIAÇÃO SELLOUT': 'S4',
            'TOTAL A RECEBER': 'TOT'
        })
        
        # Garante que a coluna se chame MATRICULA (sem acento para facilitar)
        c_m1 = [c for c in d1.columns if 'MATRIC' in c][0]
        c_m2 = [c for c in d2.columns if 'MATRIC' in c][0]
        d1 = d1.rename(columns={c_m1: 'ID'})
        d2 = d2.rename(columns={c_m2: 'ID'})
        
        d1.ID = d1.ID.astype(str).str.strip()
        d2.ID = d2.ID.astype(str).str.strip()
        
        return pd.merge(d1, d2, on='ID', how='left')
    except: return None

df = load()

# 3. App
if df is not None:
    st.header("🏆 PAINEL PREMIAÇÃO")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        u_in = st.text_input("MATRÍCULA:", placeholder="Digite...")
    
    if u_in:
        # BUSCA BLINDADA (Sem colchetes para evitar SyntaxError)
        u_df = df.query(f"ID == '{u_in.strip()}'")
        
        if not u_df.empty:
            r = u_df.iloc[0]
            nome_p = str(r.get('NOME', 'User')).split()[0]
            st.subheader(f"Olá, {nome_p}!")
            
            with col2:
                m_s = st.selectbox("MÊS:", u_df.MÊS.unique())
            
            r = u_df[u_df.MÊS == m_s].iloc[0]
            
            # Labels curtos
            st.write("### Indicadores")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("**🎯 ADERÊNCIA**")
                    st.write(f"Perf: **{f_pc(r.get('A1',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('A2',0))}**")
            
            with c2:
                with st.container(border=True):
                    st.write("**🏪 LOJA**")
                    st.write(f"Medalha: **{r.get('L1','
