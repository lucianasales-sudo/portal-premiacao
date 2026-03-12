import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Portal de Premiação", layout="wide")

st.markdown("""
    <style>
    .header-pilar { background-color: #556B2F; color: white; padding: 10px; border-radius: 8px 8px 0 0; text-align: center; font-weight: bold; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; text-align: center; border: 1px solid #e0e0e0; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .total-container { background-color: #FFD700; padding: 20px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold; margin-top: 20px; }
    </style>
""", unsafe_allow_input_html=True)

st.title("☕ Portal de Premiação")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    acesso = st.text_input("Para começar, digite sua MATRÍCULA:", placeholder="Ex: 12345")

    if acesso:
        if acesso.lower() == "admin":
            st.dataframe(df)
        else:
            dados = df[df['MATRÍCULA'].astype(str) == acesso]
            if not dados.empty:
                info = dados.iloc[0]
                st.markdown(f"## Olá, **{info['NOME RH']}**!")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<p class="header-pilar">ADERÊNCIA</p>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="card"><h2>{info["PRODUTIVIDADE ADERENCIA ROTEIRO"]}%</h2><p>R$ {info["PREMIAÇÃO ADERENCIA ROTEIRO"]}</p></div>', unsafe_allow_input_html=True)
                with col2:
                    st.markdown('<p class="header-pilar">LOJA DO CORAÇÃO</p>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="card"><h2>{info["MEDALHA LOJA DO CORAÇÃO"]}</h2><p>R$ {info["PREMIAÇÃO MEDALHA LC"]}</p></div>', unsafe_allow_input_html=True)
                with col3:
                    st.markdown('<p class="header-pilar">SELL OUT</p>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="card"><h2>{info["AING SELLOUT %"]}%</h2><p>R$ {info["PREMIAÇÃO SELLOUT"]}</p></div>', unsafe_allow_input_html=True)
                st.markdown(f'<div class="total-container">TOTAL A RECEBER: R$ {info["TOTAL A RECEBER"]}</div>', unsafe_allow_input_html=True)
            else:
                st.error("Matrícula não encontrada.")
except Exception as e:
    st.info("Conectando à base de dados...")
