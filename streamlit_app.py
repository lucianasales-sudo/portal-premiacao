import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal de Premiação 3 Corações", layout="wide")

# Título com ícone de café
st.title("☕ Portal de Premiação")
st.markdown("---")

try:
    df = pd.read_csv("dados.csv")
    df['MATRÍCULA'] = df['MATRÍCULA'].astype(str)
    
    # 1. ACESSO INICIAL
    acesso = st.text_input("Digite sua MATRÍCULA para acessar:", placeholder="Ex: 12345")

    if acesso:
        if acesso.upper() == "ADMIN":
            st.subheader("📊 Painel Geral (Visão Admin)")
            st.dataframe(df)
        else:
            # Filtra primeiro pela matrícula
            dados_pessoais = df[df['MATRÍCULA'] == acesso]
            
            if not dados_pessoais.empty:
                nome_promotora = dados_pessoais.iloc[0]['NOME RH']
                st.header(f"Olá, {nome_promotora}! 👋")
                
                # 2. FILTRO DE MÊS
                # Pega todos os meses disponíveis na planilha para essa pessoa
                meses_disponiveis = dados_pessoais['MÊS'].unique()
                mes_selecionado = st.selectbox("Selecione o Mês de Competência:", meses_disponiveis)
                
                # Filtra os dados finais pelo mês escolhido
                info = dados_pessoais[dados_pessoais['MÊS'] == mes_selecionado].iloc[0]
                
                st.write(f"Exibindo resultados de: **{mes_selecionado} / {info['ANO']}**")
                st.markdown("<br>", unsafe_allow_input_html=True)

                # 3. CARDS DE PERFORMANCE (Versão Clean)
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    st.info("### ADERÊNCIA")
                    # Usei .replace para garantir que não venha % duplicado se já estiver no CSV
                    valor_ad = str(info['PRODUTIVIDADE ADERENCIA ROTEIRO']).replace('%', '')
                    st.metric("Performance", f"{valor_ad}%")
                    st.write(f"**Prêmio: R$ {info['PREMIAÇÃO ADERENCIA ROTEIRO']}**")
                
                with c2:
                    st.success("### LOJA DO CORAÇÃO")
                    st.metric("Medalha", str(info['MEDALHA LOJA DO CORAÇÃO']))
                    st.write(f"**Prêmio: R$ {info['PREMIAÇÃO MEDALHA LC']}**")
                
                with c3:
                    st.warning("### SELL OUT")
                    valor_so = str(info['AING SELLOUT %']).replace('%', '')
                    st.metric("Atingimento", f"{valor_so}%")
                    st.write(f"**Prêmio: R$ {info['PREMIAÇÃO SELLOUT']}**")

                st.markdown("<br>", unsafe_allow_input_html=True)
                
                # 4. DESTAQUE TOTAL
                st.markdown(f"""
                <div style="background-color: #FFD700; padding: 25px; border-radius: 15px; text-align: center;">
                    <h2 style="color: #333; margin: 0;">💰 TOTAL A RECEBER: R$ {info['TOTAL A RECEBER']}</h2>
                </div>
                """, unsafe_allow_input_html=True)
                
                if str(info['OBSERVAÇÕES GERAIS']) != 'nan':
                    st.info(f"**Nota:** {info['OBSERVAÇÕES GERAIS']}")
            else:
                st.error("Matrícula não localizada.")

except Exception as e:
    st.error("Erro ao carregar dados. Verifique o arquivo dados.csv")
