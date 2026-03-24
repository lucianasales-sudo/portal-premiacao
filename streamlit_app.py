import streamlit as st
import pandas as pd

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Portal de Premiação | 3 Corações", layout="wide", page_icon="☕")

# CSS Avançado para Design Moderno e Elegante
st.markdown("""
    <style>
    /* Importando fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f1f5f9;
    }

    /* Estilização do Título e Header */
    .main-title {
        color: #1e293b;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 5px;
    }
    
    .sub-header {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Cards Brancos com Sombra Suave */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #ffffff;
        padding: 5px;
        border-radius: 12px;
    }

    /* Customização dos Containers (Cards) */
    .premium-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-2px);
    }

    /* Cabeçalhos dos Cards */
    .card-title {
        color: #0f172a;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-left: 4px solid #8B4513; /* Tom Café / 3 Corações */
        padding-left: 12px;
        margin-bottom: 20px;
    }

    /* Estilo dos Valores */
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .metric-label { color: #64748b; font-size: 14px; }
    .metric-value { color: #1e293b; font-weight: 600; font-size: 15px; }
    .metric-highlight { color: #1e293b; font-weight: 800; font-size: 18px; }

    /* Sucesso / Valor Total */
    .total-receber {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }

    /* Bloco de Observações */
    .obs-section {
        background-color: #f8fafc;
        border-left: 5px solid #64748b;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
    }

    /* Esconder menus padrão para look de sistema */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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

# 2. Carregamento de Dados (Lógica Mantida)
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

# 3. Interface Visual
st.markdown('<p class="main-title">Portal de Premiação</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Consulte seu desempenho e indicadores mensais</p>', unsafe_allow_html=True)

if df is not None:
    c_busca1, _ = st.columns([1, 2])
    with c_busca1:
        acesso = st.text_input("Acesso via Matrícula:", placeholder="Digite aqui...")
    
    if acesso:
        u_df = df[df['ID_BUSCA'] == acesso.strip()]
        
        if not u_df.empty:
            row_zero = u_df.iloc[0]
            n_cols = [c for c in df.columns if 'NOME' in c]
            nome_f = str(row_zero.get(n_cols[0], 'Colaborador'))
            st.markdown(f"### Olá, **{nome_f.split()[0]}**! 👋")
            
            c_mes_col = [c for c in u_df.columns if 'M' in c and 'S' in c][0]
            m_sel = st.selectbox("Selecione o Ciclo:", u_df[c_mes_col].unique())
            r = u_df[u_df[c_mes_col] == m_sel].iloc[0]
            
            st.write("")

            # --- CARDS PRINCIPAIS COM DESIGN PREMIUM ---
            col1, col2, col3 = st.columns(3)
            
            with col1:
                with st.container():
                    st.markdown('<p class="card-title">🎯 Aderência Roteiro</p>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Performance</span><span class="metric-highlight">{f_pc(r.get("A1",0))}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("A2",0))}</span></div>', unsafe_allow_html=True)
            
            with col2:
                with st.container():
                    st.markdown('<p class="card-title">🏪 Loja do Coração</p>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Medalha</span><span class="metric-highlight">{r.get("L1","-")}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">P. Extra / Natural</span><span class="metric-value">{r.get("P1",0)} / {r.get("P2",0)}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Ruptura / MPDV</span><span class="metric-value">{r.get("P3",0)} / {r.get("P4",0)}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Nota</span><span class="metric-value">{r.get("L0", 0)}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("L2",0))}</span></div>', unsafe_allow_html=True)
            
            with col3:
                with st.container():
                    st.markdown('<p class="card-title">📈 Sellout</p>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Meta</span><span class="metric-value">{f_nm(r.get("S1",0))}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Real</span><span class="metric-value">{f_nm(r.get("S2",0))}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Atingimento %</span><span class="metric-highlight">{f_pc(r.get("S3",0))}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("S4",0))}</span></div>', unsafe_allow_html=True)

            # --- TOTALIZADOR ESTILIZADO ---
            st.markdown(f"""
                <div class="total-receber">
                    <span style="font-size: 14px; opacity: 0.8; text-transform: uppercase; letter-spacing: 2px;">Valor Total a Receber</span><br>
                    <span style="font-size: 36px; font-weight: 800;">{f_rs(r.get('TOT',0))}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # --- BLOCO DE OBSERVAÇÕES ---
            texto_obs = str(r.get('OBS_GERAIS','')).strip()
            if texto_obs not in ['nan', '0', '', 'None']:
                st.write("")
                st.markdown('<p class="card-title" style="margin-top:20px;">📝 Notas da Liderança</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="obs-section">{texto_obs}</div>', unsafe_allow_html=True)
        else:
            st.warning("Matrícula não encontrada no sistema.")
