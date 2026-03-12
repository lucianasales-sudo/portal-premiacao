import streamlit as st
import pandas as pd

# 1. Configurações Iniciais
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# Funções de Formatação (Devem vir antes de serem usadas)
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

# 2. Função de Carregamento
def carregar():
    try:
        try:
            df_local = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df_local = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df_local.columns = [c.strip().upper() for c in df_local.columns]
        return df_local
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# --- AQUI É O PONTO CRÍTICO ---
# Primeiro criamos a variável df
df = carregar()

# Só depois verificamos se ela existe
if df is not None:
    st.title("🏆 Portal de Premiação")
    
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    with st.sidebar:
        st.header("🔑 Acesso")
        acesso = st.text_input("Digite sua MATRÍCULA:", placeholder="Ex: 1-46532")
    
    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN":
            st.dataframe(df)
        else:
            dados = df[df[col_mat] == acesso]
            if not dados.empty:
                col_n = [c for c in df.columns if 'NOME' in c][0]
                st.header(f"Olá, {dados.iloc[0][col_n]}! 👋")
                
                # Tratamento de Mês
                dados['MÊS'] = dados['MÊS'].astype(str).str.strip().str.upper()
                mes_sel = st.selectbox("📅 Selecione o mês:", dados['MÊS'].unique())
                info = dados[dados['MÊS'] == mes_sel].iloc[0]
                
                st.markdown("### 📊 Seus Indicadores")
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    with st.container(border=True):
                        st.write("🎯 **ADERÊNCIA**")
                        st.metric("Performance", formatar_pct(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                        st.write(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
                
                with c2:
                    with st.container(border=True):
                        st.write("🏪 **LOJA DO CORAÇÃO**")
                        med = str(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                        emo = "🥇" if "Ouro" in med else "🥈" if "Prata" in med else "🥉" if "Bronze" in med else "💎" if "Diamante" in med else "⚪"
                        st.metric("Medalha", f"{emo} {med}")
                        st.write(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO MEDALHA LC', 0))}**")
                
                with c3:
                    with st.container(border=True):
                        st.write("📈 **SELL OUT**")
                        st.metric("Atingimento", formatar_pct(info.get('AING SELLOUT %', 0)))
                        st.write(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO SELLOUT', 0))}**")

                st.divider()
                total_final = formatar_reais(info.get('TOTAL A RECEBER', '0,00'))
                st.success(f"### 🏆 VALOR TOTAL A RECEBER: {total_final}")
            else:
                st.error("Matrícula não encontrada.")
else:
    st.warning("Aguardando carregamento do arquivo de dados...")
