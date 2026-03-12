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

# Função para garantir o R$ e limpar duplicatas
def formatar_reais(valor):
    if pd.isna(valor) or str(valor).strip() == '-':
        return "R$ 0,00"
    # Remove R, $, espaços e garante que o símbolo seja R$
    limpo = str(valor).replace('R', '').replace('$', '').strip()
    return f"R$ {limpo}"

def formatar_pct(valor):
    try:
        num = float(str(valor).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
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
                        st.metric("Performance", formatar_pct(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                        st.write(f"💰 **Prêmio: {formatar_reais(info.get('PREMIAÇÃO ADERENCIA ROTEIRO', '0,00'))}**")
                
                with c2:
                    with st.container(border=True):
                        st.subheader("🏪 LOJA DO CORAÇÃO")
                        med = str(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                        emo = "🥇" if "Ouro" in med else "🥈" if "Prata" in med else "🥉" if "Bronze" in med else "💎" if "Diamante" in med else "⚪"
                        st.metric("Medalha", f"{emo} {med}")
                        st.write(f"💰 **Prêmio: {formatar_reais(info.get('PREMIAÇÃO MEDALHA LC', '0,00'))}**")
                
                with c3:
                    with st.container(border=True):
                        st.subheader("📈 SELL OUT")
                        st.metric("Atingimento", formatar_pct(info.get('AING SELLOUT %', 0)))
                        st.write(f"💰 **Prêmio: {formatar_reais(info.get('PREMIAÇÃO SELLOUT', '0,00'))}**")

                st.divider()
                
                # Valor Total com Cifrão Garantido
                total_final = formatar_reais(info.get('TOTAL A RECEBER', '0,00'))
                st.success(f"### 🏆 VALOR TOTAL A RECEBER: {total_final}")
            else:
                st.error("Matrícula não encontrada.")
