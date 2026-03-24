import streamlit as st
import pandas as pd

# 1. Configuração e Título (Sempre visíveis)
st.set_page_config(page_title="PAINEL", layout="wide")
st.header("🏆 PAINEL PREMIAÇÃO")

# Funções Curtas
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_pc(v):
    try:
        n = float(str(v).replace('%','').replace(',','.'))
        return f"{int(n)}%"
    except: return "0%"

# 2. Carregamento com Aviso de Erro
@st.cache_data
def load():
    try:
        # Tenta carregar os dois arquivos
        try: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')

        d1.columns = [c.strip().upper() for c in d1.columns]
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Apelidos para os indicadores (P1, P2, P3, P4 são os novos)
        m_map = {
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'A1',
            'PREMIAÇÃO ADERENCIA ROTEIRO': 'A2',
            'MEDALHA LOJA DO CORAÇÃO': 'L1',
            'PREMIAÇÃO MEDALHA LC': 'L2',
            'META SELLOUT': 'S1',
            'REAL SELLOUT': 'S2',
            'AING SELLOUT %': 'S3',
            'PREMIAÇÃO SELLOUT': 'S4',
            'TOTAL A RECEBER': 'TOT',
            'PONTO EXTRA': 'P1',
            'PONTO NATURAL': 'P2',
            'RUPTURA': 'P3',
            'MPDV': 'P4'
        }
        d1 = d1.rename(columns=m_map)

        # Acha a coluna de matrícula
        k1 = [c for c in d1.columns if 'MATRIC' in c][0]
        k2 = [c for c in d2.columns if 'MATRIC' in c][0]
        
        d1 = d1.rename(columns={k1: 'ID'})
        d2 = d2.rename(columns={k2: 'ID'})
        
        d1.ID = d1.ID.astype(str).str.strip()
        d2.ID = d2.ID.astype(str).str.strip()
        
        return pd.merge(d1, d2, on='ID', how='left')
    except Exception as e:
        # Se der erro, mostra na tela o motivo
        st.error(f"Erro ao carregar dados: {e}")
        return None

df = load()

# 3. Interface de busca
if df is not None:
    st.divider()
    acesso = st.text_input("DIGITE SUA MATRÍCULA:", placeholder="Ex: 1-49174")
    
    if acesso:
        u_id = acesso.strip()
        u_df = df[df.ID == u_id]
        
        if not u_df.empty:
            r_ini = u_df.iloc[0]
            n_col = [c for c in df.columns if 'NOME' in c][0]
            nome = str(r_ini.get(n_col, 'Colaborador')).split()[0]
            st.subheader(f"Olá, {nome}!")
            
            m_s = st.selectbox("MÊS:", u_df['MÊS'].unique())
            r = u_df[u_df['MÊS'] == m_s].iloc[0]
            
            # --- CARDS DE INDICADORES ---
            st.write("### Indicadores")
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
                    # Novos Campos
                    st.write(f"P.Extra: **{f_pc(r.get('P1',0))}**")
                    st.write(f"P.Natural: **{f_pc(r.get('P2',0))}**")
                    st.write(f"Ruptura: **{f_pc(r.get('P3',0))}**")
                    st.write(f"MPDV: **{f_pc(r.get('P4',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('L2',0))}**")
            
            with c3:
                with st.container(border=True):
                    st.write("**📈 SELLOUT**")
                    st.write(f"Ating: **{f_pc(r.get('S3',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('S4',0))}**")

            st.divider()
            st.success(f"🏆 TOTAL: {f_rs(r.get('TOT',0))}")
        else:
            st.warning("Matrícula não encontrada.")
else:
    st.info("Aguardando carregamento dos arquivos CSV...")
