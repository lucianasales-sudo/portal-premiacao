import streamlit as st
import pandas as pd

# 1. Configurações
st.set_page_config(page_title="PAINEL PREMIAÇÃO", layout="wide", page_icon="☕")

# Funções de Formatação
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','nan']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-','nan']: return "0"
    return str(v).replace('R','').replace('$','').strip()

def f_pc(v):
    try:
        n = float(str(v).replace('%','').replace(',','.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Carregamento de Dados (2 Arquivos)
@st.cache_data
def load_data():
    try:
        # Base Principal
        try: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        except: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        d1.columns = [c.strip().upper() for c in d1.columns]

        # Base Secundária
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Mapeamento para nomes curtos (Evita SyntaxError)
        d1 = d1.rename(columns={
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'AD_P',
            'PREMIAÇÃO ADERENCIA ROTEIRO': 'AD_V',
            'MEDALHA LOJA DO CORAÇÃO': 'LC_M',
            'PREMIAÇÃO MEDALHA LC': 'LC_V',
            'META SELLOUT': 'SO_M',
            'REAL SELLOUT': 'SO_R',
            'AING SELLOUT %': 'SO_A',
            'PREMIAÇÃO SELLOUT': 'SO_V',
            'TOTAL A RECEBER': 'TOTAL'
        })

        c1 = 'MATRÍCULA' if '
