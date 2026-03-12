import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Limpeza e Formatação
def f_reais(v):
    if pd.isna(v) or str(v).strip() in ['-', '', '0', '0,00', 'nan']: return "R$ 0,00"
    v_limpo = str(v).replace('R', '').replace('$', '').replace('S', '').strip()
    return f"R$ {v_limpo}"

def f_pct(v):
    try:
        num = float(str(v).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
    except: return str(v).strip() if pd.notna(v) else "0%"

def f_txt(v):
    return str(v).strip() if pd.notna(v) and str(v).strip() not in ['nan', '0', '-'] else "-"

# 2. Carregamento de Dados
@st.cache_data
def carregar():
    try:
        try: df = pd.read_csv("dados.csv", encoding='utf-8')
        except: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except: return None

df = carregar()
if df is None:
    st.error("Arquivo dados.csv não encontrado.")
    st.stop()

# Ajuste de Matrícula
c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
df[c_mat] = df[c_mat].astype(str).str.strip()

# --- PÁGINA 1: LOGIN CENTRALIZADO ---
st.write("#")
st.write("#")
_, col_c, _ = st.columns([1, 2, 1])

with col_c:
    st.markdown('<h1 style="text-align:center;background:#333;color:white;padding:20px;border-radius:10px;">🏆 Portal de Premiação</h1>', unsafe_allow_input_html=True)
    st.write("")
    with st.container(border=True):
        st.subheader("🔑 Acesso Restrito")
        acesso = st.text_input("👤 MATRÍCULA:", placeholder="Ex: 1-46532")
    if not acesso: st.info("💡 Digite sua matrícula e pressione Enter.")

# --- PÁGINA 2: RESULTADOS ---
if acesso:
    acesso = acesso.strip()
    if acesso.upper() == "ADMIN":
        st.divider()
        st.dataframe(df, use_container_width=True)
    else:
        user_df = df[df[c_mat] == acesso]
        if user_df.empty:
            st.error(f"Matrícula {acesso} não encontrada.")
        else:
            c_nome = [c for c in df.columns if 'NOME' in c][0]
            st.divider()
            st.header(f"Olá, {user_df.iloc[0][c_nome]}! 👋")
            
            user_df['MÊS'] = user_df['MÊS'].astype(str).str.strip().str.upper()
            _, col_m, _ = st.columns([1, 1, 1])
            with col_m:
                m_sel = st.selectbox("📅 Selecione o mês:", user_df['MÊS'].unique())
            
            row = user_df[user_df['MÊS'] == m_sel].iloc[0]
            st.markdown("### 📊 Seus Indicadores")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                with st.container(border=True):
                    st.write("🎯 **ADERÊNCIA**")
                    st.metric("Performance", f_pct(row.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
