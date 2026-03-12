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
        try:
            df_local = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df_local = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df_local.columns = [c.strip().upper() for c in df_local.columns]
        return df_local
    except:
        return None

df = load()

if df is not None:
    # Cabeçalho Nativo (Seguro contra TypeError)
    st.title("🏆 Portal de Premiação")
    st.divider()

    c_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[c_mat] = df[c_mat].astype(str).str.strip()
    
    # Login e Filtro (Centralização por colunas nativas)
    _, c_log, _ = st.columns([1.5, 1, 1.5])
    with c_log:
        acesso = st.text_input("MATRÍCULA:", placeholder="Ex: 1-49174")
    
    if acesso:
        u_df = df[df[c_mat] == acesso.strip()]
        if not u_df.empty:
            # Saudação
            nome_col = [c for c in df.columns if 'NOME' in c][0]
            st.subheader(f"Olá, {u_df.iloc[0][nome_col]}! 👋")
            
            # Seletor de Mês
            _, c_m, _ = st.columns([1.5, 1, 1.5])
            with c_m:
                u_df['MÊS'] = u_df['MÊS'].astype(str).str.upper()
                m_sel = st.selectbox("MÊS DE REFERÊNCIA:", u_df['MÊS'].unique())
            
            r = u_df[u_df['MÊS'] == m_sel].iloc[0]
            
            # --- ÁREA DE INDICADORES (Design Harmônico Nativo) ---
            st.write("### 📊 Seus Indicadores")
            
            # Criamos os cards usando containers com borda (Nativos e estáveis)
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("🎯 **ADERÊNCIA**")
                    st.metric("Performance", f_pc(r.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.write(f"💰 Prêmio: **{f_rs(r.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
            
            with c2:
                with st.container(border=True):
                    st.write("🏪 **LOJA DO CORAÇÃO**")
                    st.metric("Medalha", str(r.get('MEDALHA LOJA DO CORAÇÃO', '-')))
                    st.write(f"💰 Prêmio: **{f_rs(r.get('PREMIAÇÃO MEDALHA LC', 0))}**")
            
            with c3:
                with st.container(border=True):
                    st.write("📈 **SELLOUT**")
                    # Meta e Real em texto simples para segurança
                    meta_v = f_nm(r.get('META SELLOUT', 0))
                    real_v = f_nm(r.get('REAL SELLOUT', 0))
                    st.caption(f"Meta: {meta_v} | Real: {real_v}")
                    st.metric("Atingimento", f_pc(r.get('AING SELLOUT %', 0)))
                    st.write(f"💰 Prêmio: **{f_rs(r.get('PREMIAÇÃO SELLOUT', 0))}**")

            # --- TOTALIZADOR (Versão Blindada) ---
            st.divider()
            total_final = f_rs(r.get('TOTAL A RECEBER', 0))
            
            # Usando st.success que é um componente nativo com fundo verde e ícone
            st.success(f"## 🏆 TOTAL A RECEBER: {total_final}")
            
            # Notas e Observações
            obs = str(r.get('OBSERVAÇÕES GERAIS', '')).strip()
            if obs not in ['nan', '0', '', 'None']:
                with st.expander("📝 Notas e Observações Gerais", expanded=True):
                    st.write(obs)
        else:
            st.error("Matrícula não encontrada.")
