import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# --- CSS PARA CENTRALIZAÇÃO ---
st.markdown("""
    <style>
    /* Centraliza os títulos e prêmios nos cards */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], .stMarkdown {
        text-align: center !important;
    }
    /* Centraliza os ícones e colunas dentro dos containers */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div {
        text-align: center !important;
    }
    /* Centraliza os cards de métricas */
    [data-testid="stMetric"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """, unsafe_allow_input_html=True)

# Funções de Formatação
def f_reais(v):
    if pd.isna(v) or str(v).strip() in ['-', '', '0', '0,00', 'nan']: return "R$ 0,00"
    v_limpo = str(v).replace('R', '').replace('$', '').replace('S', '').strip()
    return f"R$ {v_limpo}"

def f_numero(v):
    if pd.isna(v) or str(v).strip() in ['-', '', 'nan', '0']: return "0"
    v_limpo = str(v).replace('R', '').replace('$', '').replace('S', '').replace('.', '').replace(',', '.').strip()
    try:
        num = float(v_limpo)
        return f"{num:,.0f}".replace(',', '.')
    except:
        return str(v).replace('R', '').replace('$', '').strip()

def f_pct(v):
    try:
        num = float(str(v).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
    except: return "0%"

# 2. Carregamento de Dados
@st.cache_data
def carregar():
    try:
        try:
            df_local = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df_local = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df_local.columns = [c.strip().upper() for c in df_local.columns]
        return df_local
    except:
        return None

df = carregar()

if df is not None:
    st.title("🏆 Portal de Premiação")
    st.divider()

    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()

    # Login
    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        with st.container(border=True):
            st.subheader("🔑 Acesso Restrito")
            acesso = st.text_input("👤 MATRÍCULA:", placeholder="Ex: 1-46532")
    
    if acesso:
        acesso = acesso.strip()
        user_df = df[df[col_mat] == acesso]
        
        if not user_df.empty:
            col_n = [c for c in df.columns if 'NOME' in c][0]
            st.markdown(f"<h2 style='text-align: center;'>Olá, {user_df.iloc[0][col_n]}! 👋</h2>", unsafe_allow_input_html=True)
            
            user_df['MÊS'] = user_df['MÊS'].astype(str).str.strip().str.upper()
            
            _, col_m, _ = st.columns([1, 1, 1])
            with col_m:
                mes_sel = st.selectbox("📅 Selecione o mês:", user_df['MÊS'].unique())
            
            row = user_df[user_df['MÊS'] == mes_sel].iloc[0]
            
            st.markdown("<h3 style='text-align: center;'>📊 Seus Indicadores</h3>", unsafe_allow_input_html=True)
            
            # --- CARDS CENTRALIZADOS ---
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.markdown("🎯 **ADERÊNCIA**")
                    st.metric("Performance", f_pct(row.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.markdown(f"💰 Prêmio: **{f_reais(row.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
            
            with c2:
                with st.container(border=True):
                    st.markdown("🏪 **LOJA DO CORAÇÃO**")
                    med = str(row.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                    st.metric("Medalha", med)
                    st.markdown(f"💰 Prêmio: **{f_reais(row.get('PREMIAÇÃO MEDALHA LC', 0))}**")
            
            with c3:
                with st.container(border=True):
                    st.markdown("📈 **SELLOUT**")
                    cm, cr = st.columns(2)
                    cm.metric("🎯 Meta", f_numero(row.get('META SELLOUT', 0)))
                    cr.metric("📈 Real", f_numero(row.get('REAL SELLOUT', 0)))
                    
                    st.metric("📊 Atingimento", f_pct(row.get('AING SELLOUT %', 0)))
                    st.markdown(f"💰 Prêmio: **{f_reais(row.get('PREMIAÇÃO SELLOUT', 0))}**")

            st.divider()
            total = f_reais(row.get('TOTAL A RECEBER', '0,00'))
            st.success(f"###
