"""
Created on Mon Dec 04 10:31:35 2023

@author: Barbara Rosa, Mylena Hortz
"""
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
from streamlit_option_menu import option_menu
from  PIL import Image
import plotly.express as px
pd.set_option('display.float_format', lambda x: '%.3f' % x)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests
from tratamento_dados import tratamento_pj, tratamento_pf
from funcoes import processar_regras_associacao_pf, processar_regras_associacao_pj, find_associated_products
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.graph_objects as go

############################################################################################################
########################################## ESTILO DA PÁGINA ################################################
############################################################################################################

st.set_page_config(page_title="Análise de Potenciais Clientes do Senai",
                   page_icon="Sistema_Fiep_Logo.ico",
                   layout='wide')
mystyle = '''
        <style>
            p {
                text-align: justify;
            }
               .css-1vq4p4l {
                   padding: 1.5rem 1rem 1.5rem;
                }
        </style>
        '''
st.markdown(mystyle, unsafe_allow_html=True)
#st.set_theme('light')
############################################################################################################
############################################## MENU ########################################################
############################################################################################################

logo = Image.open('Senai-Azul.png')
st.sidebar.image(logo, use_column_width=True, clamp=False)

with st.sidebar:
    choose = option_menu("Análise de Potenciais Clientes", ["Sobre o App", "Sobre os Dados", "Regra de Associação", "Contato"],
                         icons=['house', 'search', 'diagram-3','person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "white"},
        "icon": {"color": "black", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#00547c"},
        "nav-link-selected": {"background-color": "#00547c"},
    }
    )
    
data_uploaded = st.sidebar.file_uploader(label="Upload Dataset",type=["xlsx","xls"],key='new_data')
data_path = '../dados/POC_ComercialFIEP_BD.xlsx'

if data_uploaded is not None:
    data = data_uploaded
else:
    data = data_path

@st.cache_data
def load_and_process_data(dataset):
    # Carrega o arquivo Excel
    xl = pd.ExcelFile(dataset)
    
    # Obtém as planilhas
    df_pf_original = pd.read_excel(xl, sheet_name="PF")
    df_pj_original = pd.read_excel(xl, sheet_name="PJ")

    df_pf = tratamento_pf(df_pf_original)
    df_pj = tratamento_pj(df_pj_original)
    
    return df_pf, df_pj

df_pf, df_pj = load_and_process_data(data)
############################################################################################################
######################################## INÍCIO DAS PÁGINAS ################################################
############################################################################################################


############################################################################################################
######################################### PÁGINA 1 - SOBRE #################################################
############################################################################################################
    
## Page 1 - APRESENTAÇÃO

if choose == "Sobre o App":

    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #00547c;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('## <span style="color:#00547c"> Sobre o Aplicativo </span>', unsafe_allow_html=True)

    st.write(
        """Este é um ambiente interativo desenvolvido em formato Streamlit. Este aplicativo foi criado 
        com o objetivo de conduzir uma análise exploratória detalhada da base de dados coletada pela empresa."""
        """ As funcionalidades do dashboard estão organizadas em diferentes páginas, acessíveis através do menu 
        à esquerda. Aqui, você encontrará informações detalhadas sobre os dados coletados."""
    )

    st.write(
        """Destaca-se duas análises exploratórias principais: uma dedicada à categoria 'Pessoa Física' e outra 
        à categoria 'Pessoa Jurídica'. Essas análises fornecem insights valiosos sobre padrões, tendências e 
        métricas relacionadas a cada categoria, contribuindo para uma compreensão mais profunda do conjunto de 
        dados."""
    )

    
    st.markdown('### <span style="color:#327696">Sobre os dados </span>', unsafe_allow_html=True)

    st.write(
    """Nesta seção, apresenta-se uma visualização abrangente das bases de dados subjacentes. Durante a análise 
    inicial dos dados, identificou-se a oportunidade de otimizar a exploração ao abordar separadamente as duas 
    bases disponíveis. Ao examinar detalhadamente os conjuntos de dados, observou-se que as vendas não estavam 
    inicialmente relacionadas de maneira que maximizasse sua utilidade conjunta."""
    )

    st.write(
        """Diante desse insight, optou-se por realizar um processo abrangente de tratamento e limpeza em ambas 
        as bases de dados, personalizando cada etapa conforme as necessidades específicas de cada uma. Essa 
        abordagem personalizada visava não apenas garantir a consistência e integridade dos dados, mas também 
        potencializar as análises subsequentes ao ajustar as informações de acordo com a natureza única de cada 
        conjunto."""
    )

    
    st.markdown('### <span style="color:#327696"> Regra de Associação </span>', unsafe_allow_html=True)

    st.write(
)

    st.write(
    )
        
    st.markdown('#### <span style="color:#327696"> Algoritmo Apriori </span>', unsafe_allow_html=True)
    st.write(
)


############################################################################################################
######################################### PÁGINA 2 - Sobre os Dados ########################################
############################################################################################################

# Adicione um botão na seção "Sobre o App" para escolher entre as bases de dados
if choose == "Sobre os Dados":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #00547c;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('## <span style="color:#00547c"> Sobre os dados </span>', unsafe_allow_html=True)   
    
    st.write("""As bases de dados foram segmentadas entre informações de Pessoa Física e Pessoa Jurídica. 
             A análise foi conduzida de maneira distinta, alinhada aos interesses específicos de cada tipo de cliente, visando aprimorar a abordagem na análise exploratória.
             """)
    # Botão para escolher a base de dados
    selected_base = st.radio("Selecione a Base de Dados que deseja visualizar", ["Pessoa Física", "Pessoa Jurídica"])

    if selected_base == "Pessoa Física":
        qtd_linhas = df_pf.shape[0]
        qtd_colunas = df_pf.shape[1]

        col1, col2 = st.columns(2)
        col1.metric(f'Número de linhas', f'{qtd_linhas}')
        col2.metric(f'Número de colunas', f'{qtd_colunas}')
        with st.expander("Visualização completa dos dados"):
            st.write(df_pf)
    else:
        qtd_linhas = df_pj.shape[0]
        qtd_colunas = df_pj.shape[1]

        col1, col2 = st.columns(2)
        col1.metric(f'Número de linhas', f'{qtd_linhas}')
        col2.metric(f'Número de colunas', f'{qtd_colunas}')
        with st.expander("Visualização completa dos dados"):
            st.write(df_pj)

############################################################################################################
################################### PÁGINA 3 - Regra de Associação #########################################
############################################################################################################
# Page 3 - Regra de Associação

elif choose == "Regra de Associação":
    st.markdown('## <span style="color:#00547c"> Regra de Associação </span>', unsafe_allow_html=True) 
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #00547c;} 
    </style> """, unsafe_allow_html=True) 
 
    aba1, aba2 = st.tabs(['Pessoa Jurídica', 'Pessoa Física'])
    with aba1:
        df = df_pj

        st.markdown('### <span style="color:#00547c"> Filtrando por Perfil de Cliente: </span>', unsafe_allow_html=True) 
        ###################################### Filtros ###################################### 
        col1, col2 = st.columns(2)
        with col1:
            ibge_options = df_pj['Setor IBGE'].value_counts().index.tolist()
            selected_setor_ibge = st.selectbox('Selecione Setor IBGE', ibge_options)
            filtered_df_pj_ibge = df_pj[df_pj['Setor IBGE'] == selected_setor_ibge]

            porte_options = filtered_df_pj_ibge['Porte'].value_counts().index.tolist()
            selected_porte = st.selectbox('Selecione o porte da empresa', porte_options)
            filtered_df_pj_porte = filtered_df_pj_ibge[filtered_df_pj_ibge['Porte'] == selected_porte]

        with col2:
            estado_options_pj = filtered_df_pj_porte['Estado'].value_counts().index.tolist()
            selected_estado_pj = st.selectbox('Selecione um estado', estado_options_pj)
            filtered_df_pj_estado = filtered_df_pj_porte[filtered_df_pj_porte['Estado'] == selected_estado_pj]
            
            cidade_options_pj = filtered_df_pj_estado['Cidade'].value_counts().index.tolist()
            selected_cidade_pj = st.selectbox('Selecione uma cidade', cidade_options_pj)
            filtered_df_pj_cidade = filtered_df_pj_estado[filtered_df_pj_estado['Cidade'] == selected_cidade_pj]

        cnae_options = filtered_df_pj_cidade['Classificação CNAE - Subclasse'].value_counts().index.tolist()
        selected_cnae = st.selectbox('Selecione uma classificação CNAE', cnae_options)
        filtered_df_pj = filtered_df_pj_cidade[filtered_df_pj_cidade['Classificação CNAE - Subclasse'] == selected_cnae]
        ##################################################################################### 
        ############################### Regras de associacao ################################

        regras_pj = processar_regras_associacao_pj(filtered_df_pj) 
        
         # Create an expander for the filtered table
        with st.expander('Visualizar tabela filtrada', expanded=False):
            st.markdown('#### <span style="color:#00547c"> Tabela filtrada </span>', unsafe_allow_html=True) 
            st.dataframe(filtered_df_pj)


        # Função para filtrar os produtos consequentes relacionados ao produto antecedente clicado
        def filter_consequents(antecedent):
            consequents = regras_pj[regras_pj['antecedents'].apply(lambda x: antecedent in x)]['consequents']
            return consequents.explode().unique()

        # Display the association rules
        st.markdown('#### <span style="color:#00547c"> Regra de Associação </span>', unsafe_allow_html=True) 

        antecedents = regras_pj['antecedents'].explode().unique()

        col1, col2 = st.columns(2)

        for i, antecedent in enumerate(antecedents):
            if i % 2 == 0:
                with col1.expander(f'Produtos consequentes de {antecedent}', expanded=False):
                    consequents = filter_consequents(antecedent)
                    st.write(consequents)
            else:
                with col2.expander(f'Produtos consequentes de {antecedent}', expanded=False):
                    consequents = filter_consequents(antecedent)
                    st.write(consequents)
        
        # Display the modified dataframe
        regras_pj_d = regras_pj.copy()
        regras_pj_d['antecedents'] = regras_pj_d['antecedents'].apply(lambda x: ', '.join(x))
        regras_pj_d['consequents'] = regras_pj_d['consequents'].apply(lambda x: ', '.join(x))

        with st.expander('Visualização geral de regra de associação com filtro', expanded=False):
            st.dataframe(regras_pj_d.sort_values("support", ascending=False))

            if st.button("Exportar para CSV"):
                csv = regras_pj_d.to_csv(index=False)
                st.download_button(label="Baixar CSV", data=csv, file_name='regras_apriori_pj.csv', mime='text/csv', key='exported_pj')
        #####################################################################################
        ################################# Grafico de Barras #################################
        # Construção do DataFrame para o Treemap
        data = {'antecedents': [], 'consequents': [], 'confidence': []}
        for index, row in regras_pj.iterrows():
            antecedente = list(row['antecedents'])[0]  # Convertendo frozenset para lista
            consequentes = list(row['consequents'])    # Convertendo frozenset para lista
            confidence = row['confidence']      # Multiplicando por 100 para obter a porcentagem
            for consequent in consequentes:
                data['antecedents'].append(antecedente)
                data['consequents'].append(consequent)
                data['confidence'].append(confidence)

        # Criando o DataFrame
        df = pd.DataFrame(data)

        # Criando uma nova coluna contendo a contagem de ocorrências
        df['count'] = 1

        # Agrupando os dados para criar as barras empilhadas e ordenando a contagem de antecedentes em ordem decrescente
        grouped_df = df.groupby(['antecedents', 'consequents']).size().unstack(fill_value=0)
        grouped_df = grouped_df[grouped_df.sum().sort_values(ascending=False).index]

        # Criando o gráfico de barras empilhadas
        fig = go.Figure()

        # Define a paleta de cores em tons de azul
        colors = ['royalblue', 'lightblue', 'skyblue', 'deepskyblue', 'dodgerblue', 'cornflowerblue', 'steelblue']

        for i, consequent in enumerate(grouped_df.columns):
            fig.add_trace(go.Bar(
                y=grouped_df.index,
                x=grouped_df[consequent],
                name=consequent,
                orientation='h',
                marker=dict(color=colors[i % len(colors)])
            ))

        # Atualizando o layout do gráfico
        fig.update_layout(
            barmode='stack',
            yaxis_title='Antecedents',
            xaxis_title='Ocorrências',
            title=''
        )
        fig.update_layout(height=800, width=1400)

        st.markdown('#### <span style="color:#00547c"> Gráfico de barras empilhadas relacionando produtos antecedentes com consequentes</span>', unsafe_allow_html=True) 
        # Exibindo o gráfico
        st.plotly_chart(fig)
        #####################################################################################
        ############################# Recomendacao por Cliente ##############################
        st.markdown('#### <span style="color:#00547c"> Filtrando por Cliente: </span>', unsafe_allow_html=True) 

        produto_counts = filtered_df_pj.groupby(['ID Cliente', 'Produto GPOM e Área de Atuação']).size()

        # Filtrar para obter apenas clientes com produtos que aparecem mais de uma vez
        cliente_options = produto_counts[produto_counts > 2].reset_index()['ID Cliente'].unique()
        select_cliente = st.selectbox('Selecione um Cliente', cliente_options)

        produtos = filtered_df_pj[filtered_df_pj['ID Cliente'] == select_cliente]['Produto GPOM e Área de Atuação'].unique()
        associated_products = find_associated_products(produtos, regras_pj)
        
        with st.expander(f'Produtos comprados e recomendados do cliente {select_cliente}', expanded=False):
            col1, col2 = st.columns(2)
            with col1: 
                st.markdown('#### <span style="color:#00547c"> Produtos comprados </span>', unsafe_allow_html=True)
                st.dataframe(produtos, use_container_width=True)
            with col2:
                st.markdown('#### <span style="color:#00547c"> Produtos recomendados </span>', unsafe_allow_html=True)
                if associated_products:
                    # Se houver produtos associados, mostramos eles
                    st.dataframe(associated_products, use_container_width=True)
                else:
                    # Se não houver produtos associados, mostrar uma mensagem
                    st.write("Não há produtos associados para mostrar.")
        #####################################################################################
    with aba2:
        df = df_pf
        ###################################### Filtros ###################################### 
        st.markdown('### <span style="color:#00547c"> Filtrando por Perfil de Cliente: </span>', unsafe_allow_html=True)
        
        faixas_etarias = {
        '0 a 12 anos': (0, 12),
        '13 a 17 anos': (13, 17),
        '18 a 24 anos': (18, 24),
        '25 a 34 anos': (25, 34),
        '35 a 64 anos': (35, 64),
        '65 anos ou mais': (65, 80),
        'Todas': (0, 80) 
    }
        faixas = ['0 a 12 anos', '13 a 17 anos', '18 a 24 anos', '25 a 34 anos', '35 a 64 anos', '65 anos ou mais', 'Todas']
        faixa_etaria = st.selectbox('Selecione a faixa etária desejada:', faixas)
        idade_inicio, idade_fim = faixas_etarias[faixa_etaria]
        filtered_df_pf_idade = df[(df['Idade'] >= idade_inicio) & (df['Idade'] <= idade_fim)]

        estado_options = filtered_df_pf_idade['Estado'].value_counts().index.tolist()
        selected_estado = st.selectbox('Selecione um estado', estado_options)
        filtered_df_pf_estado = filtered_df_pf_idade[filtered_df_pf_idade['Estado'] == selected_estado]

        cidade_options = filtered_df_pf_estado['Cidade'].value_counts().index.tolist()
        selected_cidade = st.selectbox('Selecione uma cidade', cidade_options)
        filtered_df_pf = filtered_df_pf_estado[filtered_df_pf_estado['Cidade'] == selected_cidade]

        ##################################################################################### 
        ############################### Regras de associacao ################################
        regras_pf = processar_regras_associacao_pf(filtered_df_pf) 
        
        # Create an expander for the filtered table
        with st.expander('Visualizar tabela filtrada', expanded=False):
            st.markdown('#### <span style="color:#00547c"> Tabela filtrada </span>', unsafe_allow_html=True) 
            st.dataframe(filtered_df_pf)


        # Função para filtrar os produtos consequentes relacionados ao produto antecedente clicado
        def filter_consequents(antecedent):
            consequents = regras_pf[regras_pf['antecedents'].apply(lambda x: antecedent in x)]['consequents']
            return consequents.explode().unique()

        # Display the association rules
        st.markdown('#### <span style="color:#00547c"> Regra de Associação </span>', unsafe_allow_html=True) 

        antecedents = regras_pf['antecedents'].explode().unique()

        col1, col2 = st.columns(2) 

        for i, antecedent in enumerate(antecedents):
            if i % 2 == 0:
                with col1.expander(f'Produtos consequentes de {antecedent}', expanded=False):
                    consequents = filter_consequents(antecedent)
                    st.write(consequents)
            else:
                with col2.expander(f'Produtos consequentes de {antecedent}', expanded=False):
                    consequents = filter_consequents(antecedent)
                    st.write(consequents)

        # Display the modified dataframe
        regras_pf_d = regras_pf.copy()
        regras_pf_d['antecedents'] = regras_pf_d['antecedents'].apply(lambda x: ', '.join(x))
        regras_pf_d['consequents'] = regras_pf_d['consequents'].apply(lambda x: ', '.join(x))

        with st.expander('Visualização geral de regra de associação com filtro', expanded=False):
            st.dataframe(regras_pf_d.sort_values("support", ascending=False))

            if st.button("Exportar os dados de Pessoa Física para CSV"):
                csv = regras_pf_d.to_csv(index=False)
                st.download_button(label="Baixar CSV", data=csv, file_name='regras_apriori_pf.csv', mime='text/csv', key='exported_pf')
        #####################################################################################
        ################################# Grafico de Barras #################################
        # Construção do DataFrame para o Treemap
        data = {'antecedents': [], 'consequents': [], 'confidence': []}
        for index, row in regras_pf.iterrows():
            antecedente = list(row['antecedents'])[0]  # Convertendo frozenset para lista
            consequentes = list(row['consequents'])    # Convertendo frozenset para lista
            confidence = row['confidence']      # Multiplicando por 100 para obter a porcentagem
            for consequent in consequentes:
                data['antecedents'].append(antecedente)
                data['consequents'].append(consequent)
                data['confidence'].append(confidence)

        # Criando o DataFrame
        df = pd.DataFrame(data)

        # Criando uma nova coluna contendo a contagem de ocorrências
        df['count'] = 1

        # Agrupando os dados para criar as barras empilhadas e ordenando a contagem de antecedentes em ordem decrescente
        grouped_df = df.groupby(['antecedents', 'consequents']).size().unstack(fill_value=0)
        grouped_df = grouped_df[grouped_df.sum().sort_values(ascending=False).index]

        # Criando o gráfico de barras empilhadas
        fig = go.Figure()

        # Define a paleta de cores em tons de azul
        colors = ['royalblue', 'lightblue', 'skyblue', 'deepskyblue', 'dodgerblue', 'cornflowerblue', 'steelblue']

        for i, consequent in enumerate(grouped_df.columns):
            fig.add_trace(go.Bar(
                y=grouped_df.index,
                x=grouped_df[consequent],
                name=consequent,
                orientation='h',
                marker=dict(color=colors[i % len(colors)])
            ))

        # Atualizando o layout do gráfico
        fig.update_layout(
            barmode='stack',
            yaxis_title='Antecedents',
            xaxis_title='Ocorrências',
            title=''
        )
        fig.update_layout(height=800, width=1400)

        st.markdown('#### <span style="color:#00547c"> Gráfico de barras empilhadas relacionando produtos antecedentes com consequentes</span>', unsafe_allow_html=True) 
        # Exibindo o gráfico
        st.plotly_chart(fig)
        #####################################################################################
        ############################# Recomendacao por Cliente ##############################
        st.markdown('#### <span style="color:#00547c"> Filtrando por Cliente: </span>', unsafe_allow_html=True) 

        produto_counts = filtered_df_pf.groupby(['ID Cliente', 'Produto GPOM e Área de Atuação']).size()
        
        grupo_clientes = df_pf.groupby(['ID Cliente', 'Data de Nascimento']).size()
        
        # Filtrar para obter apenas clientes com produtos que aparecem mais de uma vez
        clientes_com_produtos_repetidos = produto_counts[produto_counts > 2].reset_index()['ID Cliente'].unique()

        # Usar esse filtro para os cliente_options no selectbox
        cliente_options = clientes_com_produtos_repetidos
        select_cliente = st.selectbox('Selecione um Cliente', cliente_options)

        produtos = filtered_df_pf[filtered_df_pf['ID Cliente'] == select_cliente]['Produto GPOM e Área de Atuação'].unique()
        associated_products = find_associated_products(produtos, regras_pf)

        with st.expander(f'Produtos comprados e recomendados do cliente {select_cliente}', expanded=False):
            col1, col2 = st.columns(2)
            with col1: 
                st.markdown('#### <span style="color:#00547c"> Produtos comprados </span>', unsafe_allow_html=True)
                st.dataframe(produtos, use_container_width=True)
            with col2:
                st.markdown('#### <span style="color:#00547c"> Produtos recomendados </span>', unsafe_allow_html=True)
                if associated_products:
                    st.dataframe(associated_products, use_container_width=True)
                else:
                    # Se não houver produtos associados, mostrar uma mensagem
                    st.write("Não há produtos associados para mostrar.")
       #####################################################################################
############################################################################################################
######################################### PÁGINA 4 - CONTATO ###############################################
############################################################################################################
    
elif choose == "Contato":
    with open ("README.md", 'r') as f:
        st.markdown(f.read(), unsafe_allow_html=True)