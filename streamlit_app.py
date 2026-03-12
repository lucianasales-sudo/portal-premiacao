import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_icon="☕")

# Estilo para centralizar tudo
st.markdown("""
<style>
.stMetric, .stMetricValue, .stMetricLabel, .central {
    text-align: center !important; display: flex;
    flex-direction: column; align-items: center;
}
.pr-txt { color: #28a745; font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_input_html=True)

def f_rs(v):
    if pd.isna(v) or str(v) in ['0','0,00','-']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-']: return "0"
    l = str(v).replace('R','').replace('$','').strip()
    return l

def f_pc(v):
    try:
        n = float(str(v).replace('%','').replace(',','.'))
        return f"{int(n)}%"
    except: return "0%"

@st.cache_data
def load():
    try:
        df = pd.read_csv("dados.csv", encoding='utf-8')
    except:
        df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
    df.columns = [c.strip().upper() for c in df.columns]
    return df

df = load()
if df is not None:
    st.markdown("<h1 class='central'>🏆 Portal</h1>", True)
    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()
    
    _, col_l, _ = st.columns([1, 1, 1])
    with col_l:
        acesso = st.text_input("MATRÍCULA:", placeholder="Digite aqui")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            c_n = [c for c in df.columns if 'NOME' in c][0]
            nome = u_df.iloc[0][c_n]
            st.markdown(f"<h2 class='central'>Olá, {nome}</h2>", True)
            u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
            
            _, col_m, _ = st.columns([1, 1, 1])
            with col_m:
                m_sel = st.selectbox("Mês:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("**🎯 ADERÊNCIA**")
                    st.metric("Perf.", f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.write(f"💰 {f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}")
            with c2:
                with st.container(border=True):
                    st.write("**🏪 LOJA**")
                    st.metric("Medalha", str(r.get('MEDALHA LOJA DO CORAÇÃO', '-')))
                    st.write(f"💰 {f_rs(r.get('PREMIAÇÃO MEDALHA LC', 0))}")
            with c3:
                with st.container(border=True):
                    st.write("**📈 SELLOUT**")
                    ca, cb = st.columns(2)
                    ca.metric("Meta", f_nm(r.get('META SELLOUT', 0)))
                    cb.metric("Real", f_nm(r.get('REAL SELLOUT', 0)))
                    st.metric("Ating.", f_pc(r.get('AING SELLOUT %', 0)))
                    st.write(f"💰 {f_rs(r.get('PREMIAÇÃO SELLOUT', 0))}")
            
            st.divider()
            tt = f_rs(r.get('TOTAL A RECEBER', '0,00'))
            st.success(f"🏆 TOTAL: {tt}")
            
            obs = r.get('OBSERVAÇÕES GERAIS', '')
            if pd.notna(obs) and str(obs).strip() not in ['0','','nan']:
                st.info(f"💡 Obs: {obs}")
        else:
            st.error("Não encontrado.")
