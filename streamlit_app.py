import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. Configuração Visual (Inspirado na identidade 3 Corações)
st.set_page_config(page_title="Portal de Premiação", layout="wide")

st.markdown("""
    <style>
    /* Estilo do fundo e fontes */
    .main { background-color: #fcfcfc; }
    
    /* Cabeçalho dos Pilares (Verde Oliva) */
    .header-pilar { 
        background-color: #556B2F; 
        color: white; 
        padding: 12px; 
        border-radius: 8px 8px 0px 0px; 
        text-align: center; 
        font-weight: bold;
        margin-bottom: 0px;
    }
    
    /* Cards de Dados */
    .card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 0px 0px 8px 8px; 
        text-align: center; 
        border: 1px solid #e0e0e0;
        border-top: none;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Destaque do Valor Total (Amarelo) */
    .total-container {
        background-color: #FFD700;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-top: 20px;
    }
    
    h1, h2, h3 { color: #556B2F; }
    </style>
""", unsafe_allow_input_html=True)

# Título Principal
st.title("☕ Portal de Premiação")
st.subheader("Acompanhamento de Performance e Metas")

# 2. Conexão com a Planilha via Secrets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    # 3. Sistema de Login/Consulta
    acesso = st.text_input("Para começar, digite sua MATRÍCULA:", placeholder="Ex:
