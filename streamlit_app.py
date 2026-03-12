import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação simplificadas para evitar erros de tipo
def f_reais(v):
    if pd.isna(v) or str(v).strip() in ['-', '', '0', '0,00', 'nan']: return "R$ 0,00"
    v_limpo = str(v).replace('R', '').replace('$', '').replace('S', '').strip()
    return f"R$ {v_limpo}"

def f_pct(v):
    try:
        num = float(str(v).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
    except: return "0%"

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

if df is not None:
    # Título Nativo (Sem HTML para evitar o TypeError)
    st.title("🏆 Portal de Premiação")
    st.divider()

    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()

    # Login Centralizado usando colunas nativas
    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        with st.container(border=True):
            st.subheader("🔑 Acesso Restrito")
            acesso = st.text_input("👤 MATRÍCULA:", placeholder="Ex: 1-46532")
    
    if acesso:
        acesso = acesso.strip()
        user_df = df[df[c_mat] == acesso]
        
        if user_df.empty:
            st.error("Matrícula não encontrada.")
        else:
            c_nome = [c for c in df.columns if 'NOME' in c][0]
            st.header(f"Olá, {user_df.iloc[0][c_nome]}! 👋")
            
            user_df['MÊS'] = user_df['MÊS'].astype(str).str.strip().str.upper()
            mes_sel = st.selectbox("📅 Selecione o mês:", user_df['MÊS'].unique())
            
            row = user_df[user_df['MÊS'] == mes_sel].iloc[0]
            
            # --- CARDS ---
            st.markdown("### 📊 Seus Indicadores")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.subheader("🎯 ADERÊNCIA")
                    st.metric("Performance", f_pct(row.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.write(f"💰 Prêmio: **{f_reais(row.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
            
            with c2:
                with st.container(border=True):
                    st.subheader("🏪 LOJA DO CORAÇÃO")
                    med = str(row.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                    st.metric("Medalha", med)
                    st.write(f"💰 Prêmio: **{f_reais(row.get('PREMIAÇÃO MEDALHA LC', 0))}**")
            
            with c3:
                with st.container(border=True):
                    st.subheader("📈 SELLOUT")
                    st.metric("Atingimento", f_pct(row.get('AING SELLOUT %', 0)))
                    st.write(f"💰 Prêmio: **{f_reais(row.get('PREMIAÇÃO SELLOUT', 0))}**")

            st.divider()
            
            # Totalizador usando st.success (Seguro e Nativo)
            total = f_reais(row.get('TOTAL A RECEBER', '0,00'))
            st.success(f"## 🏆 VALOR TOTAL A RECEBER: {total}")
else:
    st.error("Erro ao carregar o arquivo dados.csv")
