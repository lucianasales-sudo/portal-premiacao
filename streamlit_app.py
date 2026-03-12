import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Portal de Premiação 3 Corações", layout="wide")

# Design "Blindado" (Linha por linha para evitar o erro de TypeError)
st.markdown('<style>', unsafe_allow_input_html=True)
st.markdown('.pilar-header { background-color: #556B2F; color: white; padding: 10px; text-align: center; border-radius: 8px 8px 0 0; font-weight: bold; margin-bottom: 0px; }', unsafe_allow_input_html=True)
st.markdown('.pilar-card { background-color: white; padding: 20px; text-align: center; border-radius: 0 0 8px 8px; border: 1px solid #ddd; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }', unsafe_allow_input_html=True)
st.markdown('.total-box { background-color: #FFD700; color: #333; padding: 20px; text-align: center; border-radius: 10px; font-size: 24px; font-weight: bold; }', unsafe_allow_input_html=True)
st.markdown('</style>', unsafe_allow_input_html=True)

st.title("🏆 Portal de Premiação")

# 2. Carregamento dos Dados
try:
    df = pd.read_csv("dados.csv")
    df['MATRÍCULA'] = df['MATRÍCULA'].astype(str)
    
    # 3. Interface de Acesso
    acesso = st.text_input("Digite sua MATRÍCULA para acessar:", placeholder="Ex: 12345")

    if acesso:
        if acesso.upper() == "ADMIN":
            st.subheader("📊 Painel Geral (Visão Admin)")
            st.dataframe(df)
        else:
            resultado = df[df['MATRÍCULA'] == acesso]
            if not resultado.empty:
                info = resultado.iloc[0]
                st.header(f"Olá, {info['NOME RH']}! 👋")
                
                # Exibição em Colunas
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown('<div class="pilar-header">ADERÊNCIA</div>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="pilar-card"><h2>{info["PRODUTIVIDADE ADERENCIA ROTEIRO"]}%</h2><p>R$ {info["PREMIAÇÃO ADERENCIA ROTEIRO"]}</p></div>', unsafe_allow_input_html=True)
                with c2:
                    st.markdown('<div class="pilar-header">LOJA DO CORAÇÃO</div>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="pilar-card"><h2>{info["MEDALHA LOJA DO CORAÇÃO"]}</h2><p>R$ {info["PREMIAÇÃO MEDALHA LC"]}</p></div>', unsafe_allow_input_html=True)
                with c3:
                    st.markdown('<div class="pilar-header">SELL OUT</div>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="pilar-card"><h2>{info["AING SELLOUT %"]}%</h2><p>R$ {info["PREMIAÇÃO SELLOUT"]}</p></div>', unsafe_allow_input_html=True)

                st.markdown(f'<div class="total-box">TOTAL A RECEBER: R$ {info["TOTAL A RECEBER"]}</div>', unsafe_allow_input_html=True)
            else:
                st.error("Matrícula não localizada.")
except Exception as e:
    st.error("Erro ao carregar o arquivo dados.csv no GitHub.")
