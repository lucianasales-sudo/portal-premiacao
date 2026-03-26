import streamlit as st
import pandas as pd

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Portal de Premiação", layout="wide", page_icon="☕")

# CSS COM BLINDAGEM REFORÇADA E BOTÃO PREMIUM
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* FORÇAR FUNDO BRANCO E LETRAS ESCURAS EM TODO O APP (Blindagem Samsung) */
    .stApp, div[data-testid="stAppViewContainer"], .main {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }

    /* FORÇAR COR DAS FONTES EM INPUTS E SELECTBOX (Blindagem Samsung) */
    input, div[data-baseweb="select"] > div, li {
        color: #1e293b !important;
        background-color: #ffffff !important;
    }

    /* FIX: FORÇAR COR CLARA NO PLACEHOLDER (Blindagem Samsung) */
    input::placeholder {
        color: #94a3b8 !important; /* Um cinza legível mas suave */
        opacity: 1;
    }

    /* Header Centralizado e Slim */
    .header-container {
        display: flex; flex-direction: column; align-items: center;
        text-align: center; padding: 5px 0px 20px 0px; width: 100%; margin: 0 auto;
    }
    .logo-img { width: 55px; height: auto; margin-bottom: 8px; }
    
    .main-title { 
        color: #1e293b !important; 
        font-size: 15px; font-weight: 800; margin: 0; 
        text-transform: uppercase; white-space: nowrap; 
        width: 100vw; display: flex; justify-content: center;
    }
    
    .sub-header { color: #64748b !important; font-size: 11px; margin-top: 2px; }

    /* Estilização dos Cards - Forçando Fundo Branco */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #ffffff !important; 
        border: 1px solid #f1f5f9 !important;
        border-radius: 12px; padding: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04); margin-bottom: 8px;
    }

    .card-title {
        color: #0f172a !important; font-size: 11px !important;
        font-weight: 700 !important; text-transform: uppercase !important;
        border-left: 3px solid #8B4513 !important; padding-left: 10px; margin-bottom: 10px; display: block;
    }

    .metric-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 5px 0; border-bottom: 1px solid #f8fafc;
    }
    .metric-label { color: #64748b !important; font-size: 11px; }
    .metric-value { color: #1e293b !important; font-weight: 600; font-size: 12px; }
    .metric-highlight { color: #1e293b !important; font-weight: 800; font-size: 13px; }

    /* Banner de Total - Fundo Escuro com Letras Brancas */
    .total-receber {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%) !important;
        color: #ffffff !important; padding: 18px; border-radius: 12px;
        text-align: center; margin-top: 15px;
    }
    .total-label { font-size: 10px; opacity: 0.8; text-transform: uppercase; color: #ffffff !important; }
    .total-value { font-size: 24px; font-weight: 800; display: block; color: #ffffff !important; }

    /* --- NOVO ESTILO DO BOTÃO: FUNDO MARROM CORPORATIVO COM TEXTO BRANCO --- */
    .stButton>button { 
        width: 100%; border-radius: 8px; font-size: 14px; font-weight: 700 !important;
        background-color: #8B4513 !important; /* Marrom 3 Corações */
        color: #ffffff !important; /* TEXTO BRANCO PURO */
        border: none !important;
        padding: 10px !important;
        box-shadow: 0 4px 6px rgba(139, 69, 19, 0.2) !important;
    }
    
    /* Efeito ao passar o mouse ou clicar (FeedBack Visual) */
    .stButton>button:hover, .stButton>button:active, .stButton>button:focus {
        background-color: #5D2E0A !important; /* Marrom mais escuro */
        color: #ffffff !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    @media (max-width: 640px) {
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# (Funções f_rs, f_nm, f_pc e carregamento de dados continuam iguais)

# ... (Manter código de carregamento de dados e session_state)

# 3. Interface
st.markdown(f"""
    <div class="header-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/63/Logo_grupo_3_cora%C3%A7%C3%B5es.png" class="logo-img">
        <div class="main-title">PORTAL PREMIAÇÃO</div>
        <p class="sub-header">Resultados e Indicadores</p>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    if not st.session_state.consultado:
        _, col_login, _ = st.columns([0.05, 0.9, 0.05])
        with col_login:
            # --- MUDANÇA NO FORMULÁRIO ---
            with st.form("form_acesso"):
                acesso = st.text_input("Matrícula:", placeholder="Digite aqui...")
                
                # Botão Consultar agora sairá Marrom com texto Branco
                if st.form_submit_button("Consultar"):
                    if acesso:
                        u_id = acesso.strip()
                        u_df = df[df['ID_BUSCA'] == u_id]
                        if not u_df.empty:
                            st.session_state.consultado = True
                            st.session_state.matricula_id = u_id
                            st.rerun()
                        else: st.error("Não encontrado.")
                    else: st.warning("Informe sua matrícula.")
    else:
        # (O restante do seu código de visualização continua igual)
# ...
