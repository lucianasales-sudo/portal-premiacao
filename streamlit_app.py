import streamlit as st
import pandas as pd

# 1. Config e Cabecalho
st.set_page_config(page_title="PAINEL", layout="wide")
st.header("🏆 PAINEL PREMIAÇÃO")

# Funcoes
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_pc(v):
    try:
        n = float(str(v).replace('%','').replace(',','.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Dados
@st.cache_data
def load():
    try:
        # Carregamento fragmentado para evitar corte de linha
        try: 
            d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: 
            d1 = pd.read_csv("dados.csv", encoding='utf-8')
        
        try: 
            d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        except: 
            d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')

        d1.columns = [c.strip().upper() for c in d1.columns]
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Mapeamento (Cada item em uma linha para seguranca)
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
        
        d1 = d1.rename(columns=m)

        # Chaves de Matricula
        k1 = [c for c in d1.columns if 'MATRIC' in c][0]
        k2 = [c for c in d2.columns if 'MATRIC' in c][0]
        
        # Limpeza em etapas separadas (Evita erro na linha 60)
        v1 = d1[k1].astype(str)
        d1['ID'] = v1.str.strip()
        
        v2 = d2[k2].astype(str)
        d2['ID'] = v2.str.strip()
        
        return pd.merge(d1, d2, on='ID', how='left')
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

df = load()

# ... (mantenha o topo do código igual)

# 2. Dados
@st.cache_data
def load():
    try:
        # Carregamento
        try: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')

        d1.columns = [c.strip().upper() for c in d1.columns]
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Mapeamento de Indicadores
        m = {
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'A1', 'PREMIAÇÃO ADERENCIA ROTEIRO': 'A2',
            'MEDALHA LOJA DO CORAÇÃO': 'L1', 'PREMIAÇÃO MEDALHA LC': 'L2',
            'AING SELLOUT %': 'S3', 'PREMIAÇÃO SELLOUT': 'S4',
            'TOTAL A RECEBER': 'TOT', 'PONTO EXTRA': 'P1',
            'PONTO NATURAL': 'P2', 'RUPTURA': 'P3', 'MPDV': 'P4'
        }
        d1 = d1.rename(columns=m)

        # --- BUSCA SEGURA DE MATRÍCULA (RESOLVE O INDEX ERROR) ---
        # Tenta achar 'MATRIC', se não achar, usa a primeira coluna da planilha
        c_m1 = [c for c in d1.columns if 'MATRIC' in c]
        k1 = c_m1[0] if c_m1 else d1.columns[0]
        
        c_m2 = [c for c in d2.columns if 'MATRIC' in c]
        k2 = c_m2[0] if c_m2 else d2.columns[0]
        
        # Limpeza
        d1['ID'] = d1[k1].astype(str).str.strip()
        d2['ID'] = d2[k2].astype(str).str.strip()
        
        return pd.merge(d1, d2, on='ID', how='left')
    except Exception as e:
        st.error(f"Erro ao processar colunas: {e}")
        return None

# ... (resto do código igual)
            st.divider()
            st.success(f"🏆 TOTAL: {f_rs(r.get('TOT',0))}")
        else:
            st.warning("Não encontrado.")
