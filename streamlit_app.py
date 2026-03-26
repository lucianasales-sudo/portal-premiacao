import streamlit as st
import pandas as pd

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Portal de Premiação", layout="wide", page_icon="☕")

# CSS COM PADRONIZAÇÃO DE BOTÕES E BLINDAGEM
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* FUNDO E TEXTO GLOBAL */
    .stApp, div[data-testid="stAppViewContainer"], .main {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }

    /* INPUTS E PLACEHOLDER */
    input { color: #1e293b !important; background-color: #ffffff !important; }
    input::placeholder { color: #94a3b8 !important; opacity: 1; }

    /* Header */
    .header-container {
        display: flex; flex-direction: column; align-items: center;
        text-align: center; padding: 5px 0px 15px 0px; width: 100%;
    }
    .logo-img { width: 55px; height: auto; margin-bottom: 8px; }
    .main-title { 
        color: #1e293b !important; font-size: 15px; font-weight: 800; 
        text-transform: uppercase; white-space: nowrap; width: 100vw; 
        display: flex; justify-content: center; letter-spacing: 0.2px;
    }
    .sub-header { color: #64748b !important; font-size: 11px; margin-top: 2px; }

    /* Cards */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #ffffff !important; border: 1px solid #f1f5f9 !important;
        border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04); margin-bottom: 8px;
    }
    .card-title {
        color: #0f172a !important; font-size: 11px !important; font-weight: 700 !important;
        text-transform: uppercase !important; border-left: 3px solid #8B4513 !important;
        padding-left: 10px; margin-bottom: 10px; display: block;
    }

    /* --- PADRONIZAÇÃO DOS BOTÕES (CONSULTAR = NOVA CONSULTA) --- */
    /* Aplica-se ao st.button e ao st.form_submit_button */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        width: 100% !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: 400 !important;
        background-color: #f8fafc !important; /* Cinza bem clarinho */
        color: #64748b !important; /* Texto grafite suave */
        border: 1px solid #e2e8f0 !important; /* Borda sutil */
        padding: 8px !important;
        transition: all 0.2s ease;
    }

    /* Efeito ao passar o mouse em ambos */
    .stButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
        border-color: #cbd5e1 !important;
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
    }

    /* Banner Total */
    .total-receber {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%) !important;
        color: #ffffff !important; padding: 18px; border-radius: 12px; text-align: center; margin-top: 15px;
    }
    .total-value { font-size: 24px; font-weight: 800; display: block; color: #ffffff !important; }
    
    #MainMenu, footer, header {visibility: hidden;}
    @media (max-width: 640px) { .block-container { padding: 1rem !important; } }
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
        return f"{int(float(s))}%"
    except: return str(v)

# 2. Carregamento de Dados
@st.cache_data
def load():
    try:
        try: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: df = pd.read_csv("dados.csv", sep=',', encoding='utf-8')
        df.columns = [c.strip().upper() for c in df.columns]
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
            'TOTAL A RECEBER': 'TOT'
        }
        return df.rename(columns=m)
    except: return None

df = load()

if 'consultado' not in st.session_state: st.session_state.consultado = False
if 'matricula_id' not in st.session_state: st.session_state.matricula_id = ""

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
            with st.form("form_acesso"):
                acesso = st.text_input("Matrícula:", placeholder="Ex: 1-83362")
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
        u_df = df[df['ID_BUSCA'] == st.session_state.matricula_id]
        r_zero = u_df.iloc[0]
        n_col = [c for c in df.columns if 'NOME' in c][0]
        st.markdown(f"**Olá, {str(r_zero.get(n_col)).split()[0]}!** 👋")
        
        c_mes = [c for c in u_df.columns if 'M' in c and 'S' in c][0]
        m_sel = st.selectbox("Mês:", u_df[c_mes].unique())
        r = u_df[u_df[c_mes] == m_sel].iloc[0]

        # Containers de indicadores (Mantidos)
        with st.container():
            st.markdown('<p class="card-title">🎯 Aderência</p>', unsafe_allow_html=True)
            st.write(f"Ating.: **{f_pc(r.get('A1',0))}**")
            st.write(f"Prêmio: **{f_rs(r.get('A2',0))}**")

        with st.container():
            st.markdown('<p class="card-title">🏪 Loja do Coração</p>', unsafe_allow_html=True)
            st.write(f"Medalha: **{r.get('L1','-')}**")
            st.write(f"Prêmio: **{f_rs(r.get('L2',0))}**")

        with st.container():
            st.markdown('<p class="card-title">📈 Sellout</p>', unsafe_allow_html=True)
            st.write(f"Ating.: **{f_pc(r.get('S3',0))}**")
            st.write(f"Prêmio: **{f_rs(r.get('S4',0))}**")

        st.markdown(f"""
            <div class="total-receber">
                <span style="font-size:10px; text-transform:uppercase; opacity:0.8;">Total a Receber</span>
                <span class="total-value">{f_rs(r.get('TOT',0))}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        # Este botão agora terá o mesmo estilo do botão de formulário acima
        if st.button("Nova Consulta"):
            st.session_state.consultado = False
            st.rerun()
