import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal de Premiação 3 Corações", layout="wide")

st.title("☕ Portal de Premiação")
st.markdown("---")

def carregar_dados():
    try:
        # Tenta ler com vírgula, se der erro tenta ponto e vírgula
        try:
            df = pd.read_csv("dados.csv", encoding='utf-8')
            if len(df.columns) < 2: # Se ler apenas uma coluna, o separador está errado
                raise Exception
        except:
            df = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        
        # Limpa nomes das colunas
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo dados.csv: {e}")
        return None

df = carregar_dados()

if df is not None:
    # Garante que MATRÍCULA seja texto
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    acesso = st.text_input("Digite sua MATRÍCULA para acessar:", placeholder="Ex: 1-37507")

    if acesso:
        acesso = acesso.strip()
        if acesso.upper() == "ADMIN":
            st.subheader("📊 Visão Geral - Admin")
            st.dataframe(df)
        else:
            dados_pessoais = df[df[col_mat] == acesso]
            
            if not dados_pessoais.empty:
                # Busca nome da promotora
                col_nome = [c for c in df.columns if 'NOME' in c][0]
                st.header(f"Olá, {dados_pessoais.iloc[0][col_nome]}! 👋")
                
                # Filtro de Mês
                meses = dados_pessoais['MÊS'].unique()
                mes_sel = st.selectbox("Selecione o Mês:", meses)
                
                info = dados_pessoais[dados_pessoais['MÊS'] == mes_sel].iloc[0]

                st.write(f"Resultados de: **{mes_sel}**")
                
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    st.info("### ADERÊNCIA")
                    val = str(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', '0')).replace('%', '')
                    st.metric("Performance", f"{val}%")
                    st.write(f"Prêmio: R$ {info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0)}")
                
                with c2:
                    st.success("### LOJA DO CORAÇÃO")
                    st.metric("Medalha", str(info.get('MEDALHA LOJA DO CORAÇÃO', '-')))
                    st.write(f"Prêmio: R$ {info.get('PREMIAÇÃO MEDALHA LC', 0)}")
                
                with c3:
                    st.warning("### SELL OUT")
                    val_so = str(info.get('AING SELLOUT %', '0')).replace('%', '')
                    st.metric("Atingimento", f"{val_so}%")
                    st.write(f"Prêmio: R$ {info.get('PREMIAÇÃO SELLOUT', 0)}")

                st.write("---")
                # Destaque do Total usando comandos simples e seguros
                total_valor = info.get('TOTAL A RECEBER', 0)
                
                st.subheader(f"💰 TOTAL A RECEBER: R$ {total_valor}")
                
                # Se quiser manter o fundo amarelo, usamos este comando em linha única:
                estilo_total = f'<div style="background-color:#FFD700; padding:20px; border-radius:10px; text-align:center;"><h2 style="color:#333; margin:0;">💰 TOTAL A RECEBER: R$ {total_valor}</h2></div>'
                st.markdown(estilo_total, unsafe_allow_input_html=True)
                
                # Observações
                obs = info.get('OBSERVAÇÕES GERAIS', '')
                if pd.notna(obs) and obs != '':
                    st.info(f"**Nota:** {obs}")
            else:
                st.error(f"Matrícula '{acesso}' não encontrada.")
