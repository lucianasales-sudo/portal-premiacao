import streamlit as st
import pandas as pd

# 1. Configurações da Página
st.set_page_config(page_title="Portal de Premiação 3 Corações", layout="wide")

# 2. DESIGN CUSTOMIZADO (Bloco único e estável)
st.markdown("""
<style>
    /* Fundo do App */
    .stApp { background-color: #f8f9fa; }
    
    /* Estilo dos Cards */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #556B2F;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-title { color: #556B2F; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .metric-value { color: #333; font-size: 32px; font-weight: bold; margin: 10px 0; }
    .metric-prize { color: #28a745; font-size: 16px; font-weight: bold; }

    /* Banner do Total */
    .total-banner {
        background: linear-gradient(90deg, #FFD700 0%, #ffcc00 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 30px;
        border: 2px solid #e6b800;
    }
</style>
""", unsafe_allow_input_html=True)

# 3. CABEÇALHO
st.title("☕ Portal de Premiação")
st.subheader("Performance e Metas")
st.markdown("---")

def carregar_dados():
    try:
        try:
            df = pd.read_csv("dados.csv", encoding='utf-8')
        except:
            df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except:
        return None

df = carregar_dados()

if df is not None:
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    # Campo de login centralizado
    col_login, _ = st.columns([2, 3])
    with col_login:
        acesso = st.text_input("👤 Digite sua MATRÍCULA:", placeholder="Ex: 1-37507")

    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN":
            st.dataframe(df)
        else:
            dados_pessoais = df[df[col_mat] == acesso]
            
            if not dados_pessoais.empty:
                col_nome = [c for c in df.columns if 'NOME' in c][0]
                st.markdown(f"### Olá, **{dados_pessoais.iloc[0][col_nome]}**! 👋")
                
                # Seleção de Mês
                meses = dados_pessoais['MÊS'].unique()
                mes_sel = st.selectbox("📅 Selecione o mês de referência:", meses)
                
                info = dados_pessoais[dados_pessoais['MÊS'] == mes_sel].iloc[0]
                st.markdown("<br>", unsafe_allow_input_html=True)

                # 4. EXIBIÇÃO DOS CARDS
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    val_ad = str(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', '0')).replace('%', '')
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-title">Aderência</div>
                        <div class="metric-value">{val_ad}%</div>
                        <div class="metric-prize">Prêmio: R$ {info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0)}</div>
                    </div>""", unsafe_allow_input_html=True)
                
                with c2:
                    st.markdown(f"""<div class="metric-card" style="border-left-color: #cc0000;">
                        <div class="metric-title">Loja do Coração</div>
                        <div class="metric-value">{info.get('MEDALHA LOJA DO CORAÇÃO', '-')}</div>
                        <div class="metric-prize">Prêmio: R$ {info.get('PREMIAÇÃO MEDALHA LC', 0)}</div>
                    </div>""", unsafe_allow_input_html=True)
                
                with c3:
                    val_so = str(info.get('AING SELLOUT %', '0')).replace('%', '')
                    st.markdown(f"""<div class="metric-card" style="border-left-color: #ff8c00;">
                        <div class="metric-title">Sell Out</div>
                        <div class="metric-value">{val_so}%</div>
                        <div class="metric-prize">Prêmio: R$ {info.get('PREMIAÇÃO SELLOUT', 0)}</div>
                    </div>""", unsafe_allow_input_html=True)

                # 5. BANNER FINAL
                total = info.get('TOTAL A RECEBER', 0)
                st.markdown(f"""
                <div class="total-banner">
                    <span style="font-size: 18px; color: #555;">VALOR TOTAL A RECEBER</span><br>
                    <span style="font-size: 40px; color: #333; font-weight: bold;">R$ {total}</span>
                </div>
                """, unsafe_allow_input_html=True)
                
                obs = info.get('OBSERVAÇÕES GERAIS', '')
                if pd.notna(obs) and obs != '' and obs != '0':
                    st.info(f"💡 **Nota do Supervisor:** {obs}")
            else:
                st.error("Matrícula não encontrada.")
