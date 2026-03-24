import streamlit as st
import pandas as pd

# 1. Configuração e Título
st.set_page_config(page_title="PAINEL PREMIAÇÃO", layout="wide")
st.header("🏆 PAINEL PREMIAÇÃO")

# Funções de Formatação
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','R$ -']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

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
        # Tenta carregar os arquivos
        try: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: d1 = pd.read_csv("dados.csv", sep=',', encoding='utf-8')
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=',', encoding='utf-8')

        d1.columns = [c.strip().upper() for c in d1.columns]
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Mapeamento Seguro (Busca por palavras-chave para evitar erro de acento)
        # NOTA LOJA DO CORACAO -> L0
        c_nota = [c for c in d1.columns if 'NOTA' in c and 'CORA' in c]
        if c_nota: d1 = d1.rename(columns={c_nota[0]: 'L0'})

        # Outros mapeamentos
        m = {
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'A1', 'PREMIAÇÃO ADERENCIA ROTEIRO': 'A2',
            'MEDALHA LOJA DO CORAÇÃO': 'L1', 'PREMIAÇÃO MEDALHA LC': 'L2',
            'AING SELLOUT %': 'S3', 'PREMIAÇÃO SELLOUT': 'S4',
            'TOTAL A RECEBER': 'TOT', 'PONTO EXTRA': 'P1',
            'PONTO NATURAL': 'P2', 'RUPTURA': 'P3', 'MPDV': 'P4'
        }
        d1 = d1.rename(columns=m)

        # Matrícula
        c_m1 = [c for c in d1.columns if 'MATRIC' in c]
        k1 = c_m1[0] if c_m1 else d1.columns[0]
        c_m2 = [c for c in d2.columns if 'MATRIC' in c]
        k2 = c_m2[0] if c_m2 else d2.columns[0]
        
        d1['ID'] = d1[k1].astype(str).str.strip()
        d2['ID'] = d2[k2].astype(str).str.strip()
        
        return pd.merge(d1, d2, on='ID', how='left')
    except Exception as e:
        st.error(f"Erro ao processar: {e}")
        return None

df = load()

# 3. Interface
if df is not None:
    st.divider()
    acesso = st.text_input("MATRÍCULA:", placeholder="Ex: 1-49036")
    
    if acesso:
        u_id = acesso.strip()
        u_df = df[df['ID'] == u_id]
        
        if not u_df.empty:
            # Saudação
            n_cols = [c for c in df.columns if 'NOME' in c]
            nome_f = str(u_df.iloc[0].get(n_cols[0], 'Colaborador'))
            st.subheader(f"Olá, {nome_f.split()[0]}! 👋")
            
            # Seletor de Mês (Corrige bug de encoding no nome da coluna Mês)
            c_mes = [c for c in u_df.columns if 'M' in c and 'S' in c][0]
            m_sel = st.selectbox("MÊS:", u_df[c_mes].unique())
            r = u_df[u_df[c_mes] == m_sel].iloc[0]
            
            st.write("### Meus Indicadores")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("**🎯 ADERÊNCIA**")
                    st.write(f"Perf: **{f_pc(r.get('A1',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('A2',0))}**")
            
            with c2:
                with st.container(border=True):
                    st.write("**🏪 LOJA DO CORAÇÃO**")
                    st.write(f"Medalha: **{r.get('L1','-')}**")
                    # Detalhamento
                    st.write(f"P. Extra: **{r.get('P1',0)}**")
                    st.write(f"P. Natural: **{r.get('P2',0)}**")
                    st.write(f"Ruptura: **{r.get('P3',0)}**")
                    st.write(f"MPDV: **{r.get('P4',0)}**")
                    # Nota e Prêmio
                    st.write(f"Nota: **{r.get('L0', 0)}**")
                    st.write(f"Prêmio: **{f_rs(r.get('L2',0))}**")
            
            with c3:
                with st.container(border=True):
                    st.write("**📈 SELLOUT**")
                    st.write(f"Ating: **{f_pc(r.get('S3',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('S4',0))}**")

            st.divider()
            st.success(f"🏆 TOTAL A RECEBER: {f_rs(r.get('TOT',0))}")
        else:
            st.warning("Matrícula não encontrada.")
