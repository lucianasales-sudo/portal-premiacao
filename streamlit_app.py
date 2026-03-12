import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal de Premiação | 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação
def formatar_reais(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0', '0,00', 'nan', 'NAN']:
        return "R$ 0,00"
    limpo = str(valor).replace('R', '').replace('$', '').replace('S', '').replace('s', '').strip()
    return f"R$ {limpo}"

def formatar_pct(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0', '0%', 'nan', 'NAN']:
        return "0%"
    try:
        num = float(str(valor).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
    except:
        return str(valor).strip()

def limpar_dado(valor):
    if pd.isna(valor) or str(valor).strip() in ['nan', 'NAN', '0', '-']:
        return "-"
    return str(valor).strip()

# 2. Carregamento de Dados
@st.cache_data
def carregar_dados():
    try:
        try:
            df_local = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df_local = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df_local.columns = [c.strip().upper() for c in df_local.columns]
        return df_local
    except:
        return None

df = carregar_dados()

if df is None:
    st.error("❌ Erve ao carregar dados.csv")
    st.stop()

col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
df[col_mat] = df[col_mat].astype(str).str.strip()

# --- PÁGINA 1: ACESSO (Login Centralizado) ---
# Usando st.write para dar o espaço que o markdown falhou
st.write("#") 
st.write("#")

col_l, col_center, col_r = st.columns([1, 2, 1])

with col_center:
    # Título estilizado sem usar markdown complexo na mesma linha
    st.markdown('<h1 style="text-align: center; background-color: #333; color: white; padding: 20px; border-radius: 10px;">🏆 Portal de Premiação</h1>', unsafe_allow_input_html=True)
    
    st.write("") 
    
    with st.container(border=True):
        st.subheader("🔑 Acesso Restrito")
        acesso = st.text_input("👤 MATRÍCULA:", placeholder="Ex: 1-46532")
    
    if not acesso:
        st.info("💡 Digite sua matrícula e pressione Enter para consultar seus prêmios.")

# --- PÁGINA 2: RESULTADOS ---
if acesso:
    acesso = acesso.strip()
    if acesso.upper() == "ADMIN":
        st.divider()
        st.dataframe(df, use_container_width=True)
    else:
        dados_pessoais = df[df[col_mat] == acesso]
        
        if dados_pessoais.empty:
            st.write("")
            st.error(f"Matrícula '{acesso}' não encontrada.")
        else:
            col_nome = [c for c in df.columns if 'NOME' in c][0]
            nome_promo = dados_pessoais.iloc[0][col_nome]
            
            st.divider()
            st.header(f"Olá, {nome_promo}! 👋")
            
            # Limpeza de Mês
            dados_pessoais['MÊS'] = dados_pessoais['MÊS'].astype(str).str.strip().str.upper()
            
            # Seletor de mês centralizado
            c_m1, c_m2, c_m3 = st.columns([1, 1, 1])
            with c_m2:
                mes_sel = st.selectbox("📅 Selecione o mês:", dados_pessoais['MÊS'].unique())
            
            info = dados_pessoais[dados_pessoais['MÊS'] == mes_sel].iloc[0]
            
            st.markdown("### 📊 Seus Indicadores")
            
            # CARDS DE RESULTADOS
            c1, c2, c3 = st.columns(3)
            
            with c1:
                with st.container(border=True):
                    st.write("🎯 **ADERÊNCIA**")
                    st.metric("Performance", formatar_pct(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.success(f"💰 Prêmio: {formatar_reais(info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}")
            
            with c2:
                with st.container(border=True):
                    st.write("🏪 **LOJA DO CORAÇÃO**")
                    med = limpar_dado(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                    
                    # Lógica da Medalha
                    emo = "🏅"
                    if "Ouro" in med: emo = "🥇"
                    elif "Prata" in med: emo = "🥈"
                    elif "Bronze" in med: emo = "🥉"
                    elif "Diamante" in med: emo = "💎"
                    
                    col_i1, col_i2 = st.columns(2)
                    col_i1.metric("Nota", limpar_dado(info.get('NOTA
