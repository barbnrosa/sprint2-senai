import streamlit as st
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Criar uma função para processar as regras de associação
def processar_regras_associacao_pf(df_pf):
    transacao = []

    for cliente_id in df_pf['ID Cliente'].unique():
        # Obter todas as transações do cliente
        transacoes_cliente = df_pf[df_pf['ID Cliente'] == cliente_id]

        # Agregar transações por produto e data de nascimento
        transacoes_agrupadas = transacoes_cliente.groupby(['Produto GPOM e Área de Atuação', 'Data de Nascimento']).size().reset_index(name='count')

        # Criar uma lista de produtos únicos por cliente
        lista_produtos = list(transacoes_agrupadas['Produto GPOM e Área de Atuação'])

        # Adicionar lista de produtos únicos à lista de transações
        transacao.append(lista_produtos)

    te = TransactionEncoder() # estanciar função
    transacao_te = te.fit(transacao).transform(transacao)

    # transformar em dataframe
    transacao_transformado = pd.DataFrame(transacao_te, columns=te.columns_)

    items_frequentes_apriori = apriori(transacao_transformado, use_colnames=True, min_support=0.02)
    items_frequentes_apriori_sorted = items_frequentes_apriori.sort_values(['support'],ascending=False)

    regras_apriori = association_rules(items_frequentes_apriori_sorted, metric='confidence', min_threshold=0.2)
    return regras_apriori

def processar_regras_associacao_pj(df_pj):

    transacao = []

    for cliente_id in df_pj['ID Cliente'].unique():
        # Obter todas as transações do cliente
        transacoes_cliente = df_pj[df_pj['ID Cliente'] == cliente_id]

        # Agregar transações por produto e data de nascimento
        transacoes_agrupadas = transacoes_cliente.groupby(['Produto GPOM e Área de Atuação']).size().reset_index(name='count')

        # Criar uma lista de produtos únicos por cliente
        lista_produtos = list(transacoes_agrupadas['Produto GPOM e Área de Atuação'])

        # Adicionar lista de produtos únicos à lista de transações
        transacao.append(lista_produtos)

    te = TransactionEncoder() # estanciar função
    transacao_te = te.fit(transacao).transform(transacao)

    # transformar em dataframe
    transacao_transformado = pd.DataFrame(transacao_te, columns=te.columns_)

    items_frequentes_apriori = apriori(transacao_transformado, use_colnames=True, min_support=0.1)
    items_frequentes_apriori_sorted = items_frequentes_apriori.sort_values(['support'],ascending=False)

    regras_apriori = association_rules(items_frequentes_apriori_sorted, metric='confidence', min_threshold=0.5)
    return regras_apriori

def find_associated_products(client_products, rules_df):
            associated_products = set()
            
            # Convertendo client_products para sets para facilitar a comparação
            client_product_sets = [frozenset([item]) for item in client_products]
            
            for client_product_set in client_product_sets:
                for _, row in rules_df.iterrows():
                    # Se o produto do cliente é um subconjunto dos antecedentes ou dos consequentes
                    if client_product_set.issubset(row['antecedents']) or client_product_set.issubset(row['consequents']):
                        # Adicionamos os produtos associados dos antecedentes e dos consequentes
                        associated_products.update(row['antecedents'].union(row['consequents']))
            
            client_product_sets_2 =  frozenset(client_products)
            ## Removendo os produtos que o cliente já compra, já que estamos interessados apenas nos novos produtos associados
            associated_products.difference_update(client_product_sets_2)
            
            # Converter o set em uma lista para exibição
            return list(associated_products)