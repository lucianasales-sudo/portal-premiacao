import streamlit as st
import pandas as pd

# 1. Configuração inicial (DEVE ser a primeira linha de comando st)
st.set_page_config(page_title="PAINEL", layout="wide")

# Funções de Formatação
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

# 2. Carregamento de Dados (Agora com st definido antes)
@st.cache_data
def load():
    try:
        # Carrega dados.csv
        try: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        except: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        d1.columns = [c.strip().upper() for c in d1.columns]
        
        # Carrega BASE ABERTURA LC.csv
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Siglas curtas para evitar quebras de linha
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
        
        k = 'MATRÍCULA'
        d1[k] = d1[k].astype(str).str.strip()
        d2[k] = d2[k].astype(str).str.strip()
        
        return pd.merge(d1, d2, on=k, how='left')
    except Exception as e:
        st.error(f"Erro no carregamento: {e}")
        return None

df = load()

# 3. Interface
if df is not None:
    st.header("🏆 PAINEL PREMIAÇÃO")
    st.divider()
    
    col_e, col_d = st.columns(2)
    with col_e:
        u_in = st.text_input("MATRÍCULA:", placeholder="Digite...")
    
    if u_in:
        u_df = df[df['MATRÍCULA'] == u_in.strip()]
        
        if not u_df.empty:
            r = u_df.iloc[0]
            nome_p = str(r.get('NOME', 'Colaborador')).split()[0]
            st
