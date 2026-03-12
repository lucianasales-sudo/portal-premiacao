import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Portal de Premiação 3 Corações", layout="wide")

st.title("☕ Portal de Premiação")
st.write("---")

# 2. Carregamento dos Dados
try:
    # Lendo o arquivo CSV que você subiu
    df = pd.read_csv("dados.csv")
    df['MATRÍCULA'] = df['MATRÍCULA'].astype(str)
    
    # 3. Interface de Acesso
    acesso = st.text_input("Digite sua MATRÍCULA para acessar:", placeholder="Ex: 12345")

    if acesso:
        # Lógica de ADMIN
        if acesso.upper() == "ADMIN":
            st.subheader("📊 Painel Geral de Performance")
            st.dataframe(df)
        
        # Lógica de PROMOTORA
        else:
            resultado = df[df['MATRÍCULA'] == acesso]
            
            if not resultado.empty:
                info = resultado.iloc[0]
                st.header(f"Olá, {info['NOME RH']}! 👋")
                st.write(f"Competência: {info['MÊS']} / {info['ANO']}")

                # Usando colunas e métricas nativas (mais seguras contra erros)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("**ADERÊNCIA**")
                    st.metric("Performance", f"{info['PRODUTIVIDADE ADERENCIA ROTEIRO']}%")
                    st.write(f"Prêmio: R$ {info['PREMIAÇÃO ADERENCIA ROTEIRO']}")
                
                with col2:
                    st.success("**LOJA DO CORAÇÃO**")
                    st.metric("Medalha", str(info['MEDALHA LOJA DO CORAÇÃO']))
                    st.write(f"Prêmio: R$ {info['PREMIAÇÃO MEDALHA LC']}")
                
                with col3:
                    st.warning("**SELL OUT**")
                    st.metric("Atingimento", f"{info['AING SELLOUT %']}%")
                    st.write(f"Prêmio: R$ {info['PREMIAÇÃO SELLOUT']}")

                st.write("---")
                # Destaque do valor total
                st.subheader(f"💰 TOTAL A RECEBER: R$ {info['TOTAL A RECEBER']}")
                
                if str(info['OBSERVAÇÕES GERAIS']) != 'nan':
                    st.markdown(f"*Obs: {info['OBSERVAÇÕES GERAIS']}*")
            else:
                st.error("Matrícula não localizada no arquivo dados.csv")

except Exception as e:
    st.error("Erro técnico ao ler a base de dados.")
    st.info("Certifique-se de que o arquivo 'dados.csv' está na mesma pasta do código no GitHub.")
