import streamlit as st
import pandas as pd

# 1. Configurações de Design
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação
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

# 2. Carregamento de Dados
@st.cache_data
def load():
    try:
        try: df = pd.read_csv("dados.csv", encoding='utf-8')
        except: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except: return None

df = load()

if df is not None:
    # Cabeçalho
    st.markdown("<h1 style='text-align:center;'>🏆 Portal de Premiação</h1>", True)
    
    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()
    
    # Login Centralizado
    _, c_log, _ = st.columns([1.5, 1, 1.5])
    with c_log:
        acesso = st.text_input("MATRÍCULA:", placeholder="Digite aqui")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            # Saudação
            c_n = [c for c in df.columns if 'NOME' in c][0]
            nome = u_df.iloc[0][c_n]
            st.markdown(f"<h2 style='text-align:center;'>Olá, {nome}!</h2>", True)
            
            u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
            _, c_m, _ = st.columns([1.5, 1, 1.5])
            with c_m:
                m_sel = st.selectbox("MÊS:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            # --- PREPARAÇÃO DE VARIÁVEIS CURTAS (Anti-Erro) ---
            ad_p = f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0))
            ad_v = f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))
            
            lc_m = str(r.get('MEDALHA LOJA DO CORAÇÃO', '-'))
            lc_v = f_rs(r.get('PREMIAÇÃO MEDALHA LC', 0))
            
            so_m = f_nm(r.get('META SELLOUT', 0))
            so_r = f_nm(r.get('REAL SELLOUT', 0))
            so_a = f_pc(r.get('AING SELLOUT %', 0))
            so_v = f_rs(r.get('PREMIAÇÃO SELLOUT', 0))
            
            total = f_rs(r.get('TOTAL A RECEBER', 0))

            # --- GRID DE INDICADORES ---
            st.markdown("<br>", True)
            _, body, _ = st.columns([0.1, 0.8, 0.1])
            
            with body:
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;'>🎯 <b>ADERÊNCIA</b></p>", True)
                        st.markdown(f"<h2 style='text-align:center;'>{ad_p}</h2>", True)
                        st.markdown(f"<p style='text-align:center;color:#4CAF50;'><b>{ad_v}</b></p>", True)
                
                with c2:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;'>🏪 <b>LOJA</b></p>", True)
                        st.markdown(f"<h2 style='text-align:center;'>{lc_m}</h2>", True)
                        st.markdown(f"<p style='text-align:center;color:#4CAF50;'><b>{lc_v}</b></p>", True)
                
                with c3:
                    with st.container(border=True):
                        st.markdown("<p style='text-align:center;'>📈 <b>SELLOUT</b></p>", True)
                        st.markdown(f"<p style='text-align:center;font-size:12px;'>M: {so_m} | R: {so_r}</p>", True)
                        st.markdown(f"<h2 style='text-align:center;'>{so_a}</h2>", True)
                        st.markdown(f"<p style='text-align:center;color:#4CAF50;'><b>{so_v}</b></p>", True)

                # --- TOTALIZADOR PREMIUM ---
                st.markdown("<br>", True)
                html_total = f"""
                <div style="background-color:#1e2630;border:1px solid #4CAF50;padding:20px;border-radius:10px;text-align:center;">
                    <span style="color:white;font-size:18px;">🏆 TOTAL A RECEBER</span><br>
                    <span style="color:#4CAF50;font-size:36px;font-weight:bold;">{total}</span>
                </div>
                """
                st.markdown(html_total, unsafe_allow_input_html=True)

                obs = str(r.get('OBSERVAÇÕES GERAIS', '')).strip()
                if obs not in ['nan', '0', '', 'None']:
                    st.markdown(f"<p style='text-align:center;color:gray;'><br>📝 {obs}</p>", True)
        else:
            st.error("Matrícula não encontrada.")
