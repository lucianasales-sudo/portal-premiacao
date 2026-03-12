import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Portal 3 Corações", layout="wide", page_icon="☕")

# 2. Injeção de CSS em Linha Única (Evita o TypeError do Python 3.14)
st.markdown('<style>.stApp{background-color:#F4F7F6}div[data-testid="stMetric"]{background-color:white;padding:15px;border-radius:10px;box-shadow:0 4px 6px rgba(0,0,0,0.1);border-bottom:4px solid #556B2F}.stTextInput>div>div>input{border-radius:8px;border:1px solid #556B2F}</style>', unsafe_allow_input_html=True)

# 3. Cabeçalho
st.title("🏆 Portal de Premiação")
st.write("Acompanhe seus resultados mensais.")
st.divider()

def carregar():
    try:
        try: df = pd.read_csv("dados.csv", encoding='utf-8')
        except: df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except: return None

def formatar_reais(valor):
    if pd.isna(valor) or str(valor).strip() in ['-', '', '0']: return "R$ 0,00"
    limpo = str(valor).replace('R', '').replace('$', '').strip()
    return f"R$ {limpo}"

def formatar_pct(valor):
    try:
        num = float(str(valor).replace('%', '').replace(',', '.'))
        return f"{int(num)}%"
    except: return str(valor)

df = carregar()

if df is not None:
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    # Login na Lateral para deixar o centro limpo
    with st.sidebar:
        st.header("🔑 Acesso")
        acesso = st.text_input("Sua Matrícula:", placeholder="Ex: 1-46532")
    
    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN":
            st.dataframe(df, use_container_width=True)
        else:
            dados = df[df[col_mat] == acesso]
            if not dados.empty:
                col_n = [c for c in df.columns if 'NOME' in c][0]
                st.header(f"Olá, {dados.iloc[0][col_n]}! 👋")
                
                mes_sel = st.selectbox("📅 Mês de referência:", dados['MÊS'].unique())
                info = dados[dados['MÊS'] == mes_sel].iloc[0]
                
                # --- CARDS DE INDICADORES ---
                st.markdown("### 📊 Indicadores de Performance")
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    st.metric("🎯 ADERÊNCIA", formatar_pct(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                    st.write(f"💰 Prêmio: **{formatar_reais(info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
                
                with c2:
                    med = str(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                    emo = "🥇" if "Ouro" in med else "🥈" if "Prata" in med else "🥉" if "Bronze" in med else "💎" if "Diamante" in med else "⚪"
                    st.metric("🏪 LOJA DO CORAÇÃO", f"{emo} {med}")
                    st.write(f"💰 Prêmio: **{formatar_reais(info.get('PREMIAÇÃO MEDALHA LC', 0))}**")
                
                with c3:
                    st.metric("📈 SELL OUT", formatar_pct(info.get('AING SELLOUT %', 0)))
                    st.write(f"💰 Prêmio: **{formatar_reais(info.get('PREMIAÇÃO SELLOUT', 0))}**")

                st.divider()
                
                # Destaque do Total
                total_final = formatar_reais(info.get('TOTAL A RECEBER', '0,00'))
                st.success(f"## 🏆 VALOR TOTAL A RECEBER: {total_final}")

                # Observações em quadro expansível
                obs = info.get('OBSERVAÇÕES GERAIS', '')
                if pd.notna(obs) and str(obs).strip() not in ['', '0', 'nan', 'NAN']:
                    with st.expander("📝 Notas e Observações", expanded=True):
                        st.write(obs)
            else:
                st.error("Matrícula não encontrada.")
else:
    st.error("Erro ao carregar base de dados.")
