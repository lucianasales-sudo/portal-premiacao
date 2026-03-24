import streamlit as st
import pandas as pd

# 1. Configurações de Design
st.set_page_config(page_title="PAINEL PREMIAÇÃO", layout="wide", page_icon="☕")

# Funções de Formatação Seguras
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

# 2. Carregamento de Dados (2 Arquivos)
@st.cache_data
def load_data():
    try:
        # Carrega Base de Prêmios
        try: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        except: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        d1.columns = [c.strip().upper() for c in d1.columns]

        # Carrega Base de Abertura LC
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Chaves de união
        c1 = 'MATRÍCULA' if 'MATRÍCULA' in d1.columns else d1.columns[0]
        c2 = 'MATRÍCULA' if 'MATRÍCULA' in d2.columns else d2.columns[0]
        
        d1[c1] = d1[c1].astype(str).str.strip()
        d2[c2] = d2[c2].astype(str).str.strip()

        # Une as planilhas
        return pd.merge(d1, d2, left_on=c1, right_on=c2, how='left', suffixes=('','_LC'))
    except: return None

df = load_data()

if df is not None:
    st.header("🏆 PAINEL PREMIAÇÃO")
    st.divider()

    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    
    col_l, col_m = st.columns(2)
    with col_l:
        acesso = st.text_input("MATRÍCULA:", placeholder="Ex: 1-49174")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            nome_c = [c for c in df.columns if 'NOME' in c][0]
            p_nome = str(u_df.iloc[0][nome_c]).split()[0]
            st.subheader(f"Olá, {p_nome}! 👋")
            
            with col_m:
                u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
                m_sel = st.selectbox("MÊS:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            # --- VARIÁVEIS CURTAS (Blindagem contra SyntaxError) ---
            val_ad_p = f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0))
            val_ad_v = f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))
            
            val_lc_m = str(r.get('MEDALHA LOJA DO CORAÇÃO', '-'))
            val_lc_v = f_rs(r.get('PREMIAÇÃO MEDALHA LC', 0))
            
            # Exemplo de dado vindo da SEGUNDA PLANILHA (BASE ABERTURA LC)
            # Substitua 'COLUNA_DA_BASE_LC' pelo nome real da coluna que quer mostrar
            extra_lc = str(r.get('STATUS', 'Sem info')) 

            val_so_m = f_nm(r.get('META SELLOUT', 0))
            val_so_r = f_nm(r.get('REAL SELLOUT', 0))
            val_so_a = f_pc(r.get('AING SELLOUT %', 0))
            val_so_v = f_rs(r.get('PREMIAÇÃO SELLOUT', 0))
            
            val_total = f_rs(r.get('TOTAL A
