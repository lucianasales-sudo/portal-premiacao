import streamlit as st
import pandas as pd

# 1. Configurações de Design
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação Seguras
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-']: return "0"
    return str(v).replace('R','').replace('$','').strip()

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
    # --- CABEÇALHO ---
    st.markdown("<h1 style='text-align:center;'>🏆 Portal de Premiação</h1>", True)
    
    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()
    
    # Login Centralizado e Estreito
    _, c_log, _ = st.columns([1.5, 1, 1.5])
    with c_log:
        acesso = st.text_input("MATRÍCULA:", placeholder="Digite aqui")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            # Saudação
            c_n = [c for c in df.columns if 'NOME' in c][0]
            nome = u_df.iloc[0][c_n]
            st.markdown(f"<h2 style='text-align:center;'>Olá, {nome}! 👋</h2>", True)
            
            u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
            _, c_m, _ = st.columns([1.5, 1, 1.5])
            with c_m:
                m_sel = st.selectbox("MÊS DE REFERÊNCIA:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            # --- ÁREA DE INDICADORES (Cards mais compactos e centralizados) ---
            st.markdown("<br>", True)
            _, body, _ = st.columns([0.15, 0.7, 0.15]) # Cria respiro nas laterais
            
            with body:
                c1, c2, c3 = st.columns(3)
                
                # ADERÊNCIA
                with c1:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;margin:0;'>🎯 <b>ADERÊNCIA</b></p>", True)
                        st.markdown(f"<h2 style='text-align:center;margin:0;'>{f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0))}</h2>", True)
                        st.markdown(f"<p style='text-align:center;color:#4CAF50;font-weight:bold;font-size:18px;'>{f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}</p>", True)
                
                # LOJA
                with c2:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;margin:0;'>🏪 <b>LOJA DO CORAÇÃO</b></p>", True)
                        st.markdown(f"<h2 style='text-align:center;margin:0;'>{str(r.get('MEDALHA LOJA DO CORAÇÃO', '-'))}</h2>", True)
                        st.markdown(f"<p style='text-align:center;color:#4CAF50;font-weight:bold;font-size:18px;'>{f_rs(r.get('PREMIAÇÃO MEDALHA LC', 0))}</p>", True)
                
                # SELLOUT
                with c3:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;margin:0;'>📈 <b>SELLOUT</b></p>", True)
                        txt_sell = f"M: {f_nm(r.get('META SELLOUT',0))} | R: {f_nm(r.get('REAL SELLOUT',0))}"
                        st.markdown(f"<p style='text-align:center;font-size:12px;margin:0;'>{txt_sell}</p>", True)
                        st.markdown(f"<h2 style='text-align:center;margin:0;'>{f_pc(r.get('AING SELLOUT %', 0))}</h2>", True)
                        st.markdown(f"<p style='
