import streamlit as st
import pandas as pd

# 1. Configuração Inicial
st.set_page_config(page_title="PAINEL PREMIAÇÃO", layout="wide")
st.header("🏆 PAINEL PREMIAÇÃO")

# Funções de Formatação
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','R$ -']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_pc(v):
    try:
        # Limpa string de porcentagem
        s = str(v).replace('%','').replace(',','.')
        n = float(s)
        return f"{int(n)}%"
    except: return "0%"

# 2. Carregamento de Dados
@st.cache_data
def load():
    try:
        # Leitura dos arquivos
        try: 
            d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: 
            d1 = pd.read_csv("dados.csv", sep=',', encoding='utf-8')
        
        try: 
            d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        except: 
            d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=',', encoding='utf-8')

        # Padroniza colunas para maiúsculo
        d1.columns = [c.strip().upper() for c in d1.columns]
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Mapeamento de nomes (De acordo com o seu arquivo enviado)
        m = {}
        m['PRODUTIVIDADE ADERENCIA ROTEIRO'] = 'A1'
        m['PREMIAÇÃO ADERENCIA ROTEIRO'] = 'A2'
        m['MEDALHA LOJA DO CORAÇÃO'] = 'L1'
        m['PREMIAÇÃO MEDALHA LC'] = 'L2'
        m['AING SELLOUT %'] = 'S3'
        m['PREMIAÇÃO SELLOUT'] = 'S4'
        m['TOTAL A RECEBER'] = 'TOT'
        m['PONTO EXTRA'] = 'P1'
        m['PONTO NATURAL'] = 'P2'
        m['RUPTURA'] = 'P3'
        m['MPDV'] = 'P4'
        m['MÃŠS'] = 'MÊS' # Correção de encoding comum
        
        d1 = d1.rename(columns=m)

        # Busca segura da Matrícula (Evita IndexError
