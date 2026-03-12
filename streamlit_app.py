import streamlit as st
import pandas as pd

# 1. Configuração da Página
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

df = carregar()

if df is not None:
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    acesso = st.text_input("👤 Digite sua MATRÍCULA:", placeholder="Ex: 1-37507")

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
                
                st.write(f"Resultados de **{mes_sel}**")
                
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    with st.container(border=True):
                        st.subheader("🎯 ADERÊNCIA")
                        val_ad = str(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', '0')).replace('%', '')
                        st.metric("Performance", f"{val_ad}%")
                        # Colocando o R$ e emoji de dinheiro
                        st.write(f"💰 **Prêmio: R$ {info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0)}**")
                
                with c2:
                    with st.container(border=True):
                        st.subheader("🏅 LOJA DO CORAÇÃO")
                        medalha = str(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                        
                        # Lógica para escolher o emoji da medalha
                        emoji_m = "🎖️"
                        if "Ouro" in medalha: emoji_m = "🥇"
                        elif "Prata" in medalha: emoji_m = "🥈"
                        elif "Bronze" in medalha: emoji_m = "🥉"
                        elif "Diamante" in medalha: emoji_m = "💎"
                        
                        st.metric("Medalha", f"{emoji_m} {medalha}")
                        st.write(f"💰 **Prêmio: R$ {info.get('PREMIAÇÃO MEDALHA LC', 0)}**")
                
                with c3:
                    with st.container(border=True):
                        st.subheader("📈 SELL OUT")
                        val_so = str(info.get('AING SELLOUT %', '0')).replace('%', '')
                        st.metric("Atingimento", f"{val_so}%")
                        st.write(f"💰 **Prêmio: R$ {info.get('PREMIAÇÃO SELLOUT', 0)}**")

                st.divider()
                
                total = info.get('TOTAL A RECEBER', 0)
                st.success(f"### 🏆 VALOR TOTAL A RECEBER: R$ {total}")
                
                obs = info.get('OBSERVAÇÕES GERAIS', '')
                if pd.notna(obs) and obs != '' and obs != '0':
                    st.info(f"💡 **Nota:** {obs}")
            else:
                st.error("Matrícula não encontrada.")
