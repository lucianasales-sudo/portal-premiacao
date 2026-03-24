import streamlit as st
import pandas as pd

# 1. Configuração (Deve ser o primeiro comando st)
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

# 2. Carregamento de Dados (Agora com st definido)
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

        # Busca coluna de Matrícula dinamicamente
        m1 = [c for c in d1.columns if 'MATRIC' in c]
        k1 = m1[0] if m1 else d1.columns[0]
        m2 = [c for c in d2.columns if 'MATRIC' in c]
        k2 = m2[0] if m2 else d2.columns[0]

        # Padroniza nomes e chaves
        d1 = d1.rename(columns={
            k1: 'MATRÍCULA',
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
        d2 = d2.rename(columns={k2: 'MATRÍCULA'})
        
        d1['MATRÍCULA'] = d1['MATRÍCULA'].astype(str).str.strip()
        d2['MATRÍCULA'] = d2['MATRÍCULA'].astype(str).str.strip()
        
        return pd.merge(d1, d2, on='MATRÍCULA', how='left')
    except Exception as e:
        st.error(f"Erro nos arquivos: {e}")
        return None

df = load()

# 3. Interface
if df is not None:
    st.header("🏆 PAINEL PREMIAÇÃO")
    st.divider()
    
    c_l, c_d = st.columns(2)
    with c_l:
        u_in = st.text_input("MATRÍCULA:", placeholder="Digite...")
    
    if u_in:
        u_df = df[df['MATRÍCULA'] == u_in.strip()]
        
        if not u_df.empty:
            r = u_df.iloc[0]
            nome_p = str(r.get('NOME', 'Colaborador')).split()[0]
            st.subheader(f"Olá, {nome_p}! 👋")
            
            with c_d:
                m_s = st.selectbox("MÊS:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_s].iloc[0]
            
            # Textos curtos (Anti-Quebra)
            t_p, t_m, t_at, t_pr = "Perf:", "Medalha:", "Ating:",
