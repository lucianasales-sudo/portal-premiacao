import streamlit as st
import pandas as pd

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Portal de Premiação", layout="wide", page_icon="☕")

# CSS com Blindagem contra cortes laterais
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #ffffff; font-family: 'Inter', sans-serif; }

    /* Header com largura total e sem cortes */
    .header-container {
        display: flex; flex-direction: column; align-items: center;
        text-align: center; 
        padding: 5px 0px 20px 0px;
        width: 100%;
        margin: 0 auto;
    }
    
    .logo-img { width: 50px; height: auto; margin-bottom: 8px; }
    
    /* TÍTULO SLIM - 15px e largura forçada */
    .main-title { 
        color: #1e293b; 
        font-size: 15px; 
        font-weight: 800; 
        margin: 0; 
        text-transform: uppercase;
        white-space: nowrap; 
        letter-spacing: 0px;
        width: 100vw; /* Ocupa a largura da janela */
        display: flex;
        justify-content: center;
    }
    
    .sub-header { color: #64748b; font-size: 11px; margin-top: 2px; }

    /* Estilização dos Blocos (Cards) */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #ffffff; border: 1px solid #f1f5f9;
        border-radius: 12px; padding: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04); margin-bottom: 8px;
    }

    .card-title {
        color: #0f172a !important; font-size: 11px !important;
        font-weight: 700 !important; text-transform: uppercase !important;
        border-left: 3px solid #8B4513; padding-left: 10px; margin-bottom: 10px; display: block;
    }

    .metric-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 5px 0; border-bottom: 1px solid #f8fafc;
    }
    .metric-label { color: #64748b; font-size: 11px; }
    .metric-value { color: #1e293b; font-weight: 600; font-size: 12px; }
    .metric-highlight { color: #1e293b; font-weight: 800; font-size: 13px; }

    .total-receber {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%);
        color: white; padding: 15px; border-radius: 12px;
        text-align: center; margin-top: 10px;
    }
    .total-label { font-size: 9px; opacity: 0.8; text-transform: uppercase; }
    .total-value { font-size: 22px; font-weight: 800; display: block; }

    .stButton>button { width: 100%; border-radius: 8px; font-size: 12px; }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Remove padding lateral padrão do Streamlit no mobile */
    @media (max-width: 640px) {
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
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
            'TOTAL A RECEBER': 'TOT', 'PONTO EXTRA': 'P1',
            'PONTO NATURAL': 'P2', 'RUPTURA': 'P3', 'MPDV': 'P4'
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
                acesso = st.text_input("Matrícula:", placeholder="Digite aqui...")
                if st.form_submit_button("Consultar"):
                    if acesso:
                        u_df = df[df['ID_BUSCA'] == acesso.strip()]
                        if not u_df.empty:
                            st.session_state.consultado = True
                            st.session_state.matricula_id = acesso.strip()
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

        with st.container():
            st.markdown('<p class="card-title">🎯 Aderência</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Ating.</span><span class="metric-highlight">{f_pc(r.get("A1",0))}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("A2",0))}</span></div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<p class="card-title">🏪 Loja do Coração</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Medalha</span><span class="metric-highlight">{r.get("L1","-")}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Extra/Nat.</span><span class="metric-value">{r.get("P1",0)}/{r.get("P2",0)}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Nota</span><span class="metric-value">{r.get("L0",0)}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("L2",0))}</span></div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<p class="card-title">📈 Sellout</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Meta/Real</span><span class="metric-value">{f_nm(r.get("S1",0))}/{f_nm(r.get("S2",0))}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Ating.</span><span class="metric-highlight">{f_pc(r.get("S3",0))}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("S4",0))}</span></div>', unsafe_allow_html=True)

        st.markdown(f"""<div class="total-receber"><span class="total-label">Total a Receber</span><span class="total-value">{f_rs(r.get('TOT',0))}</span></div>""", unsafe_allow_html=True)
        
        obs = str(r.get('OBS_GERAIS','')).strip()
        if obs not in ['nan', '0', '', 'None']:
            st.markdown(f'<div style="background:#f8fafc; padding:15px; border-radius:10px; margin-top:15px; font-size:12px; border-left:4px solid #8B4513;"><b>Nota:</b> {obs}</div>', unsafe_allow_html=True)
        
        if st.button("Nova Consulta"):
            st.session_state.consultado = False
            st.rerun()
