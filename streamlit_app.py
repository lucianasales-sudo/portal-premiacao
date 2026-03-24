import streamlit as st
import pandas as pd

# 1. Configuração de Design Premium
st.set_page_config(page_title="Portal de Premiação | Corporativo", layout="wide")

# CSS Customizado para visual moderno
st.markdown("""
    <style>
    /* Estilização dos Cards */
    [data-testid="stMetricValue"] { font-size: 24px; color: #1E3A8A; }
    [data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }
    /* Estilo do Título Principal */
    .main-title { font-size: 32px; font-weight: 800; color: #1e293b; margin-bottom: 20px; }
    /* Ajuste de Success Box */
    .stSuccess { background-color: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
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
        try: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: d1 = pd.read_csv("dados.csv", sep=',', encoding='utf-8')
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=',', encoding='utf-8')
        
        d1.columns = [c.strip().upper() for c in d1.columns]
        d2.columns = [c.strip().upper() for c in d2.columns]

        c_nota = [c for c in d1.columns if 'NOTA' in c and 'CORA' in c]
        if c_nota: d1 = d1.rename(columns={c_nota[0]: 'L0'})

        m = {
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'A1', 'PREMIAÇÃO ADERENCIA ROTEIRO': 'A2',
            'MEDALHA LOJA DO CORAÇÃO': 'L1', 'PREMIAÇÃO MEDALHA LC': 'L2',
            'META SELLOUT': 'S1', 'REAL SELLOUT': 'S2',
            'AING SELLOUT %': 'S3', 'PREMIAÇÃO SELLOUT': 'S4',
            'TOTAL A RECEBER': 'TOT', 'PONTO EXTRA': 'P1',
            'PONTO NATURAL': 'P2', 'RUPTURA': 'P3', 'MPDV': 'P4'
        }
        d1 = d1.rename(columns=m)

        c_m1 = [c for c in d1.columns if 'MATRIC' in c]
        k1 = c_m1[0] if c_m1 else d1.columns[0]
        c_m2 = [c for c in d2.columns if 'MATRIC' in c]
        k2 = c_m2[0] if c_m2 else d2.columns[0]
        
        d1['ID'] = d1[k1].astype(str).str.strip()
        d2['ID'] = d2[k2].astype(str).str.strip()
        
        return pd.merge(d1, d2, on='ID', how='left')
    except Exception as e:
        st.error(f"Erro no processamento: {e}")
        return None

df = load()

# 3. Cabeçalho Corporativo
st.markdown('<p class="main-title">🏆 Portal de Reconhecimento</p>', unsafe_allow_html=True)

if df is not None:
    # Barra lateral ou topo para filtros
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
        st.title("Acesso Restrito")
        acesso = st.text_input("Sua Matrícula:", placeholder="0-00000")
        st.divider()
        st.info("Consulte seus indicadores e metas mensais.")

    if acesso:
        u_id = acesso.strip()
        u_df = df[df['ID'] == u_id]
        
        if not u_df.empty:
            n_cols = [c for c in df.columns if 'NOME' in c]
            nome_f = str(u_df.iloc[0].get(n_cols[0], 'Colaborador'))
            
            st.markdown(f"### Bem-vindo, **{nome_f.split()[0]}**! 👋")
            
            c_mes = [c for c in u_df.columns if 'M' in c and 'S' in c][0]
            m_sel = st.selectbox("Selecione o Ciclo/Mês:", u_df[c_mes].unique())
            r = u_df[u_df[c_mes] == m_sel].iloc[0]
            
            st.divider()

            # --- LINHA 1: DASHBOARD ---
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.metric(label="🎯 ADERÊNCIA ROTEIRO", value=f_pc(r.get('A1',0)))
                st.caption(f"💰 Prêmio Aderência: {f_rs(r.get('A2',0))}")
            
            with c2:
                # Medalha ganha destaque visual
                medalha = r.get('L1','-')
                st.metric(label="🏪 MEDALHA LC", value=medalha)
                st.caption(f"Nota: {r.get('L0', 0)} | 💰 Prêmio: {f_rs(r.get('L2',0))}")
            
            with c3:
                st.metric(label="📈 ATING. SELLOUT", value=f_pc(r.get('S3',0)))
                st.caption(f"💰 Prêmio Sellout: {f_rs(r.get('S4',0))}")

            # --- LINHA 2: DETALHAMENTO ---
            st.write("#### 📊 Detalhamento de Performance")
            d_c1, d_c2, d_c3 = st.columns([1, 1, 1])

            with d_c1:
                with st.expander("Metas Sellout", expanded=True):
                    st.write(f"**Meta:** {f_nm(r.get('S1',0))}")
                    st.write(f"**Real:** {f_nm(r.get('S2',0))}")

            with d_c2:
                with st.expander("Critérios Loja do Coração", expanded=True):
                    st.write(f"📍 Ponto Extra: **{r.get('P1',0)}**")
                    st.write(f"📍 Ponto Natural: **{r.get('P2',0)}**")
            
            with d_c3:
                with st.expander("Execução de Loja", expanded=True):
                    st.write(f"⚠️ Ruptura: **{r.get('P3',0)}**")
                    st.write(f"🖼️ MPDV: **{r.get('P4',0)}**")

            # --- RODAPÉ DE RESULTADO ---
            st.markdown("---")
            st.success(f"### **Total a Receber: {f_rs(r.get('TOT',0))}**")
            
            obs = str(r.get('OBSERVAÇÕES GERAIS','')).strip()
            if obs not in ['nan','0','','None']:
                st.info(f"**Mensagem da Liderança:** {obs}")

        else:
            st.warning("Matrícula não encontrada no sistema de RH.")
else:
    st.error("Falha na conexão com o banco de dados (CSV).")
