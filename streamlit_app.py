import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal 3 Corações", layout="wide")

# Design em linha única (sem quebras)
st.markdown('<style>.stApp{background-color:#f8f9fa}.metric-card{background-color:white;padding:20px;border-radius:15px;border-left:8px solid #556B2F;box-shadow:2px 2px 10px rgba(0,0,0,0.1);text-align:center;margin-bottom:20px}.metric-title{color:#556B2F;font-size:14px;font-weight:bold;text-transform:uppercase}.metric-value{color:#333;font-size:32px;font-weight:bold;margin:10px 0}.metric-prize{color:#28a745;font-size:16px;font-weight:bold}.total-banner{background:linear-gradient(90deg,#FFD700 0%,#ffcc00 100%);padding:30px;border-radius:20px;text-align:center;margin-top:30px;border:2px solid #e6b800}</style>', unsafe_allow_input_html=True)

st.title("☕ Portal de Premiação")

def carregar():
    try:
        try: df = pd.read_csv("dados.csv", encoding='utf-8')
        except: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except: return None

df = carregar()
if df is not None:
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    acesso = st.text_input("👤 MATRÍCULA:", placeholder="Ex: 1-37507")
    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN": st.dataframe(df)
        else:
            dados = df[df[col_mat] == acesso]
            if not dados.empty:
                col_n = [c for c in df.columns if 'NOME' in c][0]
                st.markdown(f"### Olá, {dados.iloc[0][col_n]}! 👋")
                
                mes_sel = st.selectbox("📅 Mês:", dados['MÊS'].unique())
                info = dados[dados['MÊS'] == mes_sel].iloc[0]
                
                c1, c2, c3 = st.columns(3)
                
                # Nomes curtos para as colunas para evitar quebra de linha no código
                p_ad = info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)
                v_ad = info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0)
                m_lc = info.get('MEDALHA LOJA DO CORAÇÃO', '-')
                v_lc = info.get('PREMIAÇÃO MEDALHA LC', 0)
                p_so = info.get('AING SELLOUT %', 0)
                v_so = info.get('PREMIAÇÃO SELLOUT', 0)
                total = info.get('TOTAL A RECEBER', 0)

                with c1:
                    st.markdown(f'<div class="metric-card"><div class="metric-title">Aderência</div><div class="metric-value">{p_ad}%</div><div class="metric-prize">R$ {v_ad}</div></div>', unsafe_allow_input_html=True)
                with c2:
                    st.markdown(f'<div class="metric-card" style="border-left-color:#cc0000"><div class="metric-title">Loja Coração</div><div class="metric-value">{m_lc}</div><div class="metric-prize">R$ {v_lc}</div></div>', unsafe_allow_input_html=True)
                with c3:
                    st.markdown(f'<div class="metric-card" style="border-left-color:#ff8c00"><div class="metric-title">Sell Out</div><div class="metric-value">{p_so}%</div><div class="metric-prize">R$ {v_so}</div></div>', unsafe_allow_input_html=True)

                st.markdown(f'<div class="total-banner"><span style="color:#555">TOTAL A RECEBER</span><br><span style="font-size:40px;font-weight:bold">R$ {total}</span></div>', unsafe_allow_input_html=True)
            else: st.error("Não encontrado.")
