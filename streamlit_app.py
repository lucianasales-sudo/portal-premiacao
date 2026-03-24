import streamlit as st
import pandas as pd

# 1. Configurações
st.set_page_config(page_title="PAINEL PREMIAÇÃO", layout="wide", page_icon="☕")

# Funções de Formatação
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','nan']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-','nan']: return "0"
    return str(v).replace('R','').replace('$','').strip()

def f_pc(v):
    try:
        n = float(str(v).replace('%','').replace(',','.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Carregamento de Dados (2 Arquivos)
@st.cache_data
def load_data():
    try:
        # Base Principal
        try: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        except: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        d1.columns = [c.strip().upper() for c in d1.columns]

        # Base Secundária
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Mapeamento para nomes curtos (Evita SyntaxError)
        d1 = d1.rename(columns={
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'AD_P',
            'PREMIAÇÃO ADERENCIA ROTEIRO': 'AD_V',
            'MEDALHA LOJA DO CORAÇÃO': 'LC_M',
            'PREMIAÇÃO MEDALHA LC': 'LC_V',
            'META SELLOUT': 'SO_M',
            'REAL SELLOUT': 'SO_R',
            'AING SELLOUT %': 'SO_A',
            'PREMIAÇÃO SELLOUT': 'SO_V',
            'TOTAL A RECEBER': 'TOTAL'
        })

        c1 = 'MATRÍCULA' if 'MATRÍCULA' in d1.columns else d1.columns[0]
        c2 = 'MATRÍCULA' if 'MATRÍCULA' in d2.columns else d2.columns[0]
        
        d1[c1] = d1[c1].astype(str).str.strip()
        d2[c2] = d2[c2].astype(str).str.strip()

        return pd.merge(d1, d2, left_on=c1, right_on=c2, how='left')
    except: return None

df = load_data()

if df is not None:
    st.header("🏆 PAINEL PREMIAÇÃO")
    st.divider()

    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    
    col_l, col_m = st.columns(2)
    with col_l:
        acesso = st.text_input("MATRÍCULA:", placeholder="Ex: 1-49174")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            nome_c = [c for c in df.columns if 'NOME' in c][0]
            p_nome = str(u_df.iloc[0][nome_c]).split()[0]
            st.subheader(f"Olá, {p_nome}! 👋")
            
            with col_m:
                u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
                m_sel = st.selectbox("MÊS:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            # --- ÁREA DE INDICADORES (Nomes curtos = Linhas curtas) ---
            st.write("### Indicadores")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("🎯 **ADERÊNCIA**")
                    st.write(f"Perf: **{f_pc(r.get('AD_P',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('AD_V',0))}**")
            
            with c2:
                with st.container(border=True):
                    st.write("🏪 **LOJA DO CORAÇÃO**")
                    st.write(f"Medalha: **{r.get('LC_M','-')}**")
                    # Dado da 2ª planilha (ajuste o nome da coluna se necessário)
                    st.write(f"Status: **{r.get('STATUS','Sem info')}**")
                    st.write(f"Prêmio: **{f_rs(r.get('LC_V',0))}**")
            
            with c3:
                with st.container(border=True):
                    st.write("📈 **SELLOUT**")
                    st.write(f"Meta: {f_nm(r.get('SO_M',0))} | Real: {f_nm(r.get('SO_R',0))}")
                    st.write(f"Ating: **{f_pc(r.get('SO_A',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('SO_V',0))}**")

            st.divider()
            val_tt = f_rs(r.get('TOTAL', 0))
            st.success(f"🏆 TOTAL: {val_tt}")
            
            obs = str(r.get('OBSERVAÇÕES GERAIS', '')).strip()
            if obs not in ['nan', '0', '', 'None']:
                with st.expander("📝 Notas", expanded=False):
                    st.write(obs)
        else:
            st.error("Matrícula não encontrada.")
