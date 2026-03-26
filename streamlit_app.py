import streamlit as st
import pandas as pd
import base64

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Portal de Premiação | 3 Corações", layout="wide", page_icon="☕")

# CSS Avançado: Fundo Branco, Design Clean e Sombras Suaves (Mantido e Refinado)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Fundo Branco da Aplicação */
    .stApp {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Estilização dos Cards (Containers) */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }

    .card-title {
        color: #0f172a !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border-left: 4px solid #8B4513; /* Tom Café */
        padding-left: 12px;
        margin-bottom: 20px;
        display: block;
    }

    /* Linhas de Métricas */
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #f8fafc;
    }
    
    .metric-label { color: #64748b; font-size: 14px; }
    .metric-value { color: #1e293b; font-weight: 600; font-size: 15px; }
    .metric-highlight { color: #1e293b; font-weight: 800; font-size: 18px; }

    /* Banner de Valor Total */
    .total-receber {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%);
        color: white;
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin-top: 25px;
        box-shadow: 0 10px 20px rgba(139, 69, 19, 0.2);
    }

    /* Bloco de Observações */
    .obs-section {
        background-color: #fffbeb;
        border-left: 5px solid #d97706;
        padding: 20px;
        border-radius: 8px;
        color: #92400e;
        margin-top: 10px;
        line-height: 1.6;
    }
    
    /* Centralizar imagem e título na Login Page */
    .stImage > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 20px;
    }
    
    .stForm > div {
        border: none;
        box-shadow: none;
    }

    /* Limpeza de elementos padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Funções de Formatação (Mantidas conforme seu padrão)
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

# 2. Carregamento de Dados (Foco exclusivo em dados.csv)
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
        st.error(f"Erro ao carregar o arquivo dados.csv: {e}")
        return None

df = load()

# Controle de Tela via Session State
if 'consultado' not in st.session_state:
    st.session_state.consultado = False
if 'matricula_id' not in st.session_state:
    st.session_state.matricula_id = ""

# 3. Interface Visual
# ADICIONADO LOGO E TÍTULO CORPORATIVO NO TOPO
st.image("https://upload.wikimedia.org/wikipedia/commons/6/63/Logo_grupo_3_cora%C3%A7%C3%B5es.png", width=180) # Link oficial do logo
st.markdown('<h2 style="text-align:center; color:#1e293b; font-weight:800; margin-bottom: 30px;">🏆 Portal de Premiação</h2>', unsafe_allow_html=True)

if df is not None:
    # TELA 1: LOGIN (Se não houver consulta ativa)
    if not st.session_state.consultado:
        # Título simplificado para o formulário
        col_login, _ = st.columns([1, 2])
        with col_login:
            with st.form("form_acesso"):
                st.markdown('<p style="color:#64748b; font-size:16px; margin-bottom: 20px;">Acompanhe os seus indicadores de performance</p>', unsafe_allow_html=True)
                acesso = st.text_input("Introduza a sua Matrícula:", placeholder="Ex: 1-49036")
                btn_acessar = st.form_submit_button("Consultar Premiação")
                
                if btn_acessar:
                    if acesso:
                        u_id = acesso.strip()
                        u_df = df[df['ID_BUSCA'] == u_id]
                        if not u_df.empty:
                            st.session_state.consultado = True
                            st.session_state.matricula_id = u_id
                            st.rerun() # Atualiza a tela instantaneamente
                        else:
                            st.error("Matrícula não encontrada no banco de dados.")
                    else:
                        st.warning("Por favor, digite a sua matrícula.")

    # TELA 2: RESULTADOS (Se a consulta foi realizada)
    else:
        u_df = df[df['ID_BUSCA'] == st.session_state.matricula_id]
        
        # Saudação pelo primeiro nome
        n_cols = [c for c in df.columns if 'NOME' in c]
        nome_f = str(u_df.iloc[0].get(n_cols[0], 'Colaborador'))
        st.subheader(f"Olá, {nome_f.split()[0]}! 👋")
        
        # Seletor de Mês (com busca inteligente de coluna)
        c_mes_col = [c for c in u_df.columns if 'M' in c and 'S' in c][0]
        m_sel = st.selectbox("Selecione o Mês:", u_df[c_mes_col].unique())
        r = u_df[u_df[c_mes_col] == m_sel].iloc[0]
        
        st.write("")

        # --- LINHA DE CARDS ---
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container(border=True):
                st.markdown('<p class="card-title">🎯 Aderência Roteiro</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Performance</span><span class="metric-highlight">{f_pc(r.get("A1",0))}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("A2",0))}</span></div>', unsafe_allow_html=True)
        
        with col2:
            with st.container(border=True):
                st.markdown('<p class="card-title">🏪 Loja do Coração</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Medalha</span><span class="metric-highlight">{r.get("L1","-")}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">P. Extra / Natural</span><span class="metric-value">{r.get("P1",0)} / {r.get("P2",0)}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Ruptura / MPDV</span><span class="metric-value">{r.get("P3",0)} / {r.get("P4",0)}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Nota</span><span class="metric-value">{r.get("L0", 0)}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("L2",0))}</span></div>', unsafe_allow_html=True)
        
        with col3:
            with st.container(border=True):
                st.markdown('<p class="card-title">📈 Sellout</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Meta</span><span class="metric-value">{f_nm(r.get("S1",0))}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Real</span><span class="metric-value">{f_nm(r.get("S2",0))}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Atingimento %</span><span class="metric-highlight">{f_pc(r.get("S3",0))}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><span class="metric-label">Prêmio</span><span class="metric-value">{f_rs(r.get("S4",0))}</span></div>', unsafe_allow_html=True)

        # --- TOTALIZADOR ---
        st.write("")
        st.markdown(f"""
            <div class="total-receber">
                <span style="font-size: 14px; opacity: 0.9; text-transform: uppercase; letter-spacing: 2px;">Valor Total a Receber</span><br>
                <span style="font-size: 38px; font-weight: 800;">{f_rs(r.get('TOT',0))}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # --- BLOCO DE OBSERVAÇÕES GERAIS ---
        texto_obs = str(r.get('OBS_GERAIS','')).strip()
        if texto_obs not in ['nan', '0', '', 'None']:
            st.write("")
            with st.container(border=True):
                st.markdown('<p class="card-title">📝 Notas da Liderança</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="obs-section">{texto_obs}</div>', unsafe_allow_html=True)
        
        # Botão para Voltar (Nova Consulta) no rodapé
        st.write("")
        col_voltar, _ = st.columns([1, 4])
        with col_voltar:
            if st.button("← Fazer Nova Consulta"):
                st.session_state.consultado = False
                st.rerun() # Atualiza a tela instantaneamente
else:
    st.info("Aguardando carregamento da base de dados (dados.csv)...")
