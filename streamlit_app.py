import streamlit as st
import pandas as pd

# 1. Configurações da Página (Com ícone da marca)
st.set_page_config(page_title="Portal de Premiação | 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação e Limpeza (Para garantir R$ e % sem erros)
def formatar_reais(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0', '0,00', 'nan', 'NAN']:
        return "R$ 0,00"
    limpo = str(valor).replace('R', '').replace('$', '').replace('S', '').strip()
    return f"R$ {limpo}"

def formatar_pct(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0', '0%', 'nan', 'NAN']:
        return "0%"
    try:
        # Tenta tirar % e vírgula, converter e arredondar
        num = float(str(valor).replace('%', '').replace(',', '.'))
        return f"{int(num)}%" # Sem casas decimais
    except:
        return str(valor).strip()

def limpar_dado(valor):
    # Função simples para limpar textos
    if pd.isna(valor) or str(valor).strip() in ['nan', 'NAN', '0', '-']:
        return "-"
    return str(valor).strip()

# 2. Carregamento de Dados (Com cache para velocidade)
@st.cache_data
def carregar_dados():
    try:
        # Tenta UTF-8 (mais comum)
        try:
            df_local = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            # Se falhar, tenta Latin-1 (comum em arquivos do Excel br)
            df_local = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df_local.columns = [c.strip().upper() for c in df_local.columns]
        return df_local
    except Exception as e:
        return None

df = carregar_dados()

# --- INÍCIO DO APP ---
# Se o arquivo não carregar, avisa
if df is None:
    st.error("❌ Erro grave ao carregar a base de dados. Verifique o arquivo dados.csv no GitHub.")
    st.stop() # Para a execução aqui

# Garante que a coluna MATRÍCULA existe e é texto limpo
col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
df[col_mat] = df[col_mat].astype(str).str.strip()

# --- PÁGINA 1: ACESSO (Login Centralizado) ---
# Criamos colunas para centralizar o login
st.markdown("<br><br>", unsafe_allow_input_html=True) # Espaçamento topo
col_l, col_center, col_r = st.columns([1, 2, 1])

# Variável de acesso começa vazia
acesso = ""

with col_center:
    # Banner centralizado conforme desenho
    st.markdown('<div style="text-align: center;"><h1 style="background-color: #333; color: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">🏆 Portal de Premiação</h1></div>', unsafe_allow_input_html=True)
    st.write("") # Espaço
    
    # Caixa de Login Estilizada
    st.markdown('<div style="background-color: white; padding: 25px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); border: 1px solid #ddd; text-align: center;">', unsafe_allow_input_html=True)
    st.markdown('<h3 style="color: #333; margin-top: 0;">🔑 Acesso Restrito</h3>', unsafe_allow_input_html=True)
    
    # Campo de input (Removido st.caption para mobile e colocado st.info centralizado)
    acesso = st.text_input("👤 Digite sua MATRÍCULA:", placeholder="Ex: 1-46532", key="login_mat")
    st.markdown('</div>', unsafe_allow_input_html=True)
    
    if not acesso:
        st.write("")
        st.info("💡 **Dica:** Digite sua matrícula completa e pressione Enter para consultar.")

# --- PROCESSAMENTO DO ACESSO ---
if acesso:
    acesso = acesso.strip()
    
    # Visão ADMIN
    if acesso.upper() == "ADMIN":
        st.divider()
        st.subheader("📊 Painel Geral de Dados (Visão Admin)")
        st.dataframe(df, use_container_width=True)
        
    # Busca pela promotora
    else:
        dados_pessoais = df[df[col_mat] == acesso]
        
        # Se não achar, mostra erro e para
        if dados_pessoais.empty:
            st.write("")
            st.error(f"❌ Matrícula '{acesso}' não encontrada no sistema. Verifique o número.")
            st.stop()
            
        # --- PÁGINA 2: RESULTADOS (Visual Refinado) ---
        col_nome = [c for c in df.columns if 'NOME' in c][0]
        nome_promo = dados_pessoais.iloc[0][col_nome]
        
        # Saudação e Filtro
        st.write("")
        st.divider()
        st.header(f"Olá, {nome_promo}! 👋")
        
        # Garante meses limpos e únicos
        dados_pessoais['MÊS'] = dados_pessoais['MÊS'].astype(str).str.strip().str.upper()
        meses_unicos = dados_pessoais['MÊS'].unique()
        
        # Seletor de mês centralizado
        col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
        with col_m2:
            mes_sel = st.selectbox("📅 Selecione o mês de referência:", meses_unicos)
        
        # Busca a linha do mês selecionado
        info = dados_pessoais[dados_pessoais['MÊS'] == mes_sel].iloc[0]
        
        # Título da seção
        st.markdown("### 📊 Seus Indicadores de Performance")
        st.markdown("<br>", unsafe_allow_input_html=True)

        # --- EXIBIÇÃO DOS CARDS (Responsivo: 3 cols) ---
        c1, c2, c3 = st.columns(3)
        
        with c1:
            with st.container(border=True):
                st.markdown('<div style="background-color: #f0f0f0; padding: 10px; border-radius: 8px;"><h4 style="margin:0; color: #333; text-align:center;">🎯 ADERÊNCIA</h4></div>', unsafe_allow_input_html=True)
                st.write("")
                st.metric("Performance (Roteiro)", formatar_pct(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                # Prêmio estilizado
                p_ad = formatar_reais(info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))
                st.markdown(f'<p style="font-size: 18px; color: #28a745; font-weight: bold; text-align: center; margin-top: 15px;">💰 Prêmio: {p_ad}</p>', unsafe_allow_input_html=True)
        
        with c2:
            with st.container(border=True):
                st.markdown('<div style="background-color: #f0f0f0; padding: 10px; border-radius: 8px;"><h4 style="margin:0; color: #333; text-align:center;">🏪 LOJA DO CORAÇÃO</h4></div>', unsafe_allow_input_html=True)
                st.write("")
                med = limpar_dado(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                # Lógica de Emoji de Medalha
                emo = "⚪"
                if "Ouro" in med: emo = "🥇"
                elif "Prata" in med else "🥈" if "Bronze" in med else "🥉" if "Diamante" in med else "💎"
                
                # Exibição detalhada pedida
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.metric("📝 Nota:", limpar_dado(info.get('NOTA LOJA DO CORAÇÃO', '-')))
                with col
