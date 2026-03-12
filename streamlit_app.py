import streamlit as st
import pandas as pd

# 1. Configuração da Página e Estilo Visual
st.set_page_config(page_title="Portal de Premiação 3 Corações", layout="wide")

# Usando um bloco de estilo mais simples para evitar erros de colagem
st.markdown("""
    <style>
    .pilar-header {
        background-color: #556B2F;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .pilar-card {
        background-color: white;
        padding: 20px;
        text-align: center;
        border-radius: 0 0 8px 8px;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .total-box {
        background-color: #FFD700;
        color: #333;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_input_html=True)

st.title("🏆 Portal de Premiação")
st.write("Bem-vinda ao sistema de acompanhamento de resultados.")

# 2. Carregamento dos Dados
try:
    df = pd.read_csv("dados.csv")
    df['MATRÍCULA'] = df['MATRÍCULA'].astype(str)
    
    # 3. Interface de Acesso
    acesso = st.text_input("Digite sua MATRÍCULA para ver seus resultados:", placeholder="Ex: 12345")

    if acesso:
        # Lógica de ADMIN
        if acesso.upper() == "ADMIN":
            st.subheader("📊 Painel Geral de Performance (Visão Gerencial)")
            st.dataframe(df) # Mostra a planilha inteira
            
            # Pequeno resumo para o Admin
            st.divider()
            col_adm1, col_adm2 = st.columns(2)
            col_adm1.metric("Total de Promotoras", len(df))
            col_adm2.metric("Média de Sell-out", f"{df['AING SELLOUT %'].mean():.1f}%")

        # Lógica de PROMOTORA
        else:
            resultado = df[df['MATRÍCULA'] == acesso]
            
            if not resultado.empty:
                info = resultado.iloc[0]
                st.header(f"Olá, {info['NOME RH']}! 👋")
                st.info(f"Resultados de **{info['MÊS']} / {info['ANO']}** - Regional: {info['REGIONAL']}")

                # Pilares de Premiação (Baseado na sua imagem)
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    st.markdown('<div class="pilar-header">ADÊRENCIA AO ROTEIRO</div>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="pilar-card"><h2>{info["PRODUTIVIDADE ADERENCIA ROTEIRO"]}%</h2><p>Prêmio: R$ {info["PREMIAÇÃO ADERENCIA ROTEIRO"]}</p></div>', unsafe_allow_input_html=True)
                
                with c2:
                    st.markdown('<div class="pilar-header">LOJA DO CORAÇÃO</div>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="pilar-card"><h2>{info["MEDALHA LOJA DO CORAÇÃO"]}</h2><p>Prêmio: R$ {info["PREMIAÇÃO MEDALHA LC"]}</p></div>', unsafe_allow_input_html=True)
                
                with c3:
                    st.markdown('<div class="pilar-header">SELL OUT (VENDAS)</div>', unsafe_allow_input_html=True)
                    st.markdown(f'<div class="pilar-card"><h2>{info["AING SELLOUT %"]}%</h2><p>Prêmio: R$ {info["PREMIAÇÃO SELLOUT"]}</p></div>', unsafe_allow_input_html=True)

                # Totalizador
                st.markdown(f'<div class="total-box">VALOR TOTAL A RECEBER: R$ {info["TOTAL A RECEBER"]}</div>', unsafe_allow_input_html=True)
                
                if str(info['OBSERVAÇÕES GERAIS']) != 'nan':
                    st.warning(f"**Observação:** {info['OBSERVAÇÕES GERAIS']}")
            else:
                st.error("Matrícula não localizada. Verifique o número ou contate a supervisão.")

except Exception as e:
    st.error("Erro ao carregar base de dados.")
