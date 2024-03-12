# importando as bibliotecas necessárias
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def tratamento_pj(df):
    # Preenchendo valores nulos da coluna ÁREADEATUACAO com 'Não informado'
    df['ÁREADEATUACAO'].fillna(value='Não informado', inplace=True)
    #Concatenando colunas ProdutoGPOM e área de atuação
    df['ProdutoGPOM/ÁREADEATUACAO'] = df.apply(lambda row: f"{row['ProdutoGPOM']} / {row['ÁREADEATUACAO']}", axis=1)

    # Preenchendo esses dados nulos com "Desconhecido(a)"
    df['Micro_regiao'].fillna(value='Desconhecido(a)', inplace=True)
    df['Estado'].fillna(value='Desconhecido(a)', inplace=True)
    df['Cidade da conta'].fillna(value='Desconhecido(a)', inplace=True)

    # excluindo essas linhas da base de dados pois são valores importante a analisar e não tem como fazer uma estimativa
    df.dropna(inplace=True)

    # remover linhas duplicadas
    df.drop_duplicates(inplace=True)

    # convertendo a "data de venda" para datetime e removendo a hora da data
    df['Fim Vigência_'] = pd.to_datetime(df['Fim Vigência_'])
    df['DataVenda'] = pd.to_datetime(df['DataVenda'])

    ### adicionando coluna de tempo de contrato
    df['Tempo de Contrato'] = df['Fim Vigência_'] - df['DataVenda']

    # convertendo a coluna 'Tempo de Contrato' para int
    df['Tempo de Contrato'] = df['Tempo de Contrato'].dt.days.astype(int)

    # Defina os limites dos intervalos em dias
    limites = [0, 365, 730, 1095, float('inf')]  # menos de 1 ano, 1 a 2 anos, 2 a 3 anos, mais de 3 anos

    # Crie rótulos para os intervalos
    rotulos = ['Menos de 1 ano', '1 a 2 anos', '2 a 3 anos', 'Mais de 3 anos']

    # Adicione uma nova coluna com a categoria de tempo de contrato
    df['Tempo de Contrato'] = pd.cut(df['Tempo de Contrato'], bins=limites, labels=rotulos, right=False)  

    ### Padronizando os dados para letras maiúsculas
    df = df.apply(lambda x: x.str.upper() if x.dtype == 'object' else x)

    # resetando o index
    df.reset_index(drop=True, inplace=True)

    mapeamento_nomes = {
    'IdentificadorCliente': 'ID Cliente',
    'LINHA_ACAO': 'Linha de Ação',
    'ProdutoGPOM': 'Produto GPOM',
    'DataVenda': 'Data de Venda',
    'Classe de Serviço': 'Classe de Serviço',
    'Cidade da conta': 'Cidade',
    'Micro_regiao': 'Microrregião',
    'Porte': 'Porte',
    'Estado': 'Estado',
    'Fim Vigência_': 'Fim de Vigência',
    'Tipo_Pessoa': 'Tipo Pessoa',
    'Setor IBGE': 'Setor IBGE',
    'ÁREADEATUACAO': 'Área de Atuação',
    'Tempo de Contrato': 'Tempo de Contrato',
    'longitude': 'Longitude',
    'latitude': 'Latitude',
    'Código CNAE': 'Código CNAE',
    'Descrição CNAE': 'Descrição CNAE',
    'Divisão CNAE': 'Divisão CNAE',
    'ProdutoGPOM/ÁREADEATUACAO': 'Produto GPOM e Área de Atuação'
    }

    df_final = df.rename(columns=mapeamento_nomes)

    def processar_valor(valor):
        if 'NÃO INFORMADO' in valor:
            return valor.replace(' / NÃO INFORMADO', '')  # Remove apenas a parte 'NÃO INFORMADO'
        else:
            return f'{valor}'

    # Aplica a função à coluna 'Área de Atuação e Produto GPOM'
    df_final['Produto GPOM e Área de Atuação'] = df_final['Produto GPOM e Área de Atuação'].apply(processar_valor)

    return df_final

