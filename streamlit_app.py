import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

st.title("🏆 Portal de Premiação")
st.write("Acompanhe seus resultados e metas mensais.")
st.divider()

def carregar():
    try:
        try:
            df = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except:
        return None

def formatar_reais(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0', '0,00']:
        return "R$ 0,00"
    limpo = str(valor).replace('R', '').replace('$', '').strip()
    return f"R$ {limpo}"

def formatar_pct(valor):
    try:
        num = float(str(valor).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
    except:
        return str(valor)

df = carregar()

if df is not None:
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    with st.sidebar:
        st.header("🔑 Acesso")
        acesso = st.text_input("Digite sua MATRÍCULA:", placeholder="Ex: 1-46532")
    
    else:
            # Limpa espaços extras da matrícula pesquisada
            acesso = acesso.strip()
            dados = df[df[col_mat] == acesso]
            
            if not dados.empty:
                col_n = [c for c in df.columns if 'NOME' in c][0]
                st.header(f"Olá, {dados.iloc[0][col_n]}! 👋")
                
                # Garante que os meses não tenham espaços extras e fiquem em maiúsculo
                dados['MÊS'] = dados['MÊS'].astype(str).str.strip().str.upper()
                meses = dados['MÊS'].unique()
                
                mes_sel = st.selectbox("📅 Selecione o mês:", meses)
                
                # Filtro final mais "robusto"
                info = dados[dados['MÊS'] == mes_sel].iloc[0]
                
                st.markdown("### 📊 Seus Indicadores")
                # ... daqui para baixo o código dos cards continua igual
