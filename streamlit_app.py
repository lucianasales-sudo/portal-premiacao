import streamlit as st
import pandas as pd

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Portal de Premiação | 3 Corações", layout="wide", page_icon="☕")

# CSS "Blindado" contra inversão de cores (Modo Escuro/Claro)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Força o fundo branco e fonte Inter em todo o app */
    .stApp { 
        background-color: #ffffff !important; 
        font-family: 'Inter', sans-serif !important; 
    }

    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 10px 0 30px 0;
    }

    .logo-img { width: 80px; height: auto; margin-bottom: 15px; }

    /* Força títulos e sub-headers a serem sempre tons escuros no fundo branco */
    .main-title {
        color: #1e293b !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }
    
    .sub-header {
        color: #64748b !important;
        font-size: 14px !important;
    }

    /* Estilo dos Cards */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #ffffff !important;
        border: 1px solid #f1f5f9 !important;
        border-radius: 16px !important;
        padding: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
    }

    .card-title {
        color: #0f172a !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        border-left: 3px solid #8B4513 !important;
        padding-left: 10px !important;
        display: block !important;
    }

    /* Cores das métricas travadas para não inverterem */
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #f8fafc !important;
    }
    
    .metric-label { color: #64748b !important; font-size: 12px !important; }
    .metric-value { color: #1e293b !important; font-weight: 600 !important; font-size: 13px !important; }
    .metric-highlight { color: #1e293b !important; font-weight: 800 !important; font-size: 15px !important; }

    /* BANNER TOTAL: Força o texto a ser SEMPRE BRANCO no fundo escuro */
    .total-receber {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%) !important;
        color: #ffffff !important;
        padding: 20px !important;
        border-radius: 16px !important;
        text-align: center !important;
    }
    .total-label { color: #ffffff !important; font-size: 11px !important; opacity: 0.9; text-transform: uppercase; }
    .total-value { color: #ffffff !important; font-size: 28px !important; font-weight: 800 !important; }

    /* Notas/Observações */
    .obs-section {
        background-color: #fffbeb !important;
        border-left: 5px solid #d97706 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        color: #92400e !important;
    }

    /* Remove menus e rodapés */
    #MainMenu, footer, header { visibility: hidden !important; }

    @media (max-width: 640px) {
        .main-title { font-size: 20px !important; }
        .logo-img { width: 65px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# Funções de Formatação
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','R$ -']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-','nan']: return "0"
    return str(v).replace('R','').replace('$','').strip()

def f_pc(v):
    try:
        s = str(v).replace('%','').replace(',','.')
        n = float(s)
        return f"{int(n)}%"
    except: return str(v)

# 2. Carregamento de Dados
@st.cache_data
def load():
    try:
        try: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: df = pd.read_csv("dados.csv", sep=',', encoding='utf-8')
        df.columns = [c.strip().upper() for c in df.columns]
        
        # Mapeamentos
        c_nota = [c for c in df.columns if 'NOTA' in c and 'CORA' in c]
        if c_nota: df = df.rename(columns={c_nota[0]: 'L0'})
        c_obs = [c for c in df.columns if 'OBSERV' in c]
        if c_obs: df = df.rename(columns={c_obs[0]: 'OBS_GERAIS'})
        c_mat = [c for c in df.columns if 'MATRIC' in c]
        k_mat = c_mat[0] if c_mat else df.columns[0]
        df['ID_BUSCA'] = df[k_mat].astype(str).str.strip()

        m = {
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'A1', 'PREMIAÇÃO ADERENCIA ROTEIRO': 'A2',
            'MEDALHA LOJA DO CORAÇÃO': 'L1', 'PREMIAÇÃO MEDALHA LC': 'L2',
            'META SELLOUT': 'S1', 'REAL SELLOUT': 'S2',
            'AING SELLOUT %': 'S3', 'PREMIAÇÃO SELLOUT': 'S4',
            'TOTAL A RECEBER': 'TOT', 'PONTO EXTRA': 'P1',
            'PONTO NATURAL': 'P2', 'RUPTURA': 'P3', 'MPDV': 'P4'
        }
        return df.rename(columns=m)
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

df = load()

# Session State
if 'consultado' not in st.session_state: st.session_state.consultado = False
if 'matricula_id' not in st.session_state: st.session_state.matricula_id = ""

# 3. Interface Visual
st.markdown(f"""
    <div class="header-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/63/Logo_grupo_3_cora%C3%A7%C3%B5es.png" class="logo-img">
        <h1 class="main-title">🏆 Portal de Premiação</h1>
        <p class="sub-header">Resultados e Indicadores de Performance</p>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    if not st.session_state.consultado:
        _, col_login, _ = st.columns([1, 2, 1])
        with col_login:
            with st.form("form_acesso"):
                acesso = st.text_input("Sua Matrícula:", placeholder="Digite aqui...")
                btn_acessar = st.form_submit_button("Consultar")
                if btn_acessar:
                    if acesso:
                        u_id = acesso.strip()
                        u_df = df[df['ID_BUSCA'] == u_id]
                        if not u_df.empty:
                            st.session_state.consultado = True
                            st.session_state.matricula_id = u_id
                            st.rerun()
                        else: st.error("Matrícula não encontrada.")
                    else: st.warning("Informe sua matrícula.")
    else:
        u_df = df[df['ID_BUSCA'] == st.session_state.matricula_id]
        row_zero = u_df.iloc[0]
        n_cols = [c for c in df.columns if 'NOME' in c]
        nome_f = str(row_zero.get(n_cols[0], 'Colaborador'))
        
        st.markdown(f"### Olá, **{nome_f.split()[0]}**! 👋")
        
        c_mes = [c for c in u_df.columns if 'M' in c and 'S' in c][0]
        m_sel = st.selectbox("Selecione o Mês:", u_df[c_mes].unique())
        r = u_df[u_df[c_mes] == m_sel].iloc[0]
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            with st.container():
                st.markdown('<p class="card-title">🎯 Aderência</p>', unsafe_allow_html=True)
                st.markdown(f'<div class
