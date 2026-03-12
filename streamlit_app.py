import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal de Premiação | 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação
def formatar_reais(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0', '0,00', 'nan', 'NAN']:
        return "R$ 0,00"
    limpo = str(valor).replace('R', '').replace('$', '').replace('S', '').replace('s', '').strip()
    return f"R$ {limpo}"

def formatar_pct(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0', '0%', 'nan', 'NAN']:
        return "0%"
    try:
        num = float(str(valor).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
    except:
        return str(valor).strip()

def limpar_dado(valor):
    if pd.isna(valor) or str(valor).strip() in ['nan', 'NAN', '0', '-']:
        return "-"
    return str(valor).strip()

# 2. Carregamento de Dados
@st.cache_data
def carregar_dados():
    try:
        try:
            df_local = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df_local = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df_local.columns = [c.strip().upper() for c in df_local.columns]
        return df_local
    except:
        return None

df = carregar_dados()

if df is None:
    st.error("❌ Erro ao carregar dados.csv")
    st.stop()

col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
df[col_mat] = df[col_mat].astype(str).str.strip()

# --- PÁGINA 1: ACESSO (Login Centralizado) ---
st.markdown("<br><br>", unsafe_allow_input_html=True)
col_l, col_center, col_r = st.columns([1, 2, 1])

with col_center:
    st.markdown('<div style="text-align: center;"><h1 style="background-color: #333; color: white; padding: 20px; border-radius: 10px;">🏆 Portal de Premiação</h1></div>', unsafe_allow_input_html=True)
    st.write("")
    
    with st.container(border=True):
        st.markdown('<h3 style="text-align: center; color: #333;">🔑 Acesso Restrito</h3>', unsafe_allow_input_html=True)
        acesso = st.text_input("👤 MATRÍCULA:", placeholder="Ex: 1-46532")
    
    if not acesso:
        st.info("💡 Digite sua matrícula e pressione Enter.")

# --- PÁGINA 2: RESULTADOS ---
if acesso:
    acesso = acesso.strip()
    if acesso.upper() == "ADMIN":
        st.divider()
        st.dataframe(df, use_container_width=True)
    else:
        dados_pessoais = df[df[col_mat] == acesso]
        
        if dados_pessoais.empty:
            st.error(f"Matrícula '{acesso}' não encontrada.")
        else:
            col_nome = [c for c in df.columns if 'NOME' in c][0]
            nome_promo = dados_pessoais.iloc[0][col_nome]
            
            st.divider()
            st.header(f"Olá, {nome_promo}! 👋")
            
            dados_pessoais['MÊS'] = dados_pessoais['MÊS'].astype(str).str.strip().str.upper()
            mes_sel = st.selectbox("📅 Selecione o mês:", dados_pessoais['MÊS'].unique())
            
            info = dados_pessoais
