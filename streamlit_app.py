import streamlit as st
import pandas as pd

# 1. Configuração Inicial
st.set_page_config(page_title="PAINEL PREMIAÇÃO", layout="wide")
st.header("🏆 PAINEL PREMIAÇÃO")

# Funções de Formatação
def f_rs(v):
    if pd.isna(v) or str(v).strip() in ['0','0,00','-','R$ -']: return "R$ 0,00"
    l = str(v).replace('R','').replace('$','').replace('S','').strip()
    return f"R$ {l}"

def f_pc(v):
    try:
        # Limpa string de porcentagem
        s = str(v).replace('%','').replace(',','.')
        n = float(s)
        return f"{int(n)}%"
    except: return "0%"

# 2. Carregamento de Dados
@st.cache_data
def load():
    try:
        # Leitura dos arquivos
        try: 
            d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        except: 
            d1 = pd.read_csv("dados.csv", sep=',', encoding='utf-8')
        
        try: 
            d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        except: 
            d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=',', encoding='utf-8')

        # Padroniza colunas para maiúsculo
        d1.columns = [c.strip().upper() for c in d1.columns]
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Mapeamento de nomes (De acordo com o seu arquivo enviado)
        m = {}
        m['PRODUTIVIDADE ADERENCIA ROTEIRO'] = 'A1'
        m['PREMIAÇÃO ADERENCIA ROTEIRO'] = 'A2'
        m['MEDALHA LOJA DO CORAÇÃO'] = 'L1'
        m['PREMIAÇÃO MEDALHA LC'] = 'L2'
        m['AING SELLOUT %'] = 'S3'
        m['PREMIAÇÃO SELLOUT'] = 'S4'
        m['TOTAL A RECEBER'] = 'TOT'
        m['PONTO EXTRA'] = 'P1'
        m['PONTO NATURAL'] = 'P2'
        m['RUPTURA'] = 'P3'
        m['MPDV'] = 'P4'
        m['MÃŠS'] = 'MÊS' # Correção de encoding comum
        
        d1 = d1.rename(columns=m)

        # Busca segura da Matrícula (Evita IndexError)
        c_m1 = [c for c in d1.columns if 'MATRIC' in c]
        k1 = c_m1[0] if c_m1 else d1.columns[0]
        
        c_m2 = [c for c in d2.columns if 'MATRIC' in c]
        k2 = c_m2[0] if c_m2 else d2.columns[0]
        
        # Cria ID único como texto limpo
        d1['ID'] = d1[k1].astype(str).str.strip()
        d2['ID'] = d2[k2].astype(str).str.strip()
        
        return pd.merge(d1, d2, on='ID', how='left')
    except Exception as e:
        st.error(f"Erro no processamento: {e}")
        return None

df = load()

# 3. Interface do Usuário
if df is not None:
    st.divider()
    acesso = st.text_input("DIGITE SUA MATRÍCULA:", placeholder="Ex: 1-49036")
    
    if acesso:
        u_id = acesso.strip()
        u_df = df[df['ID'] == u_id]
        
        if not u_df.empty:
            # Identifica coluna de nome
            n_cols = [c for c in df.columns if 'NOME' in c]
            nome_f = str(u_df.iloc[0].get(n_cols[0], 'Colaborador'))
            st.subheader(f"Olá, {nome_f.split()[0]}! 👋")
            
            # Seleção de Mês
            col_mes = 'MÊS' if 'MÊS' in u_df.columns else u_df.columns[0]
            lista_m = u_df[col_mes].unique()
            m_sel = st.selectbox("SELECIONE O MÊS:", lista_m)
            
            # Dados do mês selecionado
            r = u_df[u_df[col_mes] == m_sel].iloc[0]
            
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
                    # Novos Campos que você pediu
                    st.write(f"P. Extra: **{r.get('P1',0)}**")
                    st.write(f"P. Natural: **{r.get('P2',0)}**")
                    st.write(f"Ruptura: **{r.get('P3',0)}**")
                    st.write(f"MPDV: **{r.get('P4',0)}**")
                    st.write(f"Prêmio: **{f_rs(r.get('L2',0))}**")
            
            with c3:
                with st.container(border=True):
                    st.write("**📈 SELLOUT**")
                    st.write(f"Ating: **{f_pc(r.get('S3',0))}**")
                    st.write(f"Prêmio: **{f_rs(r.get('S4',0))}**")

            st.divider()
            st.success(f"🏆 TOTAL A RECEBER: {f_rs(r.get('TOT',0))}")
            
            # Observações
            obs = str(r.get('OBSERVAÇÕES GERAIS','')).strip()
            if obs not in ['nan','0','','None']:
                with st.expander("📝 Notas Importantes"):
                    st.write(obs)
        else:
            st.warning(f"Matrícula {u_id} não encontrada.")
else:
    st.info("Carregando base de dados...")
