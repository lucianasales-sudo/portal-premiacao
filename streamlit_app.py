import streamlit as st
import pandas as pd

# 1. Configuração que força o layout a usar a largura total da tela
st.set_page_config(
    page_title="Portal 3 Corações", 
    layout="wide", 
    page_icon="☕",
    initial_sidebar_state="collapsed" # Começa fechado no mobile para dar foco aos dados
)

# Funções de Formatação
def formatar_reais(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0', '0,00']:
        return "R$ 0,00"
    limpo = str(valor).replace('R', '').replace('$', '').strip()
    return f"R$ {limpo}"

def formatar_pct(valor):
    try:
        num = float(str(valor).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
    except:
        return str(valor)

# 2. Carregamento de Dados
@st.cache_data # Isso faz o app carregar muito mais rápido no celular
def carregar():
    try:
        try:
            df_local = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df_local = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df_local.columns = [c.strip().upper() for c in df_local.columns]
        return df_local
    except Exception as e:
        return None

df = carregar()

if df is not None:
    # Cabeçalho Adaptativo
    st.title("🏆 Portal de Premiação")
    
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    # Login na Sidebar (No mobile fica escondido no menu hambúrguer superior esquerdo)
    with st.sidebar:
        st.header("🔑 Acesso")
        acesso = st.text_input("Sua MATRÍCULA:", placeholder="Ex: 1-46532")
        st.caption("Digite sua matrícula e pressione Enter.")

    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN":
            st.subheader("📊 Painel Geral")
            st.dataframe(df, use_container_width=True)
        else:
            dados = df[df[col_mat] == acesso]
            if not dados.empty:
                col_n = [c for c in df.columns if 'NOME' in c][0]
                nome_promo = dados.iloc[0][col_n]
                
                # Saudação com destaque
                st.subheader(f"Olá, {nome_promo}! 👋")
                
                # Filtro de Mês em destaque
                dados['MÊS'] = dados['MÊS'].astype(str).str.strip().str.upper()
                mes_sel = st.selectbox("📅 Selecione o mês de referência:", dados['MÊS'].unique())
                
                info = dados[dados['MÊS'] == mes_sel].iloc[0]
                
                st.markdown("---")
                
                # --- LAYOUT DE COLUNAS (Responsivo) ---
                # No Desktop: 3 colunas. No Mobile: 1 coluna por linha automaticamente.
                c1, c2, c3 = st.columns([1, 1, 1])
                
                with c1:
                    with st.container(border=True):
                        st.markdown("🎯 **ADERÊNCIA**")
                        st.metric("Performance", formatar_pct(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                        st.markdown(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
                
                with c2:
                    with st.container(border=True):
                        st.markdown("🏪 **LOJA DO CORAÇÃO**")
                        med = str(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                        emo = "🥇" if "Ouro" in med else "🥈" if "Prata" in med else "🥉" if "Bronze" in med else "💎" if "Diamante" in med else "⚪"
                        st.metric("Medalha", f"{emo} {med}")
                        st.markdown(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO MEDALHA LC', 0))}**")
                
                with c3:
                    with st.container(border=True):
                        st.markdown("📈 **SELL OUT**")
                        st.metric("Atingimento", formatar_pct(info.get('AING SELLOUT %', 0)))
                        st.markdown(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO SELLOUT', 0))}**")

                # Espaçamento para o Total
                st.write("")
                
                # TOTALIZADOR (Fica centralizado e grande)
                total_val = formatar_reais(info.get('TOTAL A RECEBER', '0,00'))
                st.success(f"### 🏆 TOTAL A RECEBER: {total_val}")

                # OBSERVAÇÕES
                obs = info.get('OBSERVAÇÕES GERAIS', '')
                if pd.notna(obs) and str(obs).strip() not in ['', '0', 'nan', 'NAN']:
                    with st.expander("📝 Notas e Observações", expanded=True):
                        st.write(str(obs))
            else:
                st.error("Matrícula não encontrada. Verifique os números e tente novamente.")
    else:
        # Mensagem inicial para mobile
        st.info("👈 Abra o menu lateral (setinha no topo) e digite sua matrícula para começar.")
else:
    st.error("Erro ao carregar os dados. Verifique se o arquivo dados.csv está no GitHub.")
