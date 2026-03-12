import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. Título simples (sem design pesado para não dar erro)
st.title("☕ Portal de Premiação - 3 Corações")

# 2. Tentativa de Conexão
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    st.success("Conectado à planilha com sucesso!")
    
    # 3. Login por Matrícula
    acesso = st.text_input("Digite sua MATRÍCULA:")

    if acesso:
        if acesso.lower() == "admin":
            st.write("Visão Geral:")
            st.dataframe(df)
        else:
            # Filtra os dados
            dados = df[df['MATRÍCULA'].astype(str) == acesso]
            
            if not dados.empty:
                info = dados.iloc[0]
                st.header(f"Olá, {info['NOME RH']}")
                
                # Exibição simples dos valores
                st.metric("Total a Receber", f"R$ {info['TOTAL A RECEBER']}")
                st.write(f"Vendas: {info['AING SELLOUT %']}%")
                st.write(f"Medalha: {info['MEDALHA LOJA DO CORAÇÃO']}")
            else:
                st.error("Matrícula não encontrada.")

except Exception as e:
    st.error("Erro na conexão. Verifique se o link da planilha está correto nos Secrets.")
    st.exception(e)
