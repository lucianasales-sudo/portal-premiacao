import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal 3 Corações", layout="wide")

st.title("☕ Portal de Premiação")
st.markdown("---")

def carregar():
    try:
        try:
            df = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except:
        return None

# Função para limpar e arredondar porcentagem
def formatar_porcentagem(valor):
    try:
        # Tira o símbolo %, troca vírgula por ponto e vira número
        num = float(str(valor).replace('%', '').replace(',', '.'))
        return f"{int(num)}%" # Transforma em inteiro para sumir as casas decimais
    except:
        return str(valor)

df = carregar()

if df is not None:
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    acesso = st.text_input("👤 Digite sua MATRÍCULA:", placeholder="Ex: 1-46532")

    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN":
            st.subheader("📊 Painel Geral")
            st.dataframe(df)
        else:
            dados = df[df[col_mat] == acesso]
            if not dados.empty:
                col_n = [c for c in df.columns if 'NOME' in c][0]
                st.header(f"Olá, {dados.iloc[0][col_n]}! 👋")
                
                mes_sel = st.selectbox("📅 Selecione o mês:", dados['MÊS'].unique())
                info = dados[dados['MÊS'] == mes_sel].iloc[0]
                
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    with st.container(border=True):
                        st.subheader("🎯 ADERÊNCIA")
                        # Formata para tirar casas decimais
                        perf_formatada = formatar_porcentagem(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0))
                        st.metric("Performance", perf_formatada)
                        st.write(f"💰 **Prêmio: R$ {info.get('PREMIAÇÃO ADERENCIA ROTEIRO', '0,00')}**")
                
                with c2:
                    with st.container(border=True):
                        st.subheader("🏪 LOJA DO CORAÇÃO") # Ícone de loja
                        medalha = str(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                        
                        emoji_m = "🏅"
                        if "Ouro" in medalha: emoji_m = "🥇"
                        elif "Prata" in medalha: emoji_m = "🥈"
                        elif "Bronze" in medalha: emoji_m = "🥉"
                        elif "Diamante" in medalha: emoji_m = "💎"
                        elif "Sem medalha" in medalha: emoji_m = "⚪"
                        
                        st.metric("Medalha", f"{emoji_m} {medalha}")
                        st.write(f"💰
