import streamlit as st
import pandas as pd

# 1. Configurações de Design
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação Seguras
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','nan']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_nm(v):
    if pd.isna(v) or str(v) in ['0','-','nan']: return "0"
    l = str(v).replace('R','').replace('$','').strip()
    return l

def f_pc(v):
    try:
        n = float(str(v).replace('%','').replace(',','.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Carregamento de Dados
@st.cache_data
def load():
    try:
        try: df = pd.read_csv("dados.csv", encoding='utf-8')
        except: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except: return None

df = load()

if df is not None:
    # --- CABEÇALHO NATIVO (Sem HTML para evitar TypeError) ---
    st.header("🏆 Portal de Premiação")
    st.divider()

    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()
    
    # Login e Mês (Lado a lado no computador, empilhados no celular)
    col_l, col_m = st.columns(2)
    with col_l:
        acesso = st.text_input("MATRÍCULA:", placeholder="Ex: 1-49174")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            # Saudação Curta (Pega só o primeiro nome)
            nome_completo = u_df.iloc[0][[c for c in df.columns if 'NOME' in c][0]]
            p_nome = str(nome_completo).split()[0]
            st.subheader(f"Olá, {p_nome}! 👋")
            
            with col_m:
                u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
                m_sel = st.selectbox("MÊS:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            # --- ÁREA DE INDICADORES ---
            st.write("### 📊 Indicadores")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("**🎯 ADERÊNCIA**")
                    st.metric("Perf.", f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.write(f"Prêmio: **{f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
            
            with c2:
                with st.container(border=True):
                    st.write("**🏪 LOJA**")
                    st.metric("Medalha", str(r.get('MEDALHA LOJA DO CORAÇÃO', '-')))
                    st.write(f"Prêmio: **{f_rs(r.get('PREMIAÇÃO MEDALHA LC', 0))}**")
            
            with c3:
                with st.container(border=True):
                    st.write("**📈 SELLOUT**")
                    m_val = f_nm(r.get('META SELLOUT', 0))
                    r_val = f_nm(r.get('REAL SELLOUT', 0))
                    st.write(f"M: {m_val} | R: {r_val}")
                    st.metric("Ating.", f_pc(r.get('AING SELLOUT %', 0)))
                    st.write(f"Prêmio: **{f_rs(r.get('PREMIAÇÃO SELLOUT', 0))}**")

            # --- TOTALIZADOR NATIVO (Otimizado para Mobile) ---
            st.divider()
            total_final = f_rs(r.get('TOTAL A RECEBER', 0))
            
            # O st.success é o componente mais estável para destacar o valor final
            st.success(f"🏆 TOTAL: {total_final}")
            
            # Observações
            obs = str(r.get('OBSERVAÇÕES GERAIS', '')).strip()
            if obs not in ['nan', '0', '', 'None']:
                with st.expander("📝 Notas", expanded=False):
                    st.write(obs)
        else:
            st.error("Matrícula não encontrada.")
