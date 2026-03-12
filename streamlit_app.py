import streamlit as st
import pandas as pd

st.title("☕ Portal de Premiação")

try:
    # Tenta ler o arquivo que você subiu
    df = pd.read_csv("dados.csv")
    
    matricula = st.text_input("Digite sua MATRÍCULA:")

    if matricula:
        # Filtra os dados
        df['MATRÍCULA'] = df['MATRÍCULA'].astype(str)
        resultado = df[df['MATRÍCULA'] == str(matricula)]
        
        if not resultado.empty:
            linha = resultado.iloc[0]
            st.success(f"Olá, {linha['NOME RH']}!")
            
            # Mostra os dados básicos
            st.write(f"Mês: {linha['MÊS']}")
            st.metric("Total a Receber", f"R$ {linha['TOTAL A RECEBER']}")
            st.write(f"Vendas (Sell-out): {linha['AING SELLOUT %']}%")
        else:
            st.error("Matrícula não encontrada no arquivo dados.csv")

except Exception as e:
    st.error("Erro: Verifique se você subiu o arquivo 'dados.csv' no GitHub.")
    st.write(e)
