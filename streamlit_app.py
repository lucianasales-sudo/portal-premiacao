import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal de Premiação 3 Corações", layout="wide")

st.title("☕ Portal de Premiação")
st.markdown("---")

try:
    # Carregando os dados
    df = pd.read_csv("dados.csv")
    
    # Limpando nomes de colunas (tira espaços extras que podem causar erro)
    df.columns = [c.strip() for c in df.columns]
    df['MATRÍCULA'] = df['MATRÍCULA'].astype(str).str.strip()
    
    acesso = st.text_input("Digite sua MATRÍCULA:", placeholder="Ex: 1-37507")

    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN":
            st.dataframe(df)
        else:
            dados_pessoais = df[df['MATRÍCULA'] == acesso]
            
            if not dados_pessoais.empty:
                # Pega o nome de qualquer coluna que comece com "NOME"
                col_nome = [c for c in df.columns if 'NOME' in c.upper()][0]
                st.header(f"Olá, {dados_pessoais.iloc[0][col_nome]}! 👋")
                
                # Filtro de Mês
                meses = dados_pessoais['MÊS'].unique()
                mes_sel = st.selectbox("Selecione o Mês:", meses)
                
                info = dados_pessoais[dados_pessoais['MÊS'] == mes_sel].iloc[0]

                # Exibição segura (Métricas)
                st.write(f"Exibindo resultados de: **{mes_sel}**")
                
                c1, c2, c3 = st.columns(3)
                
                # Função interna para evitar erro de coluna inexistente
                def mostrar_metrica(coluna, titulo, local):
                    try:
                        valor = str(info[coluna]).replace('%', '')
                        local.metric(titulo, f"{valor}%")
                    except:
                        local.warning(f"Coluna {titulo} não encontrada")

                with c1:
                    st.info("### ADERÊNCIA")
                    mostrar_metrica('PRODUTIVIDADE ADERENCIA ROTEIRO', 'Performance', st)
                    st.write(f"Prêmio: R$ {info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0)}")
                
                with c2:
                    st.success("### LOJA DO CORAÇÃO")
                    st.metric("Medalha", str(info.get('MEDALHA LOJA DO CORAÇÃO', '-')))
                    st.write(f"Prêmio: R$ {info.get('PREMIAÇÃO MEDALHA LC', 0)}")
                
                with c3:
                    st.warning("### SELL OUT")
                    mostrar_metrica('AING SELLOUT %', 'Atingimento', st)
                    st
