import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal de Premiação 3 Corações", layout="wide")

# Estilo em linha única para evitar o erro de TypeError nas aspas triplas
estilo = """
<style>
    .stApp { background-color: #f8f9fa; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 8px solid #556B2F; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center; margin-bottom: 20px;
    }
    .metric-title { color: #556B2F; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .metric-value { color: #333; font-size: 32px; font-weight: bold; margin: 10px 0; }
    .metric-prize { color: #28a745; font-size: 16px; font-weight: bold; }
    .total-banner {
        background: linear-gradient(90deg, #FFD700 0%, #ffcc00 100%);
        padding: 30px; border-radius: 20px; text-align: center;
        margin-top: 30px; border: 2px solid #e6b800;
    }
</style>
"""
st.markdown(estilo.replace('\n', ' '), unsafe_allow_input_html=True)

# 2. Títulos
st.title("☕ Portal de Premiação")
st.markdown("---")

def carregar_dados():
    try:
        try:
            df = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except: return None

df = carregar_dados()

if df is not None:
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    col_l, _ = st.columns([2, 3])
    with col_l:
        acesso = st.text_input("👤 Digite sua MATRÍCULA:", placeholder="Ex: 1-37507")

    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN":
            st.dataframe(df)
        else:
            dados = df[df[col_mat] == acesso]
            if not dados.empty:
                col_n = [c for c in df.columns if 'NOME' in c][0]
                st.markdown(f"### Olá, **{dados.iloc[0][col_n]}**! 👋")
                
                meses = dados['MÊS'].unique()
                mes_sel = st.selectbox("📅 Selecione o mês:", meses)
                info = dados[dados['MÊS'] == mes_sel].iloc[0]
                
                st.markdown("<br>", unsafe_allow_input_html=True)

                # CARDS
                c1, c2, c3 = st.columns(3)
                
                # Função para gerar o HTML do card sem quebras de linha perigosas
                def gerar_card(titulo, valor, premio, cor="#556B2F"):
                    return f'<div class="metric-card" style="border-left-color: {cor}"><div class="metric-title">{titulo}</div><div class="metric-value">{valor}</div><div class="metric-prize">Prêmio: R$ {premio}</div></div>'

                with c1:
                    v_ad = str(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', '0')).replace('%', '') + '%'
                    st.markdown(gerar_card("Aderência", v_ad, info.get('PREMIAÇÃO AD
