import streamlit as st
import pandas as pd

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Portal de Premiação | 3 Corações", layout="wide", page_icon="☕")

# CSS de Alta Performance para Responsividade
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #ffffff; font-family: 'Inter', sans-serif; }

    /* Header Centralizado e Proporcional */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 10px 0 30px 0;
    }

    .logo-img {
        width: 80px; /* Tamanho discreto e proporcional */
        height: auto;
        margin-bottom: 15px;
    }

    .main-title {
        color: #1e293b;
        font-size: 24px; /* Tamanho equilibrado para celular */
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    
    .sub-header {
        color: #64748b;
        font-size: 14px;
        margin-top: 5px;
    }

    /* Cards Adaptáveis */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 16px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }

    .card-title {
        color: #0f172a !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border-left: 3px solid #8B4513;
        padding-left: 10px;
        margin-bottom: 15px;
        display: block;
    }

    /* Ajuste de métricas para não quebrar no celular */
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #f8fafc;
    }
    
    .metric-label { color: #64748b; font-size: 12px; flex-shrink: 0; }
    .metric-value { color: #1e293b; font-weight: 600; font-size: 13px; text-align: right; }
    .metric-highlight { color: #1e293b; font-weight: 800; font-size: 15px; text-align: right; }

    /* Banner Total Responsivo */
    .total-receber {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%);
        color: white;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
    }

    .total-label { font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1.5px; }
    .total-value { font-size: 28px; font-weight: 800; display: block; }

    /* Esconder elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Media Query para Celulares pequenos */
    @media (max-width: 640px) {
        .main-title { font-size: 20px; }
        .logo-img { width: 65px; }
    }
    </style>
    """, unsafe_allow_html=True)

# Funções de Formatação (Mantidas)
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

if 'consultado' not in st.session_state:
    st.session_state.consultado = False
if 'matricula_id' not in st.session_state:
    st.session_state.matricula_id = ""

# 3. Interface Visual
# HEADER USANDO HTML PARA GARANTIR ASSIMETRIA E PROPORÇÃO
st.markdown(f"""
    <div class="header-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/63/Logo_grupo_3_cora%C3%A7%C3%B5es.png" class="logo-img">
        <h1 class="main-title">🏆 Portal de Premiação</h1>
        <p class="sub-header">Resultados e Indicadores de Performance</p>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    if not st.session_state.consultado:
        _, col_login, _ = st.columns([1, 2, 1]) # Ajustado para ocupar melhor a largura
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
                        else:
                            st.error("Matrícula não encontrada.")
                    else:
                        st.warning("Informe sua matrícula.")
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
                st.markdown(f'<div class="metric-row"><span class="metric-label">Perf.</span><span class="metric-highlight">{f_pc(r.get("A1",0))}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("A2",0))}</span></div>', unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown('<p class="card-title">🏪 Loja do Coração</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Medalha</span><span class="metric-highlight">{r.get("L1","-")}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">P.Extra/Nat.</span><span class="metric-value">{r.get("P1",0)} / {r.get("P2",0)}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Rupt./MPDV</span><span class="metric-value">{r.get("P3",0)} / {r.get("P4",0)}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Nota</span><span class="metric-value">{r.get("L0", 0)}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("L2",0))}</span></div>', unsafe_allow_html=True)
        
        with col3:
            with st.container():
                st.markdown('<p class="card-title">📈 Sellout</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Meta</span><span class="metric-value">{f_nm(r.get("S1",0))}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Real</span><span class="metric-value">{f_nm(r.get("S2",0))}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Ating.%</span><span class="metric-highlight">{f_pc(r.get("S3",0))}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("S4",0))}</span></div>', unsafe_allow_html=True)

        # Banner de Total Responsivo
        st.markdown(f"""
            <div class="total-receber">
                <span class="total-label">Valor Total a Receber</span>
                <span class="total-value">{f_rs(r.get('TOT',0))}</span>
            </div>
        """, unsafe_allow_html=True)
        
        texto_obs = str(r.get('OBS_GERAIS','')).strip()
        if texto_obs not in ['nan', '0', '', 'None']:
            st.write("")
            st.markdown('<p class="card-title" style="margin-top:15px;">📝 Notas</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="obs-section">{texto_obs}</div>', unsafe_allow_html=True)
        
        st.write("")
        if st.button("Nova Consulta"):
            st.session_state.consultado = False
            st.rerun()
