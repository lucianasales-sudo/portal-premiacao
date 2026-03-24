@st.cache_data
def load():
    try:
        # Tenta ler d1 (dados.csv)
        try: d1 = pd.read_csv("dados.csv", sep=',', encoding='utf-8')
        except: d1 = pd.read_csv("dados.csv", sep=';', encoding='latin-1')
        
        # Tenta ler d2 (BASE ABERTURA LC.csv)
        try: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=',', encoding='utf-8')
        except: d2 = pd.read_csv("BASE ABERTURA LC.csv", sep=';', encoding='latin-1')
        
        # Limpeza de colunas
        d1.columns = [c.strip().upper() for c in d1.columns]
        d2.columns = [c.strip().upper() for c in d2.columns]

        # Renomeia para siglas
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
        
        k = 'MATRÍCULA'
        d1[k] = d1[k].astype(str).str.strip()
        d2[k] = d2[k].astype(str).str.strip()
        
        return pd.merge(d1, d2, on=k, how='left')
    except Exception as e:
        st.error(f"Erro nos arquivos: {e}")
        return None
