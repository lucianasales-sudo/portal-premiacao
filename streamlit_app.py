@st.cache_data
def load():
    try:
        # 1. Carrega dados.csv
        try: d1 = pd.read_csv("dados.csv", encoding='utf-8')
        except: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        d1.columns = [c.strip().upper() for c in d1.columns]
        
        # 2. Carrega BASE ABERTURA LC.csv
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", encoding='utf-8')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        d2.columns = [c.strip().upper() for c in d2.columns]

        # 3. Localiza a coluna de Matrícula dinamicamente em cada arquivo
        # Procura por 'MATRÍCULA', 'MATRICULA' ou usa a primeira coluna como reserva
        col_m1 = [c for c in d1.columns if 'MATRIC' in c]
        k1 = col_m1[0] if col_m1 else d1.columns[0]
        
        col_m2 = [c for c in d2.columns if 'MATRIC' in c]
        k2 = col_m2[0] if col_m2 else d2.columns[0]

        # 4. Padroniza para 'MATRÍCULA' para o código não quebrar depois
        d1 = d1.rename(columns={k1: 'MATRÍCULA'})
        d2 = d2.rename(columns={k2: 'MATRÍCULA'})

        # 5. Limpa os dados das matrículas (remove espaços e vira texto)
        d1['MATRÍCULA'] = d1['MATRÍCULA'].astype(str).str.strip()
        d2['MATRÍCULA'] = d2['MATRÍCULA'].astype(str).str.strip()

        # 6. Renomeia as demais colunas para siglas curtas (Anti-Quebra)
        d1 = d1.rename(columns={
            'PRODUTIVIDADE ADERENCIA ROTEIRO': 'A1',
            'PREMIAÇÃO ADERENCIA ROTEIRO': 'A2',
            'MEDALHA LOJA DO CORAÇÃO': 'L1',
            'PREMIAÇÃO MEDALHA LC': 'L2',
            'META SELLOUT': 'S1',
            'REAL SELLOUT': 'S2',
            'AING SELLOUT %': 'S3',
            'PREMIAÇÃO SELLOUT': 'S4',
            'TOTAL A RECEBER': 'TOT'
        })
        
        # 7. Merge final
        return pd.merge(d1, d2, on='MATRÍCULA', how='left')
    except Exception as e:
        st.error(f"Erro detalhado: {e}")
        return None