def tratamento_pf(df):
    # preenchendo valores nulos da coluna "ÁREADEATUACAO" com "não informado"
    df['ÁREADEATUACAO'].fillna('Não informado', inplace = True)

    #Concatenando colunas ProdutoGPOM e área de atuação
    df['ProdutoGPOM/ÁREADEATUACAO'] = df.apply(lambda row: f"{row['ProdutoGPOM']} / {row['ÁREADEATUACAO']}", axis=1)

    # excluindo essas linhas da base de dados pois são valores importante a analisar e não tem como fazer uma estimativa
    df = df.dropna(subset=['Data de Nascimento (Cliente) (Conta)','Gênero (Cliente) (Conta)'])

    # preenchendo esses dados nulos com "Desconhecido(a)"
    df['Micro_regiao'].fillna('Desconhecido(a)', inplace=True)
    df['Estado'].fillna('Desconhecido(a)', inplace=True)

    # resetando o index
    df.reset_index(drop=True,inplace=True)

    # convertendo a data de venda para datetime
    df['DataVenda'] = pd.to_datetime(df['DataVenda'])

    # convertendo a data de nascimento para datetime
    df['Data de Nascimento (Cliente) (Conta)'] = pd.to_datetime(df['Data de Nascimento (Cliente) (Conta)'], errors='coerce')

    # convertendo a data de fim de vigência para datetime
    df['Fim Vigência_'] = pd.to_datetime(df['Fim Vigência_'],errors='coerce')

    # excluindo o dado nulo atribuido ao fazer a conversão pra datetime
    df = df.dropna(subset=['Data de Nascimento (Cliente) (Conta)'])

    # resetando index
    df.reset_index(drop=True,inplace=True)

    # Criando uma coluna com a idade dos clientes
    df['Idade'] = ((df['DataVenda'] - df['Data de Nascimento (Cliente) (Conta)']).dt.days / 365.25).round(2)

    # convertendo coluna idade para tipo inteiro
    df['Idade'] = df['Idade'].astype(int)

    # removendo horário da venda
    df['DataVenda'] = pd.to_datetime(df['DataVenda']).dt.date
    df['DataVenda'] = pd.to_datetime(df['DataVenda'])

    # adicionando coluna de tempo de contrato
    df['Tempo de Contrato'] = df['Fim Vigência_'] - df['DataVenda']

    #Convertendo a coluna 'Tempo de Contrato' para int
    df['Tempo de Contrato'] = df['Tempo de Contrato'].dt.days.astype(int)

    # padronizando os dados para letras maiúsculas
    df = df.apply(lambda x: x.str.upper() if x.dtype == 'object' else x)

    # excluindo idades acima de 87

    df = df[df['Idade']<=87]

    # excluindo linhas que o gênero é 0
    df = df[df['Gênero (Cliente) (Conta)'] != '0']

    # excluindo coluna extra de micro região
    df = df.drop('Micro_regiao', axis=1)

    # resetando o index
    df.reset_index(drop=True,inplace=True)



    mapeamento_nomes = {
        'IdentificadorCliente': 'ID Cliente',
        'LINHA_ACAO': 'Linha de Ação',
        'ProdutoGPOM': 'Produto GPOM',
        'DataVenda': 'Data de Venda',
        'Classe de Serviço': 'Classe de Serviço',
        'Data de Nascimento (Cliente) (Conta)': 'Data de Nascimento',
        'Gênero (Cliente) (Conta)': 'Gênero',
        'Cidade': 'Cidade',
        'Microrregião (Cliente) (Conta)': 'Microrregião',
        'Porte': 'Porte',
        'Estado': 'Estado',
        'Fim Vigência_': 'Fim de Vigência',
        'Tipo_Pessoa': 'Tipo Pessoa',
        'Setor IBGE': 'Setor IBGE',
        'ÁREADEATUACAO': 'Área de Atuação',
        'ProdutoGPOM/ÁREADEATUACAO': 'Produto GPOM e Área de Atuação',
        'Tempo de Contrato': 'Tempo de Contrato',
        'longitude': 'Longitude',
        'latitude': 'Latitude'
    }

    df_final = df.rename(columns=mapeamento_nomes)

    def processar_valor(valor):
        if 'NÃO INFORMADO' in valor:
            return valor.replace(' / NÃO INFORMADO', '')  # Remove apenas a parte 'NÃO INFORMADO'
        else:
            return f'{valor}'

    # Aplica a função à coluna 'Área de Atuação e Produto GPOM'
    df_final['Produto GPOM e Área de Atuação'] = df_final['Produto GPOM e Área de Atuação'].apply(processar_valor)

    return df_final