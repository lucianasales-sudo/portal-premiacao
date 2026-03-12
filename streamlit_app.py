import streamlit as st
import pandas as pd

# 1. Configurações
st.set_page_config(layout="wide", page_icon="☕")

# Funções de Formatação Curtas
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-']: 
        return "R$ 0,00"
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

# 2. Dados
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
    # Centralização do Título
    _, c_tit, _ = st.columns([1, 2, 1])
    c_tit.markdown("<h1 style='text-align:center;'>🏆 Portal</h1>", True)
    
    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()
    
    # Login
    _, c_log, _ = st.columns([1, 1, 1])
    with c_log:
        acesso = st.text_input("MATRÍCULA:", placeholder="Digite aqui")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            # Saudação
            c_n = [c for c in df.columns if 'NOME' in c][0]
            nome = u_df.iloc[0][c_n]
            st.markdown(f"<h2 style='text-align:center;'>Olá, {nome}</h2>", True)
            
            u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
            _, c_m, _ = st.columns([1, 1, 1])
            with c_m:
                m_sel = st.selectbox("MÊS:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            # --- VARIÁVEIS CURTAS ---
            v_ad = f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))
            v_lc = f_rs(r.get('PREMIAÇÃO MEDALHA LC', 0))
            v_so = f_rs(r.get('PREMIAÇÃO SELLOUT', 0))
            v_tt = f_rs(r.get('TOTAL A RECEBER', 0))
            
            # --- GRID ---
            _, body, _ = st.columns([0.1, 0.8, 0.1])
            with body:
                c1, c2, c3 = st.columns(3)
                with c1:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;'>🎯 <b>ADERÊNCIA</b></p>", True)
                        st.metric("Performance", f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                        st.markdown(f"<p style='text-align:center;color:green;'>{v_ad}</p>", True)
                with c2:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;'>🏪 <b>LOJA</b></p>", True)
                        med = str(r.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                        st.metric("Medalha", med)
                        st.markdown(f"<p style='text-align:center;color:green;'>{v_lc}</p>", True)
                with c3:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;'>📈 <b>SELLOUT</b></p>", True)
                        txt_s = f"M: {f_nm(r.get('META SELLOUT',0))} | R: {f_nm(r.get('REAL SELLOUT',0))}"
                        st.markdown(f"<p style='text-align:center;font-size:12px;'>{txt_s}</p>", True)
                        st.metric("Ating.", f_pc(r.get('AING SELLOUT %', 0)))
                        st.markdown(f"<p style='text-align:center;color:green;'>{v_so}</p>", True)

                st.divider()
                st.success(f"🏆 TOTAL A RECEBER: {v_tt}")
                
                obs = str(r.get('OBSERVAÇÕES GERAIS', '')).strip()
                if obs not in ['nan', '0', '', 'None']:
                    st.info(f"📝 Notas: {obs}")
        else:
            st.error("Matrícula não encontrada.")
