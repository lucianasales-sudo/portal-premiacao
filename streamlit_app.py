import streamlit as st
import pandas as pd

# 1. Configurações
st.set_page_config(page_title="PAINEL PREMIAÇÃO", layout="wide", page_icon="☕")

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

# 2. Carregamento de Dados
@st.cache_data
def load_data():
    try:
        try: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        except: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        d1.columns = [c.strip().upper() for c in d1.columns]

        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Mapeamento Siglas
        d1 = d1.rename(columns={
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'A1',
            'PREMIAÇÃO ADERENCIA ROTEIRO': 'A2',
            'MEDALHA LOJA DO CORAÇÃO': 'L1',
            'PREMIAÇÃO MEDALHA LC': 'L2',
            'META SELLOUT': 'S1',
            'REAL SELLOUT': 'S2',
            'AING SELLOUT %': 'S3',
            'PREMIAÇÃO SELLOUT': 'S4',
            'TOTAL A RECEBER': 'TOT',
            'PONTO EXTRA': 'P1',
            'PONTO NATURAL': 'P2',
            'RUPTURA': 'P3',
            'MPDV': 'P4'
        })
        
        c_k = [c for c in d1.columns if 'MATRIC' in c][0]
        d1 = d1.rename(columns={c_k: 'ID'})
        
        c_k2 = [c for c in d2.columns if 'MATRIC' in c][0]
        d2 = d2.rename(columns={c_k2: 'ID'})
        
        d1.ID = d1.ID.astype(str).str.strip()
        d2.ID = d2.ID.astype(str).str.strip()
        
        return pd.merge(d1, d2, on='ID', how='left')
    except Exception as e: # Corrigido: adicionado os dois pontos aqui
        st.error(f"Erro: {e}")
        return None

df = load_data()

if df is not None:
    st.header("🏆 PAINEL PREMIAÇÃO")
    st.divider()

    acesso = st.text_input("MATRÍCULA:", placeholder="Ex: 1-4
