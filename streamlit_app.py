# ... (parte inicial do código de carregamento do df igual)

if df is not None:
    col_mat = 'MATRÍCULA' if 'MATRÍCULA' in df.columns else df.columns[0]
    df[col_mat] = df[col_mat].astype(str).str.strip()
    
    with st.sidebar:
        st.header("🔑 Acesso")
        acesso = st.text_input("Digite sua MATRÍCULA:", placeholder="Ex: 1-46532")
    
    if acesso:
        acesso = acesso.strip()
        # Se for ADMIN, mostra tudo
        if acesso.upper() == "ADMIN":
            st.subheader("📊 Visão Geral - Admin")
            st.dataframe(df, use_container_width=True)
        # SE NÃO FOR ADMIN, busca a promotora
        else:
            dados = df[df[col_mat] == acesso]
            
            if not dados.empty:
                col_n = [c for c in df.columns if 'NOME' in c][0]
                st.header(f"Olá, {dados.iloc[0][col_n]}! 👋")
                
                # Tratamento do Mês
                dados['MÊS'] = dados['MÊS'].astype(str).str.strip().str.upper()
                meses = dados['MÊS'].unique()
                mes_sel = st.selectbox("📅 Selecione o mês:", meses)
                
                info = dados[dados['MÊS'] == mes_sel].iloc[0]
                
                st.markdown("### 📊 Seus Indicadores")
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    with st.container(border=True):
                        st.write("🎯 **ADERÊNCIA**")
                        st.metric("Performance", formatar_pct(info.get('PRODUTIVIDADE ADERENCIA ROTEIRO', 0)))
                        st.write(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO ADERENCIA ROTEIRO', 0))}**")
                
                with c2:
                    with st.container(border=True):
                        st.write("🏪 **LOJA DO CORAÇÃO**")
                        med = str(info.get('MEDALHA LOJA DO CORAÇÃO', '-'))
                        emo = "🥇" if "Ouro" in med else "🥈" if "Prata" in med else "🥉" if "Bronze" in med else "💎" if "Diamante" in med else "⚪"
                        st.metric("Medalha", f"{emo} {med}")
                        st.write(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO MEDALHA LC', 0))}**")
                
                with c3:
                    with st.container(border=True):
                        st.write("📈 **SELL OUT**")
                        st.metric("Atingimento", formatar_pct(info.get('AING SELLOUT %', 0)))
                        st.write(f"Prêmio: **{formatar_reais(info.get('PREMIAÇÃO SELLOUT', 0))}**")

                st.divider()
                total_final = formatar_reais(info.get('TOTAL A RECEBER', '0,00'))
                st.success(f"### 🏆 VALOR TOTAL A RECEBER: {total_final}")
            else:
                st.error("Matrícula não encontrada.")
