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
from funcoes import processar_regras_associacao_pf, processar_regras_associacao_pj
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
    #st.header("Regra de Associação")    
  
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #00547c;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('## <span style="color:#00547c"> Regra de Associação </span>', unsafe_allow_html=True)  

    selected_base = st.radio(
        "Selecione a Base de Dados que deseja visualizar", 
        ["Pessoa Física", "Pessoa Jurídica"],
        horizontal=True)
    
    if selected_base == "Pessoa Física":
        regras = processar_regras_associacao_pf(df_pf)
        df = df_pf
        
    else:
        regras = processar_regras_associacao_pj(df_pj)
        df = df_pj
        
    
    with st.expander("Visualizar Regras de Associação"):
        st.markdown('### <span style="color:#00547c"> Algoritmo Apriori </span>', unsafe_allow_html=True)  
        # Executar o processamento das regras de associação
         # Adicionar controle deslizante para a porcentagem de confiança
        #min_confidence = st.slider("Selecione a porcentagem mínima de confiança:", min_value=0.0, max_value=1.0, step=0.05, value=0.2)

        # Exibir o resultado na aplicação Streamlit
        st.write(regras)
         # Adicionar um botão para exportar para CSV
        if st.button("Exportar para CSV"):
            csv = regras.to_csv(index=False)
            st.download_button(label="Baixar CSV", data=csv, file_name='regras_apriori.csv', mime='text/csv')

    
    st.markdown('### <span style="color:#00547c"> Filtrando por Perfil de Cliente: </span>', unsafe_allow_html=True) 

    # Função para filtrar os produtos consequentes relacionados ao produto antecedente clicado
    def filter_consequents(antecedent):
        consequents = regras[regras['antecedents'].apply(lambda x: antecedent in x)]['consequents']
        return consequents.explode().unique()

    selected_setor_ibge = st.selectbox('Select Setor IBGE', df_pj['Setor IBGE'].unique())
    selected_porte = st.selectbox('Select Porte', df_pj['Porte'].unique())

    filtered_df = df_pj[(df_pj['Setor IBGE'] == selected_setor_ibge) & (df_pj['Porte'] == selected_porte)]

   # Create an expander for the filtered table
    with st.expander('Visualizar tabela filtrada', expanded=False):
        st.markdown('#### <span style="color:#00547c"> Tabela filtrada </span>', unsafe_allow_html=True) 
        st.dataframe(filtered_df)

    # Display the association rules
    st.markdown('#### <span style="color:#00547c"> Regra de Associação </span>', unsafe_allow_html=True) 

    antecedents = regras['antecedents'].explode().unique()

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
    with st.expander('Visualização geral de regra de associação com filtro', expanded=False):
        st.dataframe(regras.sort_values("support", ascending=False))






############################################################################################################
######################################### PÁGINA 4 - CONTATO ###############################################
############################################################################################################
    
elif choose == "Contato":
    with open ("README.md", 'r') as f:
        st.markdown(f.read(), unsafe_allow_html=True)