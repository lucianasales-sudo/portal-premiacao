import streamlit as st
import pandas as pd

# 1. Configuração de Estilo e Página
st.set_page_config(page_title="Portal de Premiação", layout="wide")

# CSS para o aspecto de sistema profissional
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #1e293b; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .card-header { font-weight: bold; color: #334155; border-bottom: 2px solid #e2e8f0; margin-bottom: 10px; padding-bottom: 5px; }
    .stSuccess { border-radius: 10px; padding: 20px; font-weight: bold; }
    .obs-box { background-color: #fffbeb; border: 1px solid #fef3c7; padding: 20px; border-radius: 10px; color: #92400e; }
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

        # MAPEAMENTO BUSCA SEGURA (Busca apenas parte da palavra para evitar erro de acento)
        c_nota = [c for c in df.columns if 'NOTA' in c and 'CORA' in c]
        if c_nota: df = df.rename(columns={c_nota[0]: 'L0'})
        
        # Busca por 'OBSERV' em qualquer lugar da coluna
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
st.title("🏆 Portal de Performance")
st.markdown("---")

if df is not None:
    c_busca1, _ = st.columns([1, 2])
    with c_busca1:
        acesso = st.text_input("Sua Matrícula:", placeholder="Ex: 1-49036")
    
    if acesso:
        u_df = df[df['ID_BUSCA'] == acesso.strip()]
        
        if not u_df.empty:
            row_zero = u_df.iloc[0]
            n_cols = [c for c in df.columns if 'NOME' in c]
            nome_f = str(row_zero.get(n_cols[0], 'Colaborador'))
            st.subheader(f"Olá, {nome_f.split()[0]}! 👋")
            
            c_mes_col = [c for c in u_df.columns if 'M' in c and 'S' in c][0]
            m_sel = st.selectbox("Selecione o Mês:", u_df[c_mes_col].unique())
            r = u_df[u_df[c_mes_col] == m_sel].iloc[0]
            
            st.write("")

            # --- CARDS PRINCIPAIS ---
            col1, col2, col3 = st.columns(3)
            with col1:
                with st.container(border=True):
                    st.markdown('<p class="card-header">🎯 ADERÊNCIA ROTEIRO</p>', unsafe_allow_html=True)
                    st.write(f"Performance: **{f_pc(r.get('A1',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('A2',0))}**")
            
            with col2:
                with st.container(border=True):
                    st.markdown('<p class="card-header">🏪 LOJA DO CORAÇÃO</p>', unsafe_allow_html=True)
                    st.write(f"Medalha: **{r.get('L1','-')}**")
                    st.write(f"Ponto Extra: **{r.get('P1',0)}** | Ponto Natural: **{r.get('P2',0)}**")
                    st.write(f"Ruptura: **{r.get('P3',0)}** | MPDV: **{r.get('P4',0)}**")
                    st.write(f"Nota: **{r.get('L0', 0)}**")
                    st.write(f"Prêmio: **{f_rs(r.get('L2',0))}**")
            
            with col3:
                with st.container(border=True):
                    st.markdown('<p class="card-header">📈 SELLOUT</p>', unsafe_allow_html=True)
                    st.write(f"Meta: **{f_nm(r.get('S1',0))}**")
                    st.write(f"Real: **{f_nm(r.get('S2',0))}**")
                    st.write(f"Ating %: **{f_pc(r.get('S3',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('S4',0))}**")

            st.write("")
            st.success(f"### **VALOR TOTAL A RECEBER: {f_rs(r.get('TOT',0))}**")
            
            # --- BLOCO DE OBSERVAÇÕES (FORÇADO) ---
            st.write("")
            # Pega o valor da coluna de observações
            texto_obs = str(r.get('OBS_GERAIS','')).strip()
            
            # Se o texto for diferente de vazio ou "nan"
            if texto_obs not in ['nan', '0', '', 'None']:
                with st.container(border=True):
                    st.markdown('<p class="card-header">📝 OBSERVAÇÕES GERAIS</p>', unsafe_allow_html=True)
                    st.info(texto_obs)
            else:
                # Caso queira que o bloco apareça mesmo vazio, descomente a linha abaixo:
                # st.write("Nenhuma observação para este período.")
                pass
        else:
            st.warning("Matrícula não encontrada.")
